"""
MPP Transformation Engine
=========================
Applies all transformation rules from MPP SOP for eLearning course content.
Transforms content from Mentor/Protégé perspective to Program Manager perspective.

Author: Alexandria's Design
Purpose: Automated MPP course transformation
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class TransformationContext:
    """
    Tracks state across entire course transformation.

    Attributes:
        acronym_first_mentions: Set of acronyms already defined
        unit_number: Current unit being processed
        lesson_number: Current lesson being processed
        notes_positions: Tracks note markers and their positions
        total_source_length: Character count of source text
        total_target_length: Character count of transformed text
    """
    acronym_first_mentions: set = field(default_factory=set)
    unit_number: int = 1
    lesson_number: int = 1
    notes_positions: List[Tuple[int, str]] = field(default_factory=list)
    total_source_length: int = 0
    total_target_length: int = 0

    def reset_for_new_unit(self, unit_num: int):
        """Reset lesson counter when starting a new unit."""
        self.unit_number = unit_num
        self.lesson_number = 1

    def increment_lesson(self):
        """Move to next lesson."""
        self.lesson_number += 1

    def track_length(self, source: str, target: str):
        """Track character counts for length comparison."""
        self.total_source_length += len(source)
        self.total_target_length += len(target)

    def get_length_ratio(self) -> float:
        """Calculate target/source length ratio."""
        if self.total_source_length == 0:
            return 0.0
        return (self.total_target_length / self.total_source_length) * 100


# ==============================================================================
# RULE 1: CAPITALIZATION TRANSFORMATIONS
# ==============================================================================

def fix_capitalization(text: str) -> str:
    """
    Apply MPP capitalization rules.

    Rules:
    - Mentor/Mentors → always capitalize M
    - Protégé/Protégés → always capitalize P (with or without accent)
    - "Federal Government" → keep capitalized
    - "federal" (all other uses) → lowercase

    Args:
        text: Input text to transform

    Returns:
        Text with corrected capitalization
    """
    # Fix Mentor (case-insensitive)
    text = re.sub(r'\bmentor\b', 'Mentor', text, flags=re.IGNORECASE)
    text = re.sub(r'\bmentors\b', 'Mentors', text, flags=re.IGNORECASE)

    # Fix Protégé with accent (case-insensitive)
    text = re.sub(r'\bprotégé\b', 'Protégé', text, flags=re.IGNORECASE)
    text = re.sub(r'\bprotégés\b', 'Protégés', text, flags=re.IGNORECASE)

    # Fix Protege without accent (case-insensitive)
    text = re.sub(r'\bprotege\b', 'Protégé', text, flags=re.IGNORECASE)
    text = re.sub(r'\bproteges\b', 'Protégés', text, flags=re.IGNORECASE)

    # Fix Federal Government (should be capitalized)
    text = re.sub(
        r'\bfederal\s+government\b',
        'Federal Government',
        text,
        flags=re.IGNORECASE
    )

    # Fix standalone "federal" to lowercase (unless at start of sentence)
    # This regex looks for "federal" not followed by "Government"
    text = re.sub(
        r'(?<!^)(?<!\. )\bFederal\b(?!\s+Government)',
        'federal',
        text
    )

    return text


# ==============================================================================
# RULE 2: ACRONYM TRANSFORMATIONS
# ==============================================================================

# Acronym definitions with their full forms
ACRONYMS = {
    'PMs': 'Program Managers',
    'PM': 'Program Manager',
    'DoD': 'Department of Defense',
    'OSBP': 'Office of Small Business Programs',
    'DFARS': 'Defense Federal Acquisition Regulation Supplement',
    'MPP': 'Mentor-Protégé Program',
    'SAM': 'System for Award Management',
    'CPARS': 'Contractor Performance Assessment Reporting System',
    'SBA': 'Small Business Administration',
    'FAR': 'Federal Acquisition Regulation',
    'NAICS': 'North American Industry Classification System',
    'CO': 'Contracting Officer',
    'COR': 'Contracting Officer Representative',
    'SBIR': 'Small Business Innovation Research',
    'STTR': 'Small Business Technology Transfer',
    'HUBZone': 'Historically Underutilized Business Zone',
    'WOSB': 'Women-Owned Small Business',
    'EDWOSB': 'Economically Disadvantaged Women-Owned Small Business',
    'VOSB': 'Veteran-Owned Small Business',
    'SDVOSB': 'Service-Disabled Veteran-Owned Small Business',
    '8(a)': '8(a) Business Development Program'
}


def handle_acronyms(text: str, context: TransformationContext) -> str:
    """
    Handle first mention of acronyms with full expansion.

    On first mention: "Program Managers (PMs)"
    Subsequent mentions: "PMs"

    Tracks acronyms across entire course (not per unit).

    Args:
        text: Input text to transform
        context: Transformation context with acronym tracking

    Returns:
        Text with properly formatted acronyms
    """
    result = text

    # Process each acronym
    for acronym, full_form in ACRONYMS.items():
        # Escape special regex characters in acronym
        escaped_acronym = re.escape(acronym)

        # Check if acronym is already expanded in the text (e.g., "Program Manager (PM)")
        expanded_form = f"{full_form} ({acronym})"
        if expanded_form in result:
            # Already expanded, just mark as mentioned
            context.acronym_first_mentions.add(acronym)
            continue

        # Check if this is the first mention in the entire course
        if acronym not in context.acronym_first_mentions:
            # Look for first occurrence of the acronym (standalone)
            pattern = r'\b' + escaped_acronym + r'\b'
            match = re.search(pattern, result)

            if match:
                # Mark as mentioned
                context.acronym_first_mentions.add(acronym)

                # Replace first occurrence with full form + acronym
                replacement = f"{full_form} ({acronym})"
                result = re.sub(
                    pattern,
                    replacement,
                    result,
                    count=1  # Only first occurrence
                )

        # For subsequent mentions, just use acronym
        # (This handles cases where full form might appear in text)
        # Only replace if we've already introduced the acronym
        if acronym in context.acronym_first_mentions:
            # Replace "Program Managers" with "PMs" (if already introduced)
            # But NOT if it's part of the expanded form we just created
            result = re.sub(
                r'\b' + re.escape(full_form) + r'\b(?!\s*\(' + escaped_acronym + r'\))',
                acronym,
                result
            )

    return result


# ==============================================================================
# RULE 3: PERSPECTIVE CORRECTION (Mentor/Protégé → Program Manager POV)
# ==============================================================================

# Perspective transformation patterns
PERSPECTIVE_PATTERNS = [
    # Pattern 1: "As a Mentor, you..." → "Program Managers oversee Mentors who..."
    (
        r'As a Mentor,?\s+you\s+',
        'Program Managers oversee Mentors who '
    ),

    # Pattern 2: "Your Protégé" → "The Protégé"
    (
        r'\bYour\s+Protégé',
        'The Protégé'
    ),
    (
        r'\byour\s+Protégé',
        'the Protégé'
    ),

    # Pattern 3: "As a Protégé, you..." → "Protégés are expected to..."
    (
        r'As a Protégé,?\s+you\s+',
        'Protégés are expected to '
    ),

    # Pattern 4: "You should" (when addressing Mentor/Protégé) → "Mentors should" or "Protégés should"
    # This requires context - we'll handle generically
    (
        r'\bYou should\s+',
        'Participants should '
    ),
    (
        r'\byou should\s+',
        'participants should '
    ),

    # Pattern 5: "You will" → "Participants will" or "They will"
    (
        r'\bYou will\s+',
        'Participants will '
    ),
    (
        r'\byou will\s+',
        'participants will '
    ),

    # Pattern 6: "You must" → "Participants must"
    (
        r'\bYou must\s+',
        'Participants must '
    ),
    (
        r'\byou must\s+',
        'participants must '
    ),

    # Pattern 7: "You can" → "Participants can"
    (
        r'\bYou can\s+',
        'Participants can '
    ),
    (
        r'\byou can\s+',
        'participants can '
    ),

    # Pattern 8: "Your organization" → "The organization"
    (
        r'\bYour organization',
        'The organization'
    ),
    (
        r'\byour organization',
        'the organization'
    ),

    # Pattern 9: "Your role" → "The Mentor's role" or "The Protégé's role"
    (
        r'\bYour role',
        'The participant\'s role'
    ),
    (
        r'\byour role',
        'the participant\'s role'
    ),
]


def is_pm_learner_context(text: str) -> bool:
    """
    Detect if text is addressing PM learners directly (should NOT be converted).

    PM learner contexts include:
    - Learning objectives: "By the end of this lesson, you will..."
    - Direct PM instruction: "As a PM, you..." or "As a Program Manager, you..."
    - PM oversight language: "your oversight", "your responsibility as PM"
    - Course navigation: "you will learn", "you will be able to"

    Args:
        text: Input text to check

    Returns:
        True if text is addressing PM learners (should stay as-is)
    """
    pm_learner_patterns = [
        r'\bBy the end of this\b',
        r'\bBy the end of the\b',
        r'\bIn this (lesson|module|unit)\b',
        r'\bAs a (PM|Program Manager)\b',
        r'\byour oversight\b',
        r'\byour responsibility as (a )?(PM|Program Manager)\b',
        r'\byou will learn\b',
        r'\byou will be able to\b',
        r'\byou will understand\b',
        r'\byou will know\b',
        r'\byou will identify\b',
        r'\byou will explain\b',
        r'\byou will apply\b',
        r'\bwelcome to\b.*\bcourse\b',
        r'\bThis (lesson|module|unit) (will|is designed to)\b'
    ]

    for pattern in pm_learner_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


def convert_perspective(text: str, context: TransformationContext) -> str:
    """
    Convert from Mentor/Protégé perspective to Program Manager perspective.

    Removes first-person language directed at Mentors/Protégés.
    Adds Program Manager context where needed.

    IMPORTANT: Preserves PM learner instructional language.
    Does NOT convert "you/your" when addressing PM learners.

    Args:
        text: Input text to transform
        context: Transformation context

    Returns:
        Text converted to Program Manager perspective
    """
    # Check if this is PM learner instructional content
    if is_pm_learner_context(text):
        # Don't convert - this is addressed to PM learners
        return text

    result = text

    # Apply all perspective transformation patterns
    for pattern, replacement in PERSPECTIVE_PATTERNS:
        result = re.sub(pattern, replacement, result)

    # Additional contextual transformations
    # If text starts with a direct instruction, add PM context
    if result.startswith(('Complete', 'Submit', 'Ensure', 'Verify')):
        result = f"Program Managers should verify that participants {result[0].lower()}{result[1:]}"

    return result


# ==============================================================================
# RULE 4: eLEARNING SOP COMPLIANCE
# ==============================================================================

def convert_bullets_to_sentences(text: str) -> str:
    """
    Convert bullet points to complete sentences per eLearning SOP.

    Rules:
    - Capitalize first word
    - Add period at end if missing
    - Maintain parallel structure
    - Use numbered lists for procedures

    Args:
        text: Input text with bullet points

    Returns:
        Text with properly formatted sentences
    """
    result = text

    # Split into lines
    lines = result.split('\n')
    processed_lines = []

    for line in lines:
        # Check if line is a bullet point
        bullet_match = re.match(r'^(\s*)([-*•])\s+(.+)$', line)

        if bullet_match:
            indent = bullet_match.group(1)
            bullet = bullet_match.group(2)
            content = bullet_match.group(3).strip()

            # Capitalize first word
            if content:
                content = content[0].upper() + content[1:]

            # Add period if missing (and not already ending with punctuation)
            if content and not content[-1] in '.!?':
                content += '.'

            # Reconstruct line
            processed_line = f"{indent}{bullet} {content}"
            processed_lines.append(processed_line)
        else:
            # Not a bullet point, keep as-is
            processed_lines.append(line)

    return '\n'.join(processed_lines)


def convert_to_numbered_list(text: str, is_procedure: bool = False) -> str:
    """
    Convert bullet points to numbered list for procedures.

    Args:
        text: Input text with bullet points
        is_procedure: True if this is a procedural list

    Returns:
        Text with numbered list (if procedure)
    """
    if not is_procedure:
        return text

    lines = text.split('\n')
    processed_lines = []
    counter = 1

    for line in lines:
        # Check if line is a bullet point
        bullet_match = re.match(r'^(\s*)([-*•])\s+(.+)$', line)

        if bullet_match:
            indent = bullet_match.group(1)
            content = bullet_match.group(3).strip()

            # Replace bullet with number
            processed_line = f"{indent}{counter}. {content}"
            processed_lines.append(processed_line)
            counter += 1
        else:
            # Not a bullet point, keep as-is
            processed_lines.append(line)

    return '\n'.join(processed_lines)


# ==============================================================================
# RULE 5: NOTES PRESERVATION
# ==============================================================================

def extract_notes(text: str) -> Tuple[str, List[Tuple[int, str]]]:
    """
    Extract notes marked with ******* and preserve their positions.

    Args:
        text: Input text with notes

    Returns:
        Tuple of (text without notes, list of (position, note_content))
    """
    notes = []

    # Find all notes (text surrounded by *******)
    note_pattern = r'(\*{7,}.*?\*{7,})'

    # Find all matches with their positions
    for match in re.finditer(note_pattern, text, re.DOTALL):
        position = match.start()
        note_content = match.group(1)
        notes.append((position, note_content))

    # Remove notes from text temporarily
    text_without_notes = re.sub(note_pattern, '<<<NOTE_PLACEHOLDER>>>', text, flags=re.DOTALL)

    return text_without_notes, notes


def reinsert_notes(text: str, notes: List[Tuple[int, str]]) -> str:
    """
    Reinsert notes at their original positions (relative).

    Args:
        text: Transformed text with note placeholders
        notes: List of (original_position, note_content)

    Returns:
        Text with notes reinserted
    """
    result = text

    # Replace placeholders with actual notes
    for position, note_content in notes:
        result = result.replace('<<<NOTE_PLACEHOLDER>>>', note_content, 1)

    return result


# ==============================================================================
# MAIN TRANSFORMATION ENGINE
# ==============================================================================

def apply_all_transformations(
    text: str,
    context: TransformationContext,
    is_procedure: bool = False
) -> str:
    """
    Apply all MPP transformation rules to input text.

    Transformation order:
    1. Extract and preserve notes
    2. Fix capitalization
    3. Handle acronyms (with course-wide tracking)
    4. Convert perspective (Mentor/Protégé → PM)
    5. Apply eLearning SOP (bullets → sentences)
    6. Reinsert notes at original positions
    7. Track length for quality control

    Args:
        text: Source text to transform
        context: Transformation context (tracks state across course)
        is_procedure: True if text contains procedural steps (use numbered list)

    Returns:
        Fully transformed text
    """
    # Track original length
    original_length = len(text)

    # STEP 1: Extract notes
    text_without_notes, notes = extract_notes(text)

    # STEP 2: Fix capitalization
    text_without_notes = fix_capitalization(text_without_notes)

    # STEP 3: Handle acronyms (course-wide tracking)
    text_without_notes = handle_acronyms(text_without_notes, context)

    # STEP 4: Convert perspective
    text_without_notes = convert_perspective(text_without_notes, context)

    # STEP 5: Apply eLearning SOP
    text_without_notes = convert_bullets_to_sentences(text_without_notes)

    if is_procedure:
        text_without_notes = convert_to_numbered_list(text_without_notes, is_procedure=True)

    # STEP 6: Reinsert notes
    result = reinsert_notes(text_without_notes, notes)

    # STEP 7: Track length
    context.track_length(text, result)

    return result


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def transform_file(
    source_text: str,
    unit_number: int = 1,
    is_procedure: bool = False,
    context: Optional[TransformationContext] = None
) -> Tuple[str, TransformationContext]:
    """
    Transform an entire file (unit or lesson).

    Args:
        source_text: Source text to transform
        unit_number: Current unit number
        is_procedure: True if text contains procedural steps
        context: Existing context (or None to create new)

    Returns:
        Tuple of (transformed text, updated context)
    """
    if context is None:
        context = TransformationContext()

    context.reset_for_new_unit(unit_number)

    transformed = apply_all_transformations(
        source_text,
        context,
        is_procedure=is_procedure
    )

    return transformed, context


def get_transformation_report(context: TransformationContext) -> str:
    """
    Generate a transformation report with statistics.

    Args:
        context: Transformation context with tracking data

    Returns:
        Formatted report string
    """
    length_ratio = context.get_length_ratio()

    report = f"""
MPP TRANSFORMATION REPORT
========================

Source Text Length:  {context.total_source_length:,} characters
Target Text Length:  {context.total_target_length:,} characters
Length Ratio:        {length_ratio:.1f}%
Target Range:        90-95% (accuracy prioritized)

Acronyms Introduced: {len(context.acronym_first_mentions)}
Acronyms:            {', '.join(sorted(context.acronym_first_mentions))}

Units Processed:     {context.unit_number}
Lessons Processed:   {context.lesson_number}

Status: {'✓ COMPLETE' if length_ratio >= 90 and length_ratio <= 105 else '⚠ REVIEW LENGTH'}
"""

    return report


# ==============================================================================
# EXAMPLE USAGE
# ==============================================================================

if __name__ == "__main__":
    # Example usage
    context = TransformationContext()

    example_text = """
    As a Mentor, you should ensure your protege understands the mentor-protege program.

    Your role includes:
    - Working with the federal government
    - Supporting your Protégé's development
    - Ensuring compliance with DFARS and DoD requirements

    *******
    Note: This is an important reminder about program managers and their oversight.
    *******

    You must submit reports to the OSBP regularly.
    """

    print("ORIGINAL TEXT:")
    print("=" * 80)
    print(example_text)
    print("\n" * 2)

    transformed = apply_all_transformations(example_text, context)

    print("TRANSFORMED TEXT:")
    print("=" * 80)
    print(transformed)
    print("\n" * 2)

    print(get_transformation_report(context))
