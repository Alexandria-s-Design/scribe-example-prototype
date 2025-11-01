#!/usr/bin/env python3
"""
Generate TPT Ecosystem Images with Gemini Nano Banana - Direct API
Uses requests library for direct OpenRouter API calls
VERIFIED WORKING METHOD
"""

import os
import json
import base64
import re
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.5-flash-image-preview:free"

# Get API key
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("ERROR: OPENROUTER_API_KEY not found")
    exit(1)

# Create output directory
output_dir = r'C:\Users\MarieLexisDad\projects\tpt-automation\ecosystem-artwork'
os.makedirs(output_dir, exist_ok=True)

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

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://alexandriasdesign.com",
        "X-Title": "TPT Generator",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "modalities": ["text", "image"],
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            content_str = str(data.get('choices', [{}])[0].get('message', {}).get('content', ''))

            # Extract base64 image
            matches = re.findall(r'data:image/[^;]+;base64,([A-Za-z0-9+/=]+)', content_str)

            if matches:
                image_data = base64.b64decode(matches[0])
                filepath = os.path.join(output_dir, f"{elem_id}.png")

                with open(filepath, 'wb') as f:
                    f.write(image_data)

                print(f"SAVED: {filepath} ({len(image_data)/1024:.1f} KB)")
                results.append(elem_id)
            else:
                print(f"ERROR: No image in response")
        else:
            print(f"ERROR: {response.text[:200]}")
    except Exception as e:
        print(f"ERROR: {e}")

print(f"\n\nGenerated {len(results)}/8 images successfully!")
print(f"Output: {output_dir}")
