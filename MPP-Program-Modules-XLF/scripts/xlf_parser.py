"""
XLF Parser Agent - Extract translation units with exact structure preservation
"""

import xml.etree.ElementTree as ET
import json
import re
from typing import Dict, List, Tuple

def parse_xlf_file(xlf_path: str) -> Dict:
    """
    Parse XLF file maintaining EXACT structure (read-only operation)
    Extract all 568 translation units with comprehensive metadata
    """

    # Parse XML with namespace handling
    tree = ET.parse(xlf_path)
    root = tree.getroot()

    # XLF namespace
    ns = {'xliff': 'urn:oasis:names:tc:xliff:document:1.2'}

    # Extract all translation units
    trans_units = root.findall('.//xliff:trans-unit', ns)

    print(f"Found {len(trans_units)} translation units")

    all_units = []
    substantive_units = []

    for idx, unit in enumerate(trans_units):
        unit_id = unit.get('id', f'unknown_{idx}')

        # Extract source text
        source_elem = unit.find('xliff:source', ns)
        source_text = ''
        if source_elem is not None:
            # Get all text including nested elements
            source_text = ''.join(source_elem.itertext()).strip()

        # Extract target text (if exists)
        target_elem = unit.find('xliff:target', ns)
        target_text = ''
        if target_elem is not None:
            target_text = ''.join(target_elem.itertext()).strip()

        # Extract notes
        notes = []
        note_elements = unit.findall('xliff:note', ns)
        for note_elem in note_elements:
            note_text = note_elem.text or ''
            notes.append(note_text.strip())

        # Check for ******* patterns in notes
        has_notes = len(notes) > 0
        note_positions = []

        for note_idx, note in enumerate(notes):
            if '*******' in note or note.strip():
                note_positions.append({
                    'position': note_idx,
                    'content': note,
                    'has_asterisks': '*******' in note
                })

        # Word count (substantive = >10 words)
        word_count = len(source_text.split())

        # Build unit data
        unit_data = {
            'unit_id': unit_id,
            'index': idx,
            'source_text': source_text,
            'target_text': target_text,
            'has_notes': has_notes,
            'notes': notes,
            'note_positions': note_positions,
            'word_count': word_count,
            'is_substantive': word_count > 10,
            'xml_position': idx
        }

        all_units.append(unit_data)

        # Collect substantive units for sample
        if word_count > 10:
            substantive_units.append(unit_data)

    # Add context (surrounding units) for verification
    for i, unit in enumerate(all_units):
        context = {
            'previous': all_units[i-1]['source_text'][:100] if i > 0 else None,
            'next': all_units[i+1]['source_text'][:100] if i < len(all_units) - 1 else None
        }
        unit['context'] = context

    # Get first 20 substantive units
    sample_units = substantive_units[:20]

    # Statistics
    stats = {
        'total_units': len(all_units),
        'substantive_units': len(substantive_units),
        'units_with_notes': sum(1 for u in all_units if u['has_notes']),
        'units_with_asterisk_notes': sum(1 for u in all_units if any(np['has_asterisks'] for np in u['note_positions'])),
        'average_word_count': sum(u['word_count'] for u in all_units) / len(all_units) if all_units else 0,
        'sample_size': len(sample_units)
    }

    return {
        'statistics': stats,
        'all_units': all_units,
        'substantive_units': substantive_units,
        'sample_first_20': sample_units
    }


def main():
    xlf_path = r'C:\Users\MarieLexisDad\Downloads\Copy-of-module-1-do-d-mentor-protege-program.xlf'
    output_path = r'C:\Users\MarieLexisDad\scripts\xlf_parsed_units.json'

    print("Starting XLF Parser Agent...")
    print(f"Input: {xlf_path}")
    print(f"Output: {output_path}")
    print("-" * 80)

    # Parse the file
    result = parse_xlf_file(xlf_path)

    # Display statistics
    print("\n=== PARSING STATISTICS ===")
    for key, value in result['statistics'].items():
        print(f"{key}: {value}")

    # Display sample of first 5 substantive units
    print("\n=== SAMPLE: First 5 Substantive Units ===")
    for i, unit in enumerate(result['sample_first_20'][:5], 1):
        print(f"\n--- Unit {i} (ID: {unit['unit_id']}) ---")
        print(f"Word Count: {unit['word_count']}")
        print(f"Has Notes: {unit['has_notes']}")
        print(f"Source Text: {unit['source_text'][:150]}...")
        if unit['notes']:
            print(f"Notes: {unit['notes']}")

    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Successfully saved parsed data to: {output_path}")
    print(f"✓ Total units: {result['statistics']['total_units']}")
    print(f"✓ Substantive units (>10 words): {result['statistics']['substantive_units']}")
    print(f"✓ Sample first 20 saved for review")


if __name__ == '__main__':
    main()
