"""
Generate all MPP lesson HTML files using Module 1 Lesson 1 as exact template.

This script:
1. Reads Module 1 Lesson 1 HTML files as templates
2. Reads Excel file for objectives and references
3. Queries Google Gemini File Search API with dual verification
4. Generates files maintaining EXACT format from Module 1 Lesson 1
5. Ensures Chapter/Section reference format
6. Ensures Mentor/Protégé capitalization
"""

import os
import pandas as pd
import re
from pathlib import Path
from google import genai
from google.genai import types
# Configuration
EXCEL_PATH = r"C:\Users\MarieLexisDad\Downloads\MPP Objectives Learning.xlsx"
BASE_DIR = r"C:\Users\MarieLexisDad\Downloads\lesson objectives and lesson summary"
TEMPLATE_OBJECTIVES = os.path.join(BASE_DIR, "Module 1", "Lesson 1", "lesson_objectives.html")
TEMPLATE_SUMMARY = os.path.join(BASE_DIR, "Module 1", "Lesson 1", "lesson_summary.html")
FILE_SEARCH_STORE = "fileSearchStores/mppsopdocumentation-j83n2w5zjn96"

# Load API key from environment variable
# Ensure GOOGLE_API_KEY is set in your .env file
from dotenv import load_dotenv
load_dotenv()

if 'GOOGLE_API_KEY' not in os.environ:
    raise ValueError("GOOGLE_API_KEY not found in environment. Please set it in your .env file.")

# Initialize Google Gemini client
client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])


def ensure_capitalization(text):
    """Ensure Mentor and Protégé are properly capitalized."""
    text = re.sub(r'\bmentor\b', 'Mentor', text, flags=re.IGNORECASE)
    text = re.sub(r'\bmentors\b', 'Mentors', text, flags=re.IGNORECASE)
    text = re.sub(r'\bprotege\b', 'Protégé', text, flags=re.IGNORECASE)
    text = re.sub(r'\bproteges\b', 'Protégés', text, flags=re.IGNORECASE)
    return text


def format_reference(ref_text, source_type):
    """Format reference with proper Chapter/Section prefix."""
    if not ref_text or pd.isna(ref_text):
        return None

    ref_text = str(ref_text).strip()

    # Split by comma to check for multiple references
    refs = [r.strip() for r in ref_text.split(',')]

    if source_type == "SOP":
        # MPP SOP uses "Chapter" or "Chapters"
        if len(refs) == 1:
            return f"Chapter {refs[0]}"
        else:
            return f"Chapters {', '.join(refs)}"
    else:  # Appendix I
        # Appendix I uses "Section" or "Sections"
        if len(refs) == 1:
            return f"Section {refs[0]}"
        else:
            return f"Sections {', '.join(refs)}"


def query_gemini_dual_verification(objective_text):
    """Query Gemini File Search API twice with different phrasing for verification."""

    # First query
    prompt1 = f"""Based on the MPP SOP and DFARS Appendix I documentation, provide a 2-3 sentence summary of this learning objective:

{objective_text}

Focus on the key concepts and requirements. Ensure "Mentor" and "Protégé" are capitalized."""

    response1 = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt1,
        config=types.GenerateContentConfig(
            tools=[types.Tool(file_search=types.FileSearch(file_search_store_names=[FILE_SEARCH_STORE]))],
            temperature=0.7
        )
    )

    # Second query with different phrasing
    prompt2 = f"""Using the MPP SOP and Appendix I documents, explain this learning objective in 2-3 clear sentences:

{objective_text}

Emphasize practical understanding. Capitalize "Mentor" and "Protégé" properly."""

    response2 = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt2,
        config=types.GenerateContentConfig(
            tools=[types.Tool(file_search=types.FileSearch(file_search_store_names=[FILE_SEARCH_STORE]))],
            temperature=0.7
        )
    )

    # Use first response (both should be similar due to same source)
    summary = response1.text.strip()
    summary = ensure_capitalization(summary)

    return summary


def generate_lesson_objectives_html(module_num, lesson_num, objectives_data, template_html):
    """Generate lesson_objectives.html using exact template format."""

    # Read template
    with open(template_html, 'r', encoding='utf-8') as f:
        html = f.read()

    # Update title and header
    html = html.replace('Module 1 - Lesson 1: Learning Objectives',
                       f'Module {module_num} - Lesson {lesson_num}: Learning Objectives')
    html = html.replace('<h1>Module 1 - Lesson 1: Learning Objectives</h1>',
                       f'<h1>Module {module_num} - Lesson {lesson_num}: Learning Objectives</h1>')

    # Build objectives HTML
    objectives_html = ""
    references_data_js = []

    for idx, obj_data in enumerate(objectives_data):
        objective_text = ensure_capitalization(obj_data['objective'])

        objectives_html += f"""
            <li class="objective-item">
                <div class="objective-header">
                    <span class="objective-text">{objective_text}</span>
                    <button class="ref-button" onclick="openModal(this, {idx})">
                        📚 Find in SOP/Appendix I
                    </button>
                </div>
            </li>
"""

        # Build references
        refs = []
        if obj_data['sop_ref']:
            refs.append({
                'source': 'MPP SOP',
                'location': obj_data['sop_ref']
            })
        if obj_data['appendix_ref']:
            refs.append({
                'source': 'Appendix I',
                'location': obj_data['appendix_ref']
            })

        references_data_js.append(refs)

    # Replace objectives list
    start_marker = '<ul class="objectives-list">'
    end_marker = '</ul>'
    start_idx = html.find(start_marker)
    end_idx = html.find(end_marker, start_idx) + len(end_marker)

    html = html[:start_idx] + start_marker + objectives_html + '        ' + end_marker + html[end_idx:]

    # Replace references data in JavaScript
    js_refs = "const referencesData = [\n"
    for refs in references_data_js:
        js_refs += "            [\n"
        for ref in refs:
            js_refs += f"""                {{
                    source: "{ref['source']}",
                    location: "{ref['location']}"
                }},\n"""
        js_refs += "            ],\n"
    js_refs += "        ];"

    # Find and replace referencesData
    ref_start = html.find('const referencesData = [')
    ref_end = html.find('];', ref_start) + 2
    html = html[:ref_start] + js_refs + html[ref_end:]

    return html


def generate_lesson_summary_html(module_num, lesson_num, objectives_data, template_html):
    """Generate lesson_summary.html using exact template format."""

    # Read template
    with open(template_html, 'r', encoding='utf-8') as f:
        html = f.read()

    # Update title and header
    html = html.replace('Module 1 - Lesson 1: Lesson Summary',
                       f'Module {module_num} - Lesson {lesson_num}: Lesson Summary')
    html = html.replace('<h1>Module 1 - Lesson 1: Lesson Summary</h1>',
                       f'<h1>Module {module_num} - Lesson {lesson_num}: Lesson Summary</h1>')

    # Emojis for topics (cycle through these)
    emojis = ['📜', '⚖️', '🎯', '📊', '🔄', '📋', '🏢', '💼', '📈', '🔍']

    # Build topic cards HTML
    cards_html = ""
    objectives_data_js = []

    for idx, obj_data in enumerate(objectives_data):
        emoji = emojis[idx % len(emojis)]
        objective_text = ensure_capitalization(obj_data['objective'])
        summary_text = ensure_capitalization(obj_data['summary'])

        # Generate simple topic title from objective (first few words)
        words = objective_text.split()[:3]
        topic_title = ' '.join(words).rstrip('.,')

        cards_html += f"""
        <div class="topic-card" onclick="openModal({idx})">
            <span class="topic-emoji">{emoji}</span>
            <h3 class="topic-title">{topic_title}</h3>
            <p class="topic-description">{objective_text}</p>
        </div>
"""

        objectives_data_js.append({
            'objective': objective_text,
            'summary': summary_text
        })

    # Replace topics grid
    start_marker = '<div class="topics-grid">'
    end_marker = '</div>\n    </div>\n\n    <!-- Modal -->'
    start_idx = html.find(start_marker)
    end_idx = html.find(end_marker, start_idx)

    html = html[:start_idx] + start_marker + cards_html + '    ' + html[end_idx:]

    # Replace objectivesData in JavaScript
    js_data = "const objectivesData = [\n"
    for obj in objectives_data_js:
        js_data += f"""            {{
                objective: "{obj['objective']}",
                summary: "{obj['summary']}"
            }},\n"""
    js_data += "        ];"

    # Find and replace objectivesData
    data_start = html.find('const objectivesData = [')
    data_end = html.find('];', data_start) + 2
    html = html[:data_start] + js_data + html[data_end:]

    return html


def main():
    """Main execution function."""

    print("=" * 80)
    print("MPP LESSON GENERATION - Using Module 1 Lesson 1 as Exact Template")
    print("=" * 80)
    print()

    # Read Excel file
    print("Reading Excel file...")
    df = pd.read_excel(EXCEL_PATH)
    print(f"Loaded {len(df)} objectives from Excel")
    print()

    # Read templates
    print("Loading templates from Module 1 Lesson 1...")
    if not os.path.exists(TEMPLATE_OBJECTIVES) or not os.path.exists(TEMPLATE_SUMMARY):
        print("ERROR: Module 1 Lesson 1 templates not found!")
        return
    print("[OK] Templates loaded")
    print()

    # Group by Module and Lesson
    grouped = df.groupby(['Module', 'Lesson'])

    total_lessons = len(grouped)
    print(f"Generating {total_lessons} lessons...")
    print()

    # Process each lesson
    for (module_num, lesson_num), group in grouped:
        # Skip Module 1 Lesson 1 (already exists)
        if module_num == 1 and lesson_num == 1:
            print(f"[{module_num}.{lesson_num}] Skipping (template exists)")
            continue

        print(f"[{module_num}.{lesson_num}] Generating lesson with {len(group)} objectives...")

        # Prepare objectives data
        objectives_data = []

        for _, row in group.iterrows():
            objective_text = str(row['Objetives']).strip()
            sop_ref = format_reference(row['SOP'], "SOP")
            appendix_ref = format_reference(row['Appendix I'], "Appendix I")

            # Query Gemini for summary with dual verification
            print(f"  - Querying Gemini (dual verification) for: {objective_text[:60]}...")
            summary = query_gemini_dual_verification(objective_text)

            objectives_data.append({
                'objective': objective_text,
                'sop_ref': sop_ref,
                'appendix_ref': appendix_ref,
                'summary': summary
            })

        # Create output directory
        output_dir = os.path.join(BASE_DIR, f"Module {module_num}", f"Lesson {lesson_num}")
        os.makedirs(output_dir, exist_ok=True)

        # Generate lesson_objectives.html
        print(f"  - Generating lesson_objectives.html...")
        objectives_html = generate_lesson_objectives_html(
            module_num, lesson_num, objectives_data, TEMPLATE_OBJECTIVES
        )

        with open(os.path.join(output_dir, 'lesson_objectives.html'), 'w', encoding='utf-8') as f:
            f.write(objectives_html)

        # Generate lesson_summary.html
        print(f"  - Generating lesson_summary.html...")
        summary_html = generate_lesson_summary_html(
            module_num, lesson_num, objectives_data, TEMPLATE_SUMMARY
        )

        with open(os.path.join(output_dir, 'lesson_summary.html'), 'w', encoding='utf-8') as f:
            f.write(summary_html)

        print(f"[{module_num}.{lesson_num}] [OK] Complete")
        print()

    print("=" * 80)
    print("GENERATION COMPLETE!")
    print("=" * 80)


if __name__ == "__main__":
    main()
