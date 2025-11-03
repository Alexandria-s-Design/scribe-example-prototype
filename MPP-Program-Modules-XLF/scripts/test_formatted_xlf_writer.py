"""
Test script to verify formatted XLF writer preserves inline formatting.

Tests with a sample unit that has bullet lists.
"""

import sys
import os
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from xlf_writer_formatted import FormattedXLFWriter
from xlf_parser import parse_xlf_file
from transformation_engine import apply_all_transformations, TransformationContext


def main():
    print("=" * 80)
    print("TESTING FORMATTED XLF WRITER - FORMATTING PRESERVATION")
    print("=" * 80)

    # Paths
    input_xlf = r'C:\Users\MarieLexisDad\Downloads\Module-1-do-d-mentor-protege-program (1).xlf'
    output_xlf = r'C:\Users\MarieLexisDad\Downloads\Module-1-FORMATTED-TEST.xlf'

    print(f"\nInput XLF:  {input_xlf}")
    print(f"Output XLF: {output_xlf}")

    # Step 1: Parse XLF
    print("\n" + "-" * 80)
    print("STEP 1: Parsing XLF...")
    print("-" * 80)

    parse_result = parse_xlf_file(input_xlf)
    units = parse_result.get('all_units', [])

    print(f"✓ Parsed {len(units)} units")

    # Find the bullet list unit we examined earlier
    test_unit_id = "items|id:cmbrbpsre03c02a6y4bwgiai6|items|id:cmbrbpsrf03c62a6yndlhr9uu|paragraph"
    test_unit = next((u for u in units if u['unit_id'] == test_unit_id), None)

    if not test_unit:
        print(f"❌ Test unit not found: {test_unit_id}")
        return

    print(f"\n✓ Found test unit with bullet list:")
    print(f"  Unit ID: {test_unit['unit_id']}")
    print(f"  Original text length: {len(test_unit['source_text'])} chars")
    print(f"\n  Original text:")
    print(f"  {test_unit['source_text'][:200]}...")

    # Step 2: Apply transformation
    print("\n" + "-" * 80)
    print("STEP 2: Applying transformation...")
    print("-" * 80)

    context = TransformationContext(
        acronym_first_mentions=set(),
        unit_number=1,
        lesson_number=1,
        notes_positions=[],
        total_source_length=len(test_unit['source_text']),
        total_target_length=0
    )

    transformed = apply_all_transformations(test_unit['source_text'], context)

    print(f"✓ Transformed text length: {len(transformed)} chars")
    print(f"\n  Transformed text:")
    print(f"  {transformed[:200]}...")

    # Check if transformation made changes
    if transformed == test_unit['source_text']:
        print("\n  ℹ No changes made by transformation (text was already compliant)")
    else:
        print(f"\n  ℹ Text modified by transformation")

    # Step 3: Write with formatting preservation
    print("\n" + "-" * 80)
    print("STEP 3: Writing XLF with formatting preservation...")
    print("-" * 80)

    writer = FormattedXLFWriter(input_xlf)

    # Create transformation dict
    transformations = [
        {
            'unit_id': test_unit['unit_id'],
            'transformed': transformed
        }
    ]

    updated_count = writer.update_targets_with_formatting(transformations)

    print(f"\n✓ Updated {updated_count} unit(s)")

    # Save output
    writer.save(output_xlf)

    # Step 4: Verify formatting preservation
    print("\n" + "-" * 80)
    print("STEP 4: Verifying formatting preservation...")
    print("-" * 80)

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
        print(f"\n❌ WARNING: Formatting may not be fully preserved")
        print(f"   Expected {stats['original_g_tags']} <g> tags, got {stats['output_g_tags']}")

    # Step 5: Examine output structure
    print("\n" + "-" * 80)
    print("STEP 5: Examining output target structure...")
    print("-" * 80)

    import xml.etree.ElementTree as ET

    output_tree = ET.parse(output_xlf)
    output_root = output_tree.getroot()

    ns = {'xliff': 'urn:oasis:names:tc:xliff:document:1.2'}

    # Find the test unit in output
    test_unit_elem = output_root.find(f'.//xliff:trans-unit[@id="{test_unit_id}"]', ns)

    if test_unit_elem is not None:
        target = test_unit_elem.find('xliff:target', ns)

        if target is not None:
            print(f"\n✓ Target element created")

            # Count <g> tags in target
            g_tags = target.findall('.//{*}g')
            print(f"  <g> tags in target: {len(g_tags)}")

            # Check for UL tag
            ul_tags = [g for g in g_tags if g.get('ctype') == 'x-html-UL']
            li_tags = [g for g in g_tags if g.get('ctype') == 'x-html-LI']

            print(f"  UL tags (bullet lists): {len(ul_tags)}")
            print(f"  LI tags (list items): {len(li_tags)}")

            if len(ul_tags) > 0 and len(li_tags) > 0:
                print(f"\n✓ BULLET LIST FORMATTING PRESERVED!")
            else:
                print(f"\n❌ WARNING: Bullet list formatting may be missing")

            # Show sample of target XML
            target_xml = ET.tostring(target, encoding='unicode')
            print(f"\n  Sample target XML (first 500 chars):")
            print(f"  {target_xml[:500]}...")

        else:
            print(f"\n❌ No target element found in output")
    else:
        print(f"\n❌ Test unit not found in output")

    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

    print(f"\nOutput file saved to:")
    print(f"  {output_xlf}")
    print(f"\nYou can now import this XLF back into Articulate Rise to verify formatting.")


if __name__ == '__main__':
    main()
