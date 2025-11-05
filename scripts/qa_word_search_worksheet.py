#!/usr/bin/env python3
"""QA validation for word search worksheet using GPT-5 Vision"""

import os
import sys
import base64
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env', override=True)

# OpenAI API configuration
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def encode_image(image_path):
    """Encode image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def qa_validate_worksheet(image_path):
    """Use GPT-5 Vision to validate worksheet quality"""

    print("=" * 70)
    print("GPT-5 VISION QA VALIDATION")
    print("=" * 70)
    print(f"\nAnalyzing: {image_path}\n")

    # Encode image
    base64_image = encode_image(image_path)

    # GPT-5 Vision QA analysis
    try:
        response = client.chat.completions.create(
            model="gpt-5-2025-08-07",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze this 7th grade science word search worksheet for quality assurance.

**Evaluation Criteria:**

1. **Visual Layout & Design** (1-10):
   - Is the template border clean and professional?
   - Is the title "Hunt for Cell Parts!" clearly visible and engaging?
   - Is the grid properly aligned and readable?
   - Are the word list checkboxes clear?
   - Does the design avoid excessive whitespace?

2. **Educational Content** (1-10):
   - Are all 10 cell biology vocabulary words appropriate for 7th grade?
   - Does the content align with NGSS MS-LS1-2 standards?
   - Is the subtitle informative?

3. **Readability** (1-10):
   - Can students easily read the grid letters?
   - Is the word list on the right side legible?
   - Are fonts appropriate sizes?

4. **Print Quality** (1-10):
   - Will this print well on standard 8.5x11 paper?
   - Are all elements within printable margins?
   - Is resolution sufficient?

5. **Overall TPT Marketability** (1-10):
   - Would teachers purchase this on Teachers Pay Teachers?
   - Is it colorful and engaging without being over-the-top?
   - Does it look professional?

**Provide:**
- Numerical scores (1-10) for each category
- Overall grade (A-F)
- Specific issues found (if any)
- Recommendations for improvement
- Final verdict: APPROVED FOR TPT or NEEDS REVISION"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_completion_tokens=1000
        )

        result = response.choices[0].message.content

        print("QA REPORT:")
        print("-" * 70)
        print(result)
        print("-" * 70)

        # Usage info
        print(f"\n[USAGE]")
        print(f"  Prompt tokens: {response.usage.prompt_tokens}")
        print(f"  Completion tokens: {response.usage.completion_tokens}")
        print(f"  Total tokens: {response.usage.total_tokens}")

        return result

    except Exception as e:
        print(f"[ERROR] GPT-5 Vision QA: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python qa_word_search_worksheet.py <worksheet_path>")
        sys.exit(1)

    worksheet_path = sys.argv[1]

    if not os.path.exists(worksheet_path):
        print(f"[ERROR] File not found: {worksheet_path}")
        sys.exit(1)

    qa_result = qa_validate_worksheet(worksheet_path)

    if qa_result:
        print("\n" + "=" * 70)
        print("[SUCCESS] QA validation complete!")
        print("=" * 70)
