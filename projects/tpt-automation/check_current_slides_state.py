#!/usr/bin/env python3
"""
Check Current State of Google Slides Presentation
Retrieves and displays the current layout/positioning of all elements
"""

import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Configuration
PRESENTATION_ID = "1Q1eqqPwCQrY4eFiUDqBwRuFXpwF7CaEVQgbPp6qGfj0"
TOKEN_FILE = "C:/Users/MarieLexisDad/Old Files/google-workspace-mcp/token-personal.json"
ACCOUNTS_CONFIG_FILE = "C:/Users/MarieLexisDad/Old Files/google-workspace-mcp/accounts.json"

def authenticate():
    """Authenticate with Google Slides API"""
    with open(ACCOUNTS_CONFIG_FILE, 'r') as f:
        accounts_config = json.load(f)
    with open(TOKEN_FILE, 'r') as f:
        token_data = json.load(f)

    personal_config = accounts_config['personal']
    creds = Credentials(
        token=token_data.get('access_token'),
        refresh_token=token_data.get('refresh_token'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=personal_config['clientId'],
        client_secret=personal_config['clientSecret'],
        scopes=token_data.get('scope', '').split()
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return creds

def emu_to_inches(emu):
    """Convert EMU to inches"""
    return emu / 914400.0

def check_slides_state():
    """Check current state of the presentation"""
    creds = authenticate()
    service = build('slides', 'v1', credentials=creds)

    # Get presentation
    presentation = service.presentations().get(
        presentationId=PRESENTATION_ID
    ).execute()

    print("="*80)
    print("CURRENT GOOGLE SLIDES STATE")
    print("="*80)
    print(f"\nPresentation: {presentation.get('title')}")
    print(f"Slides: {len(presentation.get('slides', []))}")

    # Check page size
    page_size = presentation.get('pageSize', {})
    width_emu = page_size.get('width', {}).get('magnitude', 0)
    height_emu = page_size.get('height', {}).get('magnitude', 0)
    width_inches = emu_to_inches(width_emu)
    height_inches = emu_to_inches(height_emu)

    print(f"\nPage Size: {width_inches:.2f}\" × {height_inches:.2f}\"")
    if width_inches < 8.4 or width_inches > 8.6 or height_inches < 10.9 or height_inches > 11.1:
        print("  WARNING: Not standard US Letter size (8.5\" × 11\")")

    # Check first slide
    if presentation.get('slides'):
        slide = presentation['slides'][0]
        print(f"\nSlide ID: {slide['objectId']}")

        # Count elements by type
        page_elements = slide.get('pageElements', [])
        print(f"\nTotal Elements: {len(page_elements)}")

        images = [e for e in page_elements if 'image' in e]
        text_boxes = [e for e in page_elements if 'shape' in e]

        print(f"  Images: {len(images)}")
        print(f"  Text Boxes: {len(text_boxes)}")

        # Show all image details
        if images:
            print("\n" + "="*80)
            print("IMAGE DETAILS")
            print("="*80)

            for i, img in enumerate(images, 1):
                transform = img.get('transform', {})
                size = img.get('size', {})

                x = emu_to_inches(transform.get('translateX', 0))
                y = emu_to_inches(transform.get('translateY', 0))
                w = emu_to_inches(size.get('width', {}).get('magnitude', 0))
                h = emu_to_inches(size.get('height', {}).get('magnitude', 0))

                print(f"\nImage {i}:")
                print(f"  Position: ({x:.2f}\", {y:.2f}\")")
                print(f"  Size: {w:.2f}\" × {h:.2f}\"")
                print(f"  ID: {img['objectId']}")

                # Check if out of bounds
                if x < 0 or y < 0 or (x + w) > width_inches or (y + h) > height_inches:
                    print(f"  WARNING: Image extends beyond page bounds!")

        # Show text boxes
        if text_boxes:
            print("\n" + "="*80)
            print("TEXT BOX DETAILS")
            print("="*80)

            for i, tb in enumerate(text_boxes, 1):
                transform = tb.get('transform', {})
                size = tb.get('size', {})

                x = emu_to_inches(transform.get('translateX', 0))
                y = emu_to_inches(transform.get('translateY', 0))
                w = emu_to_inches(size.get('width', {}).get('magnitude', 0))
                h = emu_to_inches(size.get('height', {}).get('magnitude', 0))

                # Get text content
                text = ""
                shape = tb.get('shape', {})
                text_elements = shape.get('text', {}).get('textElements', [])
                for te in text_elements:
                    if 'textRun' in te:
                        text += te['textRun'].get('content', '')

                print(f"\nText Box {i}:")
                print(f"  Position: ({x:.2f}\", {y:.2f}\")")
                print(f"  Size: {w:.2f}\" × {h:.2f}\"")
                print(f"  Content: {text.strip()[:50]}...")

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)

if __name__ == "__main__":
    try:
        check_slides_state()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
