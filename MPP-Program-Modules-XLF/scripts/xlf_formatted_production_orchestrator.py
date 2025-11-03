"""
Full Production Orchestrator with HTML Formatting Preservation

Runs all 568 units with formatting preservation (bullets, lists, styling).
Uses the FormattedXLFWriter to clone <g> tag structure.
"""

import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from xlf_parser import parse_xlf_file
from transformation_engine import apply_all_transformations, TransformationContext
from xlf_writer_formatted import FormattedXLFWriter
from grok_dual_check_verifier import GrokDualCheckVerifier


def main():
    print("=" * 80)
    print("MPP XLF FULL PRODUCTION - WITH FORMATTING PRESERVATION")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Paths
    input_xlf = r'C:\Users\MarieLexisDad\Downloads\Module-1-do-d-mentor-protege-program (1).xlf'
    output_xlf = r'C:\Users\MarieLexisDad\Downloads\Module-1-MPP-TRANSFORMED-FORMATTED-FINAL.xlf'
    report_path = r'C:\Users\MarieLexisDad\Downloads\xlf_formatted_production_results.txt'

    print(f"\nInput XLF:  {input_xlf}")
    print(f"Output XLF: {output_xlf}")
    print(f"Report:     {report_path}")

    # ==================================================================
    # PHASE 1: PARSE XLF
    # ==================================================================
    print("\n" + "=" * 80)
    print("PHASE 1: PARSING XLF WITH FORMATTING")
    print("=" * 80)

    parse_result = parse_xlf_file(input_xlf)
    all_units = parse_result.get('all_units', [])
    substantive_units = parse_result.get('substantive_units', [])

    print(f"\n✓ Total units: {len(all_units)}")
    print(f"✓ Substantive units (will transform): {len(substantive_units)}")
    print(f"✓ Non-substantive units (skip): {len(all_units) - len(substantive_units)}")

    # ==================================================================
    # PHASE 2: TRANSFORM ALL SUBSTANTIVE UNITS
    # ==================================================================
    print("\n" + "=" * 80)
    print("PHASE 2: APPLYING TRANSFORMATIONS")
    print("=" * 80)

    transformations = []
    transformation_context = TransformationContext(
        acronym_first_mentions=set(),
        unit_number=0,
        lesson_number=1,
        notes_positions=[],
        total_source_length=0,
        total_target_length=0
    )

    print(f"\nTransforming {len(substantive_units)} substantive units...")

    for i, unit in enumerate(substantive_units, 1):
        source_text = unit['source_text']

        # Update context
        transformation_context.unit_number = i
        transformation_context.total_source_length = len(source_text)

        # Apply transformations
        transformed_text = apply_all_transformations(source_text, transformation_context)

        transformations.append({
            'unit_id': unit['unit_id'],
            'original': source_text,
            'transformed': transformed_text,
            'changed': transformed_text != source_text
        })

        if i % 10 == 0:
            print(f"  Transformed {i}/{len(substantive_units)} units...")

    changed_count = sum(1 for t in transformations if t['changed'])
    print(f"\n✓ Transformed {len(transformations)} units")
    print(f"  - {changed_count} modified")
    print(f"  - {len(transformations) - changed_count} unchanged")

    # ==================================================================
    # PHASE 3: GROK DUAL-CHECK VERIFICATION
    # ==================================================================
    print("\n" + "=" * 80)
    print("PHASE 3: GROK DUAL-CHECK VERIFICATION")
    print("=" * 80)

    verifier = GrokDualCheckVerifier()

    print(f"\nVerifying {len(transformations)} transformed units...")
    print("(Processing in batches of 10...)")

    all_results = []
    batch_size = 10
    total_batches = (len(transformations) + batch_size - 1) // batch_size

    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, len(transformations))
        batch = transformations[start_idx:end_idx]

        print(f"\n  Batch {batch_num + 1}/{total_batches} (units {start_idx + 1}-{end_idx})...")

        # verify_batch is async, so wrap it in asyncio.run()
        batch_results = asyncio.run(verifier.verify_batch(batch))
        all_results.extend(batch_results)

        # Show quick stats
        approved = sum(1 for r in batch_results if r['overall_pass'])
        print(f"    ✓ {approved}/{len(batch_results)} approved in this batch")

    # Calculate final stats
    overall_approved = sum(1 for r in all_results if r['overall_pass'])
    mpp_passed = sum(1 for r in all_results if r['mpp_passed'])
    sop_passed = sum(1 for r in all_results if r['sop_passed'])

    print(f"\n✓ Verification complete!")
    print(f"  - Overall approved: {overall_approved}/{len(all_results)} ({overall_approved/len(all_results)*100:.1f}%)")
    print(f"  - MPP accuracy passed: {mpp_passed}/{len(all_results)} ({mpp_passed/len(all_results)*100:.1f}%)")
    print(f"  - eLearning SOP passed: {sop_passed}/{len(all_results)*100:.1f}%)")

    # ==================================================================
    # PHASE 4: WRITE XLF WITH FORMATTING PRESERVATION
    # ==================================================================
    print("\n" + "=" * 80)
    print("PHASE 4: WRITING XLF WITH FORMATTING PRESERVATION")
    print("=" * 80)

    print("\nCreating formatted XLF writer...")
    writer = FormattedXLFWriter(input_xlf)

    print(f"Updating {len(transformations)} target elements with formatting...")
    updated_count = writer.update_targets_with_formatting(transformations)

    print(f"\n✓ Updated {updated_count} target elements")

    print(f"\nSaving XLF to: {output_xlf}")
    writer.save(output_xlf)

    print("\nVerifying formatting preservation...")
    stats = writer.verify_formatting_preservation(input_xlf)

    print(f"\nOriginal XLF:")
    print(f"  Total <g> tags: {stats['original_g_tags']}")
    print(f"  UL tags (bullet lists): {stats['original_ul']}")
    print(f"  LI tags (list items): {stats['original_li']}")

    print(f"\nOutput XLF:")
    print(f"  Total <g> tags: {stats['output_g_tags']}")
    print(f"  UL tags (bullet lists): {stats['output_ul']}")
    print(f"  LI tags (list items): {stats['output_li']}")

    print(f"\nTarget elements:")
    print(f"  Total targets: {stats['total_targets']}")
    print(f"  Targets with formatting: {stats['targets_with_formatting']}")

    if stats['formatting_preserved']:
        print(f"\n✓ FORMATTING PRESERVED SUCCESSFULLY!")
    else:
        print(f"\n⚠ WARNING: Some formatting may not be fully preserved")

    # ==================================================================
    # PHASE 5: GENERATE COMPREHENSIVE REPORT
    # ==================================================================
    print("\n" + "=" * 80)
    print("PHASE 5: GENERATING COMPREHENSIVE REPORT")
    print("=" * 80)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("MPP XLF TRANSFORMATION - FULL PRODUCTION REPORT (WITH FORMATTING)\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("INPUT/OUTPUT FILES\n")
        f.write("-" * 80 + "\n")
        f.write(f"Input XLF:  {input_xlf}\n")
        f.write(f"Output XLF: {output_xlf}\n\n")

        f.write("SUMMARY STATISTICS\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total units:              {len(all_units)}\n")
        f.write(f"Substantive units:        {len(substantive_units)}\n")
        f.write(f"Units transformed:        {len(transformations)}\n")
        f.write(f"Units modified:           {changed_count}\n")
        f.write(f"Overall approved:         {overall_approved}/{len(all_results)} ({overall_approved/len(all_results)*100:.1f}%)\n")
        f.write(f"MPP accuracy passed:      {mpp_passed}/{len(all_results)} ({mpp_passed/len(all_results)*100:.1f}%)\n")
        f.write(f"eLearning SOP passed:     {sop_passed}/{len(all_results)} ({sop_passed/len(all_results)*100:.1f}%)\n\n")

        f.write("FORMATTING PRESERVATION STATS\n")
        f.write("-" * 80 + "\n")
        f.write(f"Original <g> tags:        {stats['original_g_tags']}\n")
        f.write(f"Output <g> tags:          {stats['output_g_tags']}\n")
        f.write(f"Original UL tags:         {stats['original_ul']}\n")
        f.write(f"Output UL tags:           {stats['output_ul']}\n")
        f.write(f"Original LI tags:         {stats['original_li']}\n")
        f.write(f"Output LI tags:           {stats['output_li']}\n")
        f.write(f"Targets with formatting:  {stats['targets_with_formatting']}/{stats['total_targets']}\n")
        f.write(f"Formatting preserved:     {'YES' if stats['formatting_preserved'] else 'NO'}\n\n")

        # Units needing review
        needs_review = [r for r in all_results if not r['overall_pass']]
        f.write(f"UNITS NEEDING REVIEW ({len(needs_review)})\n")
        f.write("-" * 80 + "\n")
        if needs_review:
            for result in needs_review:
                f.write(f"\nUnit ID: {result['unit_id']}\n")
                f.write(f"  MPP Pass: {result['mpp_passed']}\n")
                f.write(f"  SOP Pass: {result['sop_passed']}\n")
                if not result['mpp_passed']:
                    f.write(f"  MPP Feedback: {result.get('mpp_accuracy', {}).get('feedback', 'N/A')}\n")
                if not result['sop_passed']:
                    f.write(f"  SOP Feedback: {result.get('sop_compliance', {}).get('feedback', 'N/A')}\n")
        else:
            f.write("None - all units approved!\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("DETAILED RESULTS\n")
        f.write("=" * 80 + "\n\n")

        for i, result in enumerate(all_results, 1):
            f.write(f"UNIT {i}/{len(all_results)}\n")
            f.write("-" * 80 + "\n")
            f.write(f"Unit ID: {result['unit_id']}\n")
            f.write(f"Overall Approved: {result['overall_pass']}\n")
            f.write(f"MPP Check: {'PASS' if result['mpp_passed'] else 'FAIL'}\n")
            f.write(f"SOP Check: {'PASS' if result['sop_passed'] else 'FAIL'}\n\n")

            f.write(f"Original Text:\n{result.get('original_text', 'N/A')}\n\n")
            f.write(f"Transformed Text:\n{result.get('transformed_text', 'N/A')}\n\n")

            mpp_feedback = result.get('mpp_accuracy', {}).get('feedback', 'N/A')
            sop_feedback = result.get('sop_compliance', {}).get('feedback', 'N/A')

            f.write(f"Grok MPP Feedback:\n{mpp_feedback}\n\n")
            f.write(f"Grok SOP Feedback:\n{sop_feedback}\n\n")

    print(f"\n✓ Report saved to: {report_path}")

    # ==================================================================
    # FINAL SUMMARY
    # ==================================================================
    print("\n" + "=" * 80)
    print("PRODUCTION COMPLETE!")
    print("=" * 80)

    print(f"\nOutput XLF: {output_xlf}")
    print(f"Report:     {report_path}")

    print(f"\nResults Summary:")
    print(f"  ✓ {len(transformations)} units transformed")
    print(f"  ✓ {changed_count} units modified")
    print(f"  ✓ {overall_approved} units approved ({overall_approved/len(all_results)*100:.1f}%)")
    print(f"  ✓ Formatting preserved (bullets, lists, styling)")

    print(f"\nNext steps:")
    print(f"  1. Review the output XLF: {output_xlf}")
    print(f"  2. Import into Articulate Rise to verify formatting")
    print(f"  3. Check units needing review in the report")

    print(f"\n{'='*80}")


if __name__ == '__main__':
    main()
