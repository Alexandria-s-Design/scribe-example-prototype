#!/usr/bin/env python3
"""
Generate TPT-Ready Ecosystem Coloring Sheet Artwork - Direct API Version
Uses OpenAI DALL-E 3 directly without helper dependencies
Author: Alexandria's Design
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def generate_ecosystem_artwork():
    """Generate all ecosystem elements as coloring page line art"""

    print("=" * 80)
    print("GENERATING TPT-READY ECOSYSTEM ARTWORK")
    print("=" * 80)
    print("Using OpenAI DALL-E 3 for professional coloring page line art")
    print()

    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found in environment")
        return None

    client = OpenAI(api_key=api_key)

    # Create output directory
    output_dir = r'C:\Users\MarieLexisDad\projects\tpt-automation\ecosystem-artwork'
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}\n")

    # Define ecosystem elements with TPT-optimized prompts
    ecosystem_elements = {
        "oak_tree": {
            "name": "Oak Tree (Producer)",
            "prompt": """Simple black and white line art coloring page drawing of a large oak tree.
            Clean black outlines only, white background, no shading or gray tones.
            Child-friendly style suitable for 3rd grade students.
            Show trunk, branches, leaves, and a few acorns.
            Large clear shapes, easy to color within the lines.
            Professional educational worksheet quality."""
        },
        "deer": {
            "name": "Deer (Consumer)",
            "prompt": """Simple black and white line art coloring page drawing of a deer standing in profile.
            Clean black outlines only, white background, no shading or gray tones.
            Child-friendly style suitable for 3rd grade students.
            Show antlers, ears, legs, and tail clearly.
            Large clear shapes, easy to color within the lines.
            Professional educational worksheet quality."""
        },
        "rabbit": {
            "name": "Rabbit (Consumer)",
            "prompt": """Simple black and white line art coloring page drawing of a cute rabbit sitting.
            Clean black outlines only, white background, no shading or gray tones.
            Child-friendly style suitable for 3rd grade students.
            Show long ears, fluffy tail, and whiskers clearly.
            Large clear shapes, easy to color within the lines.
            Professional educational worksheet quality."""
        },
        "mushrooms": {
            "name": "Mushrooms (Decomposer)",
            "prompt": """Simple black and white line art coloring page drawing of three mushrooms growing together.
            Clean black outlines only, white background, no shading or gray tones.
            Child-friendly style suitable for 3rd grade students.
            Show caps and stems clearly with spots on caps.
            Large clear shapes, easy to color within the lines.
            Professional educational worksheet quality."""
        },
        "sun": {
            "name": "Sun (Energy Source)",
            "prompt": """Simple black and white line art coloring page drawing of a smiling sun.
            Clean black outlines only, white background, no shading or gray tones.
            Child-friendly style suitable for 3rd grade students.
            Show sun rays, happy face with eyes and smile.
            Large clear shapes, easy to color within the lines.
            Professional educational worksheet quality."""
        },
        "rocks": {
            "name": "Rocks",
            "prompt": """Simple black and white line art coloring page drawing of several rocks and pebbles.
            Clean black outlines only, white background, no shading or gray tones.
            Child-friendly style suitable for 3rd grade students.
            Show 3-5 rocks of different sizes grouped together.
            Large clear shapes, easy to color within the lines.
            Professional educational worksheet quality."""
        },
        "pond": {
            "name": "Water/Pond",
            "prompt": """Simple black and white line art coloring page drawing of a small pond with water.
            Clean black outlines only, white background, no shading or gray tones.
            Child-friendly style suitable for 3rd grade students.
            Show wavy water lines, cattails or reeds at edge.
            Large clear shapes, easy to color within the lines.
            Professional educational worksheet quality."""
        },
        "grass_flowers": {
            "name": "Grass and Flowers",
            "prompt": """Simple black and white line art coloring page drawing of grass blades and simple flowers.
            Clean black outlines only, white background, no shading or gray tones.
            Child-friendly style suitable for 3rd grade students.
            Show 3-4 simple flowers with petals and grass blades.
            Large clear shapes, easy to color within the lines.
            Professional educational worksheet quality."""
        }
    }

    # Track results
    results = []
    total_cost = 0

    # Generate each element
    for element_id, element_data in ecosystem_elements.items():
        print(f"\n{'-' * 80}")
        print(f"Generating: {element_data['name']}")
        print(f"{'-' * 80}")
        print(f"Prompt: {element_data['prompt'][:80]}...")

        try:
            # Generate image with DALL-E 3
            print("Calling OpenAI DALL-E 3 API...")
            response = client.images.generate(
                model="dall-e-3",
                prompt=element_data['prompt'],
                size="1024x1024",
                quality="standard",
                n=1
            )

            if response.data and len(response.data) > 0:
                image_url = response.data[0].url
                print(f"SUCCESS: Image generated!")
                print(f"URL: {image_url[:60]}...")

                # Download image
                print("Downloading image...")
                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    filename = f"{element_id}.png"
                    filepath = os.path.join(output_dir, filename)

                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)

                    print(f"SAVED: {filepath}")

                    results.append({
                        'element': element_data['name'],
                        'filename': filename,
                        'filepath': filepath,
                        'url': image_url,
                        'prompt': element_data['prompt']
                    })

                    total_cost += 0.04  # DALL-E 3 standard pricing
                else:
                    print(f"ERROR: Failed to download image (status {img_response.status_code})")
            else:
                print("ERROR: No image URL returned")

        except Exception as e:
            print(f"ERROR: {e}")

    # Save generation report
    print(f"\n{'=' * 80}")
    print("GENERATION COMPLETE")
    print(f"{'=' * 80}")
    print(f"Images generated: {len(results)}/8")
    print(f"Total cost: ${total_cost:.2f}")
    print(f"Output directory: {output_dir}")
    print()

    # Save metadata
    metadata = {
        'generated_at': datetime.now().isoformat(),
        'total_images': len(results),
        'total_cost': total_cost,
        'images': results
    }

    metadata_path = os.path.join(output_dir, 'generation_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"Metadata saved: {metadata_path}")

    # Print summary
    print(f"\n{'=' * 80}")
    print("GENERATED ARTWORK FILES:")
    print(f"{'=' * 80}")
    for result in results:
        print(f"  - {result['filename']}: {result['element']}")

    print(f"\n{'=' * 80}")
    print("NEXT STEPS:")
    print(f"{'=' * 80}")
    print("1. Review images in: " + output_dir)
    print("2. Insert images into Google Slides template")
    print("3. Position and size each image appropriately")
    print("4. Export as PDF for TPT upload")
    print("5. Price at $5-8 (premium with original AI artwork)")
    print()

    return results

if __name__ == '__main__':
    results = generate_ecosystem_artwork()

    if results:
        print(f"\n[SUCCESS] Generated {len(results)} TPT-ready ecosystem images!")
        print("Your coloring sheet now has professional, copyright-free artwork!")
    else:
        print("\n[ERROR] Image generation failed")
