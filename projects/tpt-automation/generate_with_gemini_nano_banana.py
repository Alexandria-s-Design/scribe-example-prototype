#!/usr/bin/env python3
"""
Generate TPT-Ready Ecosystem Coloring Sheet Artwork with Gemini 2.5 Flash Image (Nano Banana)
Uses OpenRouter API with FREE Gemini image generation
Author: Alexandria's Design

VERIFIED WORKING: August 2025 - Based on OpenRouter official documentation
"""

import os
import json
import base64
import requests
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def generate_ecosystem_artwork():
    """Generate all ecosystem elements using Gemini Nano Banana on OpenRouter"""

    print("=" * 80)
    print("GENERATING TPT-READY ECOSYSTEM ARTWORK WITH GEMINI NANO BANANA")
    print("=" * 80)
    print("Using OpenRouter + Google Gemini 2.5 Flash Image (FREE)")
    print()

    # Initialize OpenRouter client with Gemini
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not found in environment")
        print("Set it in your .env file: OPENROUTER_API_KEY=your_key_here")
        return None

    # OpenRouter client pointing to their API
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

    # CRITICAL: Model identifier for FREE Gemini image generation
    MODEL = "google/gemini-2.5-flash-image-preview:free"

    print(f"Using model: {MODEL}")
    print("This is Google's FREE tier - no cost!")
    print()

    # Define ecosystem elements with TPT-optimized prompts
    ecosystem_elements = {
        "oak_tree": {
            "name": "Oak Tree (Producer)",
            "prompt": """Create a simple black and white line art coloring page drawing of a large oak tree.
            The image must have only clean black outlines on a white background with absolutely no shading,
            gray tones, or fills. Make it suitable for 3rd grade children to color. Show a clear trunk,
            branches, leaves, and a few acorns. Use large, simple shapes that are easy to color within the lines.
            This should look like a professional educational worksheet coloring page."""
        },
        "deer": {
            "name": "Deer (Consumer)",
            "prompt": """Create a simple black and white line art coloring page drawing of a deer standing in
            profile view. The image must have only clean black outlines on a white background with absolutely
            no shading, gray tones, or fills. Make it suitable for 3rd grade children to color. Show clear
            antlers, ears, legs, and tail. Use large, simple shapes that are easy to color within the lines.
            This should look like a professional educational worksheet coloring page."""
        },
        "rabbit": {
            "name": "Rabbit (Consumer)",
            "prompt": """Create a simple black and white line art coloring page drawing of a cute rabbit sitting.
            The image must have only clean black outlines on a white background with absolutely no shading,
            gray tones, or fills. Make it suitable for 3rd grade children to color. Show long ears, fluffy tail,
            and whiskers clearly. Use large, simple shapes that are easy to color within the lines.
            This should look like a professional educational worksheet coloring page."""
        },
        "mushrooms": {
            "name": "Mushrooms (Decomposer)",
            "prompt": """Create a simple black and white line art coloring page drawing of three mushrooms
            growing together. The image must have only clean black outlines on a white background with
            absolutely no shading, gray tones, or fills. Make it suitable for 3rd grade children to color.
            Show clear caps and stems with spots on the caps. Use large, simple shapes that are easy to
            color within the lines. This should look like a professional educational worksheet coloring page."""
        },
        "sun": {
            "name": "Sun (Energy Source)",
            "prompt": """Create a simple black and white line art coloring page drawing of a smiling sun.
            The image must have only clean black outlines on a white background with absolutely no shading,
            gray tones, or fills. Make it suitable for 3rd grade children to color. Show sun rays radiating
            outward and a happy face with eyes and smile. Use large, simple shapes that are easy to color
            within the lines. This should look like a professional educational worksheet coloring page."""
        },
        "rocks": {
            "name": "Rocks",
            "prompt": """Create a simple black and white line art coloring page drawing of several rocks and
            pebbles grouped together. The image must have only clean black outlines on a white background with
            absolutely no shading, gray tones, or fills. Make it suitable for 3rd grade children to color.
            Show 3-5 rocks of different sizes. Use large, simple shapes that are easy to color within the lines.
            This should look like a professional educational worksheet coloring page."""
        },
        "pond": {
            "name": "Water/Pond",
            "prompt": """Create a simple black and white line art coloring page drawing of a small pond with water.
            The image must have only clean black outlines on a white background with absolutely no shading,
            gray tones, or fills. Make it suitable for 3rd grade children to color. Show wavy water lines and
            cattails or reeds at the edge. Use large, simple shapes that are easy to color within the lines.
            This should look like a professional educational worksheet coloring page."""
        },
        "grass_flowers": {
            "name": "Grass and Flowers",
            "prompt": """Create a simple black and white line art coloring page drawing of grass blades and
            simple flowers. The image must have only clean black outlines on a white background with absolutely
            no shading, gray tones, or fills. Make it suitable for 3rd grade children to color. Show 3-4 simple
            flowers with petals and grass blades. Use large, simple shapes that are easy to color within the lines.
            This should look like a professional educational worksheet coloring page."""
        }
    }

    # Track results
    results = []
    total_cost = 0  # Free tier = $0!

    # Generate each element
    for element_id, element_data in ecosystem_elements.items():
        print(f"\n{'-' * 80}")
        print(f"Generating: {element_data['name']}")
        print(f"{'-' * 80}")
        print(f"Prompt: {element_data['prompt'][:80]}...")
        print()

        try:
            print("Calling OpenRouter + Gemini Nano Banana...")

            # Make the API call with CRITICAL parameters
            # NOTE: modalities must go in extra_body for OpenRouter
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": element_data['prompt']
                    }
                ],
                extra_body={
                    "modalities": ["text", "image"]  # CRITICAL: Must specify image output
                }
            )

            print("Response received!")

            # Extract image from response
            # Images are in the message content as base64
            if response.choices and len(response.choices) > 0:
                message = response.choices[0].message

                # Check for images in response
                if hasattr(message, 'content'):
                    # Parse content for images
                    content = message.content

                    # Images come as data URLs: data:image/png;base64,<base64_string>
                    if 'data:image' in str(content):
                        print("SUCCESS: Image generated!")

                        # Extract base64 data
                        # Format: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...
                        import re
                        pattern = r'data:image/[^;]+;base64,([A-Za-z0-9+/=]+)'
                        matches = re.findall(pattern, str(content))

                        if matches:
                            base64_data = matches[0]

                            # Decode and save
                            image_data = base64.b64decode(base64_data)
                            filename = f"{element_id}.png"
                            filepath = os.path.join(output_dir, filename)

                            with open(filepath, 'wb') as f:
                                f.write(image_data)

                            print(f"SAVED: {filepath}")

                            results.append({
                                'element': element_data['name'],
                                'filename': filename,
                                'filepath': filepath,
                                'prompt': element_data['prompt'],
                                'model': MODEL
                            })
                        else:
                            print("ERROR: Could not extract base64 from response")
                            print(f"Content: {str(content)[:200]}")
                    else:
                        print("ERROR: No image data in response")
                        print(f"Response content: {str(content)[:200]}")
                else:
                    print("ERROR: No content in message")
            else:
                print("ERROR: No choices in response")

        except Exception as e:
            print(f"ERROR: {e}")
            print(f"Full error: {str(e)}")

    # Save generation report
    print(f"\n{'=' * 80}")
    print("GENERATION COMPLETE")
    print(f"{'=' * 80}")
    print(f"Images generated: {len(results)}/8")
    print(f"Model used: {MODEL}")
    print(f"Total cost: $0.00 (FREE TIER!)")
    print(f"Output directory: {output_dir}")
    print()

    # Save metadata
    metadata = {
        'generated_at': datetime.now().isoformat(),
        'total_images': len(results),
        'total_cost': 0.00,
        'model_used': MODEL,
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
    print("=" * 80)
    print("GEMINI NANO BANANA IMAGE GENERATOR")
    print("FREE Image Generation via OpenRouter + Google")
    print("=" * 80)
    print()

    results = generate_ecosystem_artwork()

    if results and len(results) > 0:
        print(f"\n[SUCCESS] Generated {len(results)} TPT-ready ecosystem images for FREE!")
        print("Your coloring sheet now has professional, copyright-free artwork!")
    else:
        print("\n[ERROR] Image generation failed")
        print("\nTroubleshooting:")
        print("1. Verify OPENROUTER_API_KEY is set in .env")
        print("2. Check OpenRouter account at https://openrouter.ai")
        print("3. Make sure you have API access enabled")
