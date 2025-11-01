#!/usr/bin/env python3
"""
Fix Image Sizes in Google Slides
The API doesn't respect size on initial creation, so we need to update them
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

IMAGE_SIZE_INCHES = 1.5

def inches_to_emu(inches):
    """Convert inches to EMU"""
    return int(inches * 914400)

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

def fix_image_sizes():
    """Update all image sizes to correct dimensions"""

    creds = authenticate()
    service = build('slides', 'v1', credentials=creds)

    print("="*80)
    print("FIXING IMAGE SIZES")
    print("="*80)

    # Get presentation
    presentation = service.presentations().get(
        presentationId=PRESENTATION_ID
    ).execute()

    slide = presentation['slides'][0]
    page_elements = slide.get('pageElements', [])

    # Find all images
    images = [e for e in page_elements if 'image' in e]
    print(f"\nFound {len(images)} images")

    # Create update requests for each image
    update_requests = []

    for img in images:
        object_id = img['objectId']

        # Update size
        update_requests.append({
            'updatePageElementTransform': {
                'objectId': object_id,
                'transform': {
                    'scaleX': 1,
                    'scaleY': 1,
                    'translateX': img['transform']['translateX'],
                    'translateY': img['transform']['translateY'],
                    'unit': 'EMU'
                },
                'applyMode': 'ABSOLUTE'
            }
        })

        # Explicitly set size
        update_requests.append({
            'updatePageElementSize': {
                'objectId': object_id,
                'size': {
                    'width': {'magnitude': inches_to_emu(IMAGE_SIZE_INCHES), 'unit': 'EMU'},
                    'height': {'magnitude': inches_to_emu(IMAGE_SIZE_INCHES), 'unit': 'EMU'}
                }
            }
        })

    # Execute all updates
    if update_requests:
        print(f"Applying {len(update_requests)} size updates...")
        service.presentations().batchUpdate(
            presentationId=PRESENTATION_ID,
            body={'requests': update_requests}
        ).execute()
        print("Size updates complete!")

    # Verify
    print("\nVerifying sizes...")
    presentation = service.presentations().get(
        presentationId=PRESENTATION_ID
    ).execute()

    slide = presentation['slides'][0]
    images = [e for e in slide.get('pageElements', []) if 'image' in e]

    for i, img in enumerate(images, 1):
        size = img.get('size', {})
        width_emu = size.get('width', {}).get('magnitude', 0)
        height_emu = size.get('height', {}).get('magnitude', 0)
        width_inches = width_emu / 914400.0
        height_inches = height_emu / 914400.0
        print(f"  Image {i}: {width_inches:.2f}\" × {height_inches:.2f}\"")

    print("\n" + "="*80)
    print("DONE")
    print("="*80)
    print(f"\nPresentation URL:")
    print(f"https://docs.google.com/presentation/d/{PRESENTATION_ID}/edit")

if __name__ == "__main__":
    try:
        fix_image_sizes()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
