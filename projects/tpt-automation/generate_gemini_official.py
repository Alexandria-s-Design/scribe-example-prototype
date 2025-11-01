#!/usr/bin/env python3
"""
Generate TPT Ecosystem Images - CORRECT Google Gemini Implementation
Uses official google-genai library (not google-generativeai)
VERIFIED WORKING
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Install correct library
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Installing google-genai...")
    import subprocess
    subprocess.check_call(['pip', 'install', '-q', 'google-genai'])
    from google import genai
    from google.genai import types

# Configure API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("ERROR: GOOGLE_API_KEY not found")
    exit(1)

os.environ['GEMINI_API_KEY'] = api_key
client = genai.Client()

# Output directory
output_dir = r'C:\Users\MarieLexisDad\projects\tpt-automation\ecosystem-artwork'
os.makedirs(output_dir, exist_ok=True)

print("=" * 80)
print("GENERATING TPT ECOSYSTEM IMAGES - GOOGLE GEMINI 2.5 FLASH IMAGE")
print("=" * 80)
print("Using: Official Google Genai Library")
print()

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
        # Generate image with correct config
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],  # CRITICAL
                image_config=types.ImageConfig(
                    aspect_ratio="1:1"
                )
            )
        )

        # Extract and save image
        for part in response.parts:
            if part.inline_data is not None:
                generated_image = part.as_image()  # Returns PIL Image
                filepath = os.path.join(output_dir, f"{elem_id}.png")
                generated_image.save(filepath)

                # Get file size
                filesize = os.path.getsize(filepath) / 1024
                print(f"SUCCESS: Saved {filepath} ({filesize:.1f} KB)")
                results.append(elem_id)
                break

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
    print("Next steps:")
    print("1. Review images in ecosystem-artwork folder")
    print("2. Insert into Google Slides template")
    print("3. Export as PDF")
    print("4. Upload to TPT at $5-8 (premium AI artwork)")
else:
    print(f"[PARTIAL] Generated {len(results)}/8 images")
