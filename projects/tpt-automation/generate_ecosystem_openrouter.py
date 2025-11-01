#!/usr/bin/env python3
"""
Generate TPT-Ready Ecosystem Coloring Sheet Artwork with OpenRouter
Uses OpenRouter API for image generation (free/low-cost options)
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
    """Generate all ecosystem elements as coloring page line art using OpenRouter"""

    print("=" * 80)
    print("GENERATING TPT-READY ECOSYSTEM ARTWORK WITH OPENROUTER")
    print("=" * 80)
    print("Using OpenRouter for image generation (cost-optimized)")
    print()

    # Initialize OpenRouter client
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not found in environment")
        return None

    # OpenRouter uses OpenAI-compatible API
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://alexandriasdesign.com",
            "X-Title": "TPT Coloring Sheet Generator"
        }
    )

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

    # Try available image generation models on OpenRouter
    # These are known to work with OpenRouter
    image_models = [
        "openai/dall-e-3",  # Best quality, ~$0.04/image
        "openai/dall-e-2",  # Good quality, cheaper
        "stability-ai/stable-diffusion-xl",  # Open source option
    ]

    print("Attempting to connect to OpenRouter image generation...")
    print(f"Will try models: {', '.join(image_models)}")
    print()

    # Track results
    results = []
    total_cost = 0
    model_used = None

    # Generate each element
    for element_id, element_data in ecosystem_elements.items():
        print(f"\n{'-' * 80}")
        print(f"Generating: {element_data['name']}")
        print(f"{'-' * 80}")
        print(f"Prompt: {element_data['prompt'][:80]}...")

        generated = False
        for model in image_models:
            if generated:
                break

            try:
                print(f"Trying model: {model}...")

                # Generate image
                response = client.images.generate(
                    model=model,
                    prompt=element_data['prompt'],
                    size="1024x1024",
                    n=1
                )

                if response.data and len(response.data) > 0:
                    image_url = response.data[0].url
                    print(f"SUCCESS: Image generated with {model}!")
                    print(f"URL: {image_url[:60]}...")

                    if not model_used:
                        model_used = model

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
                            'prompt': element_data['prompt'],
                            'model': model
                        })

                        # Cost estimation (varies by model)
                        if 'dall-e-3' in model:
                            total_cost += 0.04
                        elif 'dall-e-2' in model:
                            total_cost += 0.02
                        else:
                            total_cost += 0.01  # Estimate for other models

                        generated = True
                    else:
                        print(f"ERROR: Failed to download image (status {img_response.status_code})")
                else:
                    print(f"ERROR: No image URL returned from {model}")

            except Exception as e:
                print(f"ERROR with {model}: {e}")
                continue

        if not generated:
            print(f"FAILED: Could not generate {element_data['name']} with any model")

    # Save generation report
    print(f"\n{'=' * 80}")
    print("GENERATION COMPLETE")
    print(f"{'=' * 80}")
    print(f"Images generated: {len(results)}/8")
    print(f"Model used: {model_used}")
    print(f"Estimated cost: ${total_cost:.2f}")
    print(f"Output directory: {output_dir}")
    print()

    # Save metadata
    metadata = {
        'generated_at': datetime.now().isoformat(),
        'total_images': len(results),
        'estimated_cost': total_cost,
        'model_used': model_used,
        'images': results
    }

    metadata_path = os.path.join(output_dir, 'generation_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"Metadata saved: {metadata_path}")

    # Print summary
    if results:
        print(f"\n{'=' * 80}")
        print("GENERATED ARTWORK FILES:")
        print(f"{'=' * 80}")
        for result in results:
            print(f"  - {result['filename']}: {result['element']} (via {result['model']})")

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

    if results and len(results) > 0:
        print(f"\n[SUCCESS] Generated {len(results)} TPT-ready ecosystem images!")
        print("Your coloring sheet now has professional, copyright-free artwork!")
    else:
        print("\n[ERROR] Image generation failed")
        print("\nTroubleshooting:")
        print("1. Check that OPENROUTER_API_KEY is set correctly in .env")
        print("2. Verify OpenRouter account has credits/access")
        print("3. Try alternative: Free clipart or manual drawing in Slides")
