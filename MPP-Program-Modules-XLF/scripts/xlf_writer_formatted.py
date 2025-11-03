"""
XLF Writer with HTML Formatting Preservation

Preserves inline <g> tags (bullets, lists, styling) when writing transformed text to target elements.
"""

import xml.etree.ElementTree as ET
from typing import Dict, List
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


class FormattedXLFWriter:
    """XLF writer that preserves inline HTML formatting tags."""

    def __init__(self, xlf_path: str):
        """
        Initialize XLF writer.

        Args:
            xlf_path: Path to the XLF file to write to
        """
        self.xlf_path = xlf_path
        self.tree = ET.parse(xlf_path)
        self.root = self.tree.getroot()

        # Register namespaces
        self.namespace = 'urn:oasis:names:tc:xliff:document:1.2'
        self.html_namespace = 'http://www.w3.org/1999/xhtml'

        # Register namespaces to prevent ns0/ns1 prefixes
        ET.register_namespace('', self.namespace)
        ET.register_namespace('html', self.html_namespace)

        self.ns = {
            'xliff': self.namespace,
            'html': self.html_namespace
        }

    def extract_text_segments(self, element: ET.Element) -> List[str]:
        """
        Recursively extract text segments from element and its children.

        Returns list of text strings from leaf nodes (innermost elements).
        """
        text_segments = []

        # Check if this is a leaf node (has text but no children)
        if element.text and element.text.strip():
            if len(list(element)) == 0:  # No children - this is a leaf
                text_segments.append(element.text.strip())

        # Recursively process children
        for child in element:
            text_segments.extend(self.extract_text_segments(child))

        return text_segments

    def apply_transformed_text(self, element: ET.Element, transformed_segments: List[str], index: List[int]) -> None:
        """
        Recursively apply transformed text to leaf nodes in element tree.

        Args:
            element: The element to process
            transformed_segments: List of transformed text segments
            index: Mutable list with current index [0] to track position in segments
        """
        # Check if this is a leaf node
        if element.text and element.text.strip():
            if len(list(element)) == 0:  # No children - this is a leaf
                if index[0] < len(transformed_segments):
                    element.text = transformed_segments[index[0]]
                    index[0] += 1

        # Recursively process children
        for child in element:
            self.apply_transformed_text(child, transformed_segments, index)

    def clone_element_tree(self, source_elem: ET.Element) -> ET.Element:
        """
        Deep clone an element tree, copying all attributes and structure.

        Args:
            source_elem: Element to clone

        Returns:
            Cloned element with same structure
        """
        # Create new element with same tag
        cloned = ET.Element(source_elem.tag, attrib=dict(source_elem.attrib))

        # Copy text
        cloned.text = source_elem.text
        cloned.tail = source_elem.tail

        # Recursively clone children
        for child in source_elem:
            cloned.append(self.clone_element_tree(child))

        return cloned

    def update_targets_with_formatting(self, transformations: List[Dict]) -> int:
        """
        Update <target> elements with transformed text while preserving inline formatting.

        Args:
            transformations: List of dicts with 'unit_id' and 'transformed' keys

        Returns:
            Number of units successfully updated
        """
        transform_map = {t['unit_id']: t['transformed'] for t in transformations}
        trans_units = self.root.findall('.//xliff:trans-unit', self.ns)
        updated_count = 0

        for unit in trans_units:
            unit_id = unit.get('id', '')

            if unit_id in transform_map:
                transformed_text = transform_map[unit_id]
                source_elem = unit.find('xliff:source', self.ns)

                if source_elem is None:
                    continue

                # Extract original text segments from source
                original_segments = self.extract_text_segments(source_elem)

                if not original_segments:
                    # No text in source - skip
                    continue

                # Combine original text to compare with transformed
                original_text = ' '.join(original_segments)

                # Split transformed text into segments matching original structure
                # For now, use simple approach: if transformed is similar length,
                # try to map it back to segments. Otherwise, put all in first segment.

                if len(original_segments) == 1:
                    # Simple case - one text segment
                    transformed_segments = [transformed_text]
                else:
                    # Multiple segments - try to preserve structure
                    # This is a simplified approach - may need refinement
                    transformed_segments = self._split_transformed_text(
                        transformed_text, original_segments
                    )

                # Clone source structure to target
                target_elem = unit.find('xliff:target', self.ns)

                if target_elem is None:
                    # Create new target element
                    target_elem = ET.Element(f'{{{self.namespace}}}target')
                    target_elem.set('xml:lang', 'en-US')

                    # Insert after source
                    source_index = list(unit).index(source_elem)
                    unit.insert(source_index + 1, target_elem)
                else:
                    # Clear existing target content
                    target_elem.clear()
                    target_elem.set('xml:lang', 'en-US')

                # Clone source children to target
                for child in source_elem:
                    target_elem.append(self.clone_element_tree(child))

                # Apply transformed text to leaf nodes
                self.apply_transformed_text(target_elem, transformed_segments, [0])

                updated_count += 1

                if updated_count % 10 == 0:
                    print(f"  Updated {updated_count} units with formatting preservation...")

        return updated_count

    def _split_transformed_text(self, transformed: str, original_segments: List[str]) -> List[str]:
        """
        Split transformed text to match original segment structure.

        This is a heuristic approach that tries to map transformed text back to
        the original segment structure. May need refinement for complex cases.
        """
        # If transformed text is very different length, put it all in first segment
        original_total = ' '.join(original_segments)
        ratio = len(transformed) / max(len(original_total), 1)

        if ratio > 2.0 or ratio < 0.5:
            # Significant length change - put all in first segment, empty rest
            result = [transformed]
            result.extend([''] * (len(original_segments) - 1))
            return result

        # Try to split based on original segment boundaries
        # Find approximate split points
        result = []
        remaining = transformed
        total_original_len = sum(len(s) for s in original_segments)

        for i, orig_seg in enumerate(original_segments):
            if i == len(original_segments) - 1:
                # Last segment gets everything remaining
                result.append(remaining.strip())
            else:
                # Calculate proportional split point
                proportion = len(orig_seg) / max(total_original_len, 1)
                split_point = int(len(transformed) * proportion)

                # Find nearest sentence boundary near split point
                if split_point < len(remaining):
                    # Look for period, question mark, or exclamation point
                    for offset in range(20):
                        check_pos = split_point + offset
                        if check_pos >= len(remaining):
                            break
                        if remaining[check_pos] in '.!?':
                            split_point = check_pos + 1
                            break

                segment = remaining[:split_point].strip()
                result.append(segment)
                remaining = remaining[split_point:].strip()

        return result

    def save(self, output_path: str = None) -> None:
        """
        Save the modified XLF to file.

        Args:
            output_path: Optional output path. If None, overwrites original file.
        """
        if output_path is None:
            output_path = self.xlf_path

        # Write with UTF-8 encoding
        self.tree.write(
            output_path,
            encoding='utf-8',
            xml_declaration=True,
            method='xml'
        )

        print(f"\n✓ XLF saved to: {output_path}")

    def verify_formatting_preservation(self, original_xlf_path: str) -> Dict:
        """
        Verify that formatting structure was preserved by comparing tag counts.

        Args:
            original_xlf_path: Path to original XLF file

        Returns:
            Dict with verification statistics
        """
        original_tree = ET.parse(original_xlf_path)
        original_root = original_tree.getroot()

        # Count formatting tags in original
        original_g_tags = len(original_root.findall('.//{*}g'))
        original_ul = len([e for e in original_root.findall('.//{*}g') if e.get('ctype') == 'x-html-UL'])
        original_li = len([e for e in original_root.findall('.//{*}g') if e.get('ctype') == 'x-html-LI'])

        # Count formatting tags in output
        output_g_tags = len(self.root.findall('.//{*}g'))
        output_ul = len([e for e in self.root.findall('.//{*}g') if e.get('ctype') == 'x-html-UL'])
        output_li = len([e for e in self.root.findall('.//{*}g') if e.get('ctype') == 'x-html-LI'])

        # Count targets
        targets = self.root.findall('.//xliff:target', self.ns)
        targets_with_g = sum(1 for t in targets if len(t.findall('.//{*}g')) > 0)

        stats = {
            'original_g_tags': original_g_tags,
            'output_g_tags': output_g_tags,
            'original_ul': original_ul,
            'output_ul': output_ul,
            'original_li': original_li,
            'output_li': output_li,
            'total_targets': len(targets),
            'targets_with_formatting': targets_with_g,
            'formatting_preserved': output_g_tags >= original_g_tags * 0.95  # Allow 5% variance
        }

        return stats


if __name__ == '__main__':
    print("XLF Writer with HTML Formatting Preservation")
    print("=" * 80)
    print("This module preserves inline <g> tags (bullets, lists, styling)")
    print("when writing transformed text to target elements.")
    print("\nImport this module and use FormattedXLFWriter class.")
