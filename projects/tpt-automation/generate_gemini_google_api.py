#!/usr/bin/env python3
"""
Generate TPT Ecosystem Images with Google Gemini API (Official)
Uses google-generativeai library for Gemini 2.5 Flash Image
VERIFIED WORKING - Direct Google API
"""

import os
import base64
from dotenv import load_dotenv

load_dotenv()

# Check for google-generativeai library
try:
    import google.generativeai as genai
except ImportError:
    print("Installing google-generativeai...")
    import subprocess
    subprocess.check_call(['pip', 'install', '-q', 'google-generativeai'])
    import google.generativeai as genai

# Configure API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("ERROR: GOOGLE_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)

# Create output directory
output_dir = r'C:\Users\MarieLexisDad\projects\tpt-automation\ecosystem-artwork'
os.makedirs(output_dir, exist_ok=True)

print("=" * 80)
print("GENERATING TPT ECOSYSTEM IMAGES WITH GOOGLE GEMINI")
print("=" * 80)
print("Using: Gemini 2.5 Flash Image (Nano Banana)")
print("Method: Official Google AI API")
print()

# Initialize model
model = genai.GenerativeModel('gemini-2.5-flash-image')

# Ecosystem elements
elements = {
    "oak_tree": "Create a simple black and white line art coloring page of a large oak tree with trunk, branches, leaves, and acorns. Clean black outlines only, white background, no shading. Suitable for 3rd grade coloring.",
    "deer": "Create a simple black and white line art coloring page of a deer in profile. Clean black outlines only, white background, no shading. Show antlers, ears, legs, tail. Suitable for 3rd grade coloring.",
    "rabbit": "Create a simple black and white line art coloring page of a cute sitting rabbit. Clean black outlines only, white background, no shading. Show long ears, fluffy tail, whiskers. Suitable for 3rd grade coloring.",
    "mushrooms": "Create a simple black and white line art coloring page of three mushrooms with caps and stems. Clean black outlines only, white background, no shading. Suitable for 3rd grade coloring.",
    "sun": "Create a simple black and white line art coloring page of a smiling sun with rays. Clean black outlines only, white background, no shading. Suitable for 3rd grade coloring.",
    "rocks": "Create a simple black and white line art coloring page of 3-5 rocks grouped together. Clean black outlines only, white background, no shading. Suitable for 3rd grade coloring.",
    "pond": "Create a simple black and white line art coloring page of a small pond with water and cattails. Clean black outlines only, white background, no shading. Suitable for 3rd grade coloring.",
    "grass_flowers": "Create a simple black and white line art coloring page of grass blades and 3-4 simple flowers. Clean black outlines only, white background, no shading. Suitable for 3rd grade coloring."
}

results = []

for elem_id, prompt in elements.items():
    print(f"\nGenerating: {elem_id}...")

    try:
        # Generate image
        response = model.generate_content(prompt)

        # Check if image was generated
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]

            # Extract image data
            if hasattr(candidate, 'content') and candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, 'inline_data'):
                        # Save image
                        image_data = part.inline_data.data
                        filepath = os.path.join(output_dir, f"{elem_id}.png")

                        with open(filepath, 'wb') as f:
                            f.write(image_data)

                        print(f"SUCCESS: Saved {filepath} ({len(image_data)/1024:.1f} KB)")
                        results.append(elem_id)
                        break
            else:
                print(f"No image in response")
        else:
            print(f"No candidates in response")

    except Exception as e:
        print(f"ERROR: {e}")

print(f"\n\n{'=' * 80}")
print(f"GENERATION COMPLETE")
print(f"{'=' * 80}")
print(f"Generated: {len(results)}/8 images")
print(f"Output: {output_dir}")
print()

if len(results) == 8:
    print("[SUCCESS] All 8 TPT-ready ecosystem images generated!")
    print("Next: Insert into Google Slides and export as PDF")
else:
    print(f"[PARTIAL] Generated {len(results)}/8 images")
