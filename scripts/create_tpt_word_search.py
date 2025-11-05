#!/usr/bin/env python3
"""Create TPT Word Search Worksheet with Template Border"""

import os
import sys
import requests
import base64
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from generate_word_search import WordSearchGenerator

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env', override=True)

# Configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
TEMPLATE_PATH = r"C:\Users\MarieLexisDad\Downloads\template.jpg"
OUTPUT_DIR = Path(r"C:\Users\MarieLexisDad\projects\tpt-automation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Word search configuration
CELL_BIOLOGY_WORDS = [
    'NUCLEUS', 'MITOCHONDRIA', 'CHLOROPLAST', 'MEMBRANE',
    'CYTOPLASM', 'RIBOSOME', 'VACUOLE', 'ORGANELLE',
    'CELLWALL', 'DIFFUSION'
]

def generate_cell_illustration():
    """Generate small cell diagram using Nano Banana"""
    print("[1/5] Generating cell illustration with Nano Banana...")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://alexandriasdesign.com",
        "X-Title": "TPT Cell Biology Word Search"
    }

    prompt = """Create a colorful, simplified diagram of a plant cell for 7th grade students.
    Include labeled parts: nucleus, mitochondria, chloroplast, cell membrane, cell wall, vacuole.
    Style: Bright colors, clean cartoon style, educational, clear labels.
    Size: Small icon suitable for worksheet corner (approx 300x300px).
    Background: Transparent or white."""

    payload = {
        "model": "google/gemini-2.5-flash-image",
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image", "text"]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)

        if response.status_code == 200:
            result = response.json()
            images = result['choices'][0]['message'].get('images', [])

            if images:
                img_data = images[0]

                # Handle nested structure
                if isinstance(img_data, dict):
                    if 'image_url' in img_data:
                        img_url = img_data['image_url'].get('url', '')
                    else:
                        img_url = img_data.get('url', '')

                    if img_url and img_url.startswith('data:image'):
                        base64_data = img_url.split(',')[1]
                        img_bytes = base64.b64decode(base64_data)

                        # Save cell illustration
                        cell_img_path = OUTPUT_DIR / "cell_illustration_temp.png"
                        with open(cell_img_path, 'wb') as f:
                            f.write(img_bytes)

                        print(f"   [OK] Cell illustration saved: {cell_img_path}")
                        return str(cell_img_path)

        print("   [ERROR] Failed to generate cell illustration")
        return None

    except Exception as e:
        print(f"   [ERROR] {e}")
        return None

def create_word_search_worksheet():
    """Create complete word search worksheet"""
    print("[2/5] Generating word search grid...")

    # Generate word search
    generator = WordSearchGenerator(size=15)
    grid, placed_words = generator.generate(CELL_BIOLOGY_WORDS)

    print(f"   [OK] Placed {len(placed_words)} words in grid")

    # Load template
    print("[3/5] Loading template border...")
    template = Image.open(TEMPLATE_PATH)
    template = template.convert('RGB')

    # Get template dimensions
    width, height = template.size
    print(f"   [OK] Template size: {width}x{height}")

    # Create drawing context
    draw = ImageDraw.Draw(template)

    # Define fonts - LARGER SIZES per best practices
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 48)  # Bigger, bold title
        grid_font = ImageFont.truetype("arialbd.ttf", 26)   # MUCH bigger grid font (was 18)
        word_font = ImageFont.truetype("arial.ttf", 20)     # Bigger word list
        small_font = ImageFont.truetype("arial.ttf", 12)    # Slightly bigger NGSS text
    except:
        title_font = ImageFont.load_default()
        grid_font = ImageFont.load_default()
        word_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    print("[4/5] Composing worksheet elements...")

    # Title - higher up to maximize space
    title = "Hunt for Cell Parts!"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 80), title, fill='#2E86AB', font=title_font)

    # Subtitle
    subtitle = "7th Grade Science - Cell Structure & Function"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=word_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, 140), subtitle, fill='#555555', font=word_font)

    # Word search grid - MUCH BIGGER cells
    grid_start_x = 120
    grid_start_y = 200
    cell_size = 38  # Increased from 25 to 38 for better readability

    # Draw grid
    for i, row in enumerate(grid):
        for j, letter in enumerate(row):
            x = grid_start_x + j * cell_size
            y = grid_start_y + i * cell_size

            # Draw cell border
            draw.rectangle([x, y, x + cell_size, y + cell_size], outline='#CCCCCC')

            # Draw letter (centered)
            letter_bbox = draw.textbbox((0, 0), letter, font=grid_font)
            letter_width = letter_bbox[2] - letter_bbox[0]
            letter_height = letter_bbox[3] - letter_bbox[1]

            text_x = x + (cell_size - letter_width) // 2
            text_y = y + (cell_size - letter_height) // 2

            draw.text((text_x, text_y), letter, fill='#000000', font=grid_font)

    # Word list (right side) - adjusted for bigger grid
    word_list_x = grid_start_x + 15 * cell_size + 60
    word_list_y = 230

    draw.text((word_list_x, word_list_y - 30), "Find these words:", fill='#333333', font=word_font)

    for i, word in enumerate(CELL_BIOLOGY_WORDS):
        y_pos = word_list_y + i * 35  # More spacing between words
        # Checkbox - larger
        draw.rectangle([word_list_x, y_pos, word_list_x + 18, y_pos + 18], outline='#666666', width=2)
        # Word
        draw.text((word_list_x + 28, y_pos), word, fill='#444444', font=word_font)

    # Add cell illustration if available
    cell_img_path = OUTPUT_DIR / "cell_illustration_temp.png"
    if cell_img_path.exists():
        try:
            cell_img = Image.open(cell_img_path)
            # Resize to fit in corner (300x300)
            cell_img = cell_img.resize((280, 280), Image.Resampling.LANCZOS)
            # Position in upper right corner above word list
            paste_x = word_list_x - 20
            paste_y = grid_start_y - 80
            template.paste(cell_img, (paste_x, paste_y), cell_img if cell_img.mode == 'RGBA' else None)
            print("   [OK] Cell illustration added to worksheet")
        except Exception as e:
            print(f"   [WARNING] Could not add cell illustration: {e}")

    # NGSS Standard at bottom
    ngss_text = "NGSS: MS-LS1-2 | Develop and use a model to describe cell parts and their functions"
    draw.text((120, height - 90), ngss_text, fill='#888888', font=small_font)

    # Save worksheet
    output_path = OUTPUT_DIR / "Cell_Structure_Word_Search_Grade7.png"
    template.save(output_path, 'PNG', quality=95)

    print(f"   [OK] Worksheet saved: {output_path}")
    return str(output_path)

def convert_to_pdf(png_path):
    """Convert PNG to PDF"""
    print("[5/5] Converting to PDF...")

    pdf_path = Path(png_path).with_suffix('.pdf')

    img = Image.open(png_path)
    img = img.convert('RGB')
    img.save(pdf_path, 'PDF', resolution=300)

    print(f"   [OK] PDF saved: {pdf_path}")
    return str(pdf_path)

if __name__ == '__main__':
    print("=" * 70)
    print("TPT WORD SEARCH GENERATOR - CELL BIOLOGY")
    print("=" * 70)

    # Step 1: Generate cell illustration
    cell_img = generate_cell_illustration()

    # Step 2: Create worksheet
    worksheet_path = create_word_search_worksheet()

    # Step 3: Convert to PDF
    pdf_path = convert_to_pdf(worksheet_path)

    print("\n" + "=" * 70)
    print("[SUCCESS] WORKSHEET COMPLETE!")
    print("=" * 70)
    print(f"PNG: {worksheet_path}")
    print(f"PDF: {pdf_path}")
    print("\nNext: Review with GPT-5 Vision for QA")
