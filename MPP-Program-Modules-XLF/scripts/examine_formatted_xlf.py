"""Examine HTML-formatted XLF structure to understand inline formatting tags."""

import xml.etree.ElementTree as ET
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Parse the HTML-formatted XLF
xlf_path = r'C:\Users\MarieLexisDad\Downloads\Module-1-do-d-mentor-protege-program (1).xlf'
tree = ET.parse(xlf_path)
root = tree.getroot()

ns = {
    'xliff': 'urn:oasis:names:tc:xliff:document:1.2',
    'html': 'http://www.w3.org/1999/xhtml'
}

# Find units with bullet lists
print("=" * 80)
print("EXAMINING HTML-FORMATTED XLF STRUCTURE")
print("=" * 80)

def extract_text_from_element(elem):
    """Recursively extract all text from an element and its children."""
    text_parts = []
    if elem.text:
        text_parts.append(elem.text)
    for child in elem:
        text_parts.extend(extract_text_from_element(child))
        if child.tail:
            text_parts.append(child.tail)
    return text_parts

def print_element_tree(elem, indent=0):
    """Print element tree structure."""
    tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
    attrs = ' '.join(f'{k.split("}")[-1]}="{v}"' for k, v in elem.attrib.items())

    text_content = elem.text.strip() if elem.text and elem.text.strip() else ""
    if text_content:
        print(f"{'  ' * indent}<{tag} {attrs}>{text_content[:60]}...")
    else:
        print(f"{'  ' * indent}<{tag} {attrs}>")

    for child in elem:
        print_element_tree(child, indent + 1)

# Find a unit with bullet list
trans_units = root.findall('.//xliff:trans-unit', ns)
print(f"\nTotal trans-units: {len(trans_units)}\n")

bullet_unit = None
for unit in trans_units:
    source = unit.find('xliff:source', ns)
    if source is not None:
        # Check if has UL tags
        for elem in source.iter():
            if 'ctype' in elem.attrib and 'UL' in elem.attrib['ctype']:
                bullet_unit = unit
                break
    if bullet_unit:
        break

if bullet_unit:
    print("FOUND UNIT WITH BULLET LIST:")
    print(f"Unit ID: {bullet_unit.get('id')}\n")

    source = bullet_unit.find('xliff:source', ns)
    print("SOURCE STRUCTURE:")
    print("-" * 80)
    print_element_tree(source)

    print("\n" + "=" * 80)
    print("EXTRACTED TEXT FROM SOURCE:")
    print("-" * 80)
    text_parts = extract_text_from_element(source)
    for i, part in enumerate(text_parts, 1):
        print(f"{i}. {part.strip()}")

    print("\n" + "=" * 80)
    print("FULL XML:")
    print("-" * 80)
    print(ET.tostring(source, encoding='unicode'))
else:
    print("No unit with bullet list found. Examining first 5 units with <g> tags:")
    print("-" * 80)

    count = 0
    for unit in trans_units:
        source = unit.find('xliff:source', ns)
        if source is not None and len(list(source)) > 0:
            print(f"\nUnit {count + 1} - ID: {unit.get('id')}")
            print_element_tree(source)
            count += 1
            if count >= 5:
                break

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
