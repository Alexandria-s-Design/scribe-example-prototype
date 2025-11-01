#!/usr/bin/env python3
"""
Upload Ecosystem Images to Google Slides Template
Inserts the 8 generated ecosystem images into the coloring sheet presentation
"""

import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

# Configuration
PRESENTATION_ID = "1Q1eqqPwCQrY4eFiUDqBwRuFXpwF7CaEVQgbPp6qGfj0"
IMAGE_DIR = "C:/Users/MarieLexisDad/projects/tpt-automation/ecosystem-artwork"
TOKEN_FILE = "C:/Users/MarieLexisDad/Old Files/google-workspace-mcp/token-personal.json"
ACCOUNTS_CONFIG_FILE = "C:/Users/MarieLexisDad/Old Files/google-workspace-mcp/accounts.json"

# Image positions on the slide (in EMU - 914400 EMU = 1 inch)
# Layout: 4 images across top, 4 images across bottom
IMAGES = [
    {"file": "oak_tree.png", "x": 0.5, "y": 1.5, "width": 2, "height": 2},
    {"file": "deer.png", "x": 3, "y": 1.5, "width": 2, "height": 2},
    {"file": "rabbit.png", "x": 5.5, "y": 1.5, "width": 2, "height": 2},
    {"file": "mushrooms.png", "x": 8, "y": 1.5, "width": 2, "height": 2},
    {"file": "sun.png", "x": 0.5, "y": 4, "width": 2, "height": 2},
    {"file": "rocks.png", "x": 3, "y": 4, "width": 2, "height": 2},
    {"file": "pond.png", "x": 5.5, "y": 4, "width": 2, "height": 2},
    {"file": "grass_flowers.png", "x": 8, "y": 4, "width": 2, "height": 2}
]

def inches_to_emu(inches):
    """Convert inches to EMU (English Metric Units)"""
    return int(inches * 914400)

def authenticate():
    """Authenticate with Google Slides API using existing token"""
    try:
        # Load accounts config
        with open(ACCOUNTS_CONFIG_FILE, 'r') as f:
            accounts_config = json.load(f)

        # Load token
        with open(TOKEN_FILE, 'r') as f:
            token_data = json.load(f)

        personal_config = accounts_config['personal']

        # Create credentials object
        creds = Credentials(
            token=token_data.get('access_token'),
            refresh_token=token_data.get('refresh_token'),
            token_uri='https://oauth2.googleapis.com/token',
            client_id=personal_config['clientId'],
            client_secret=personal_config['clientSecret'],
            scopes=token_data.get('scope', '').split()
        )

        # Refresh if needed
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        return creds

    except Exception as e:
        print(f"Error authenticating: {e}")
        raise

def upload_images_to_slides():
    """Upload all 8 ecosystem images to the Google Slides presentation"""

    creds = authenticate()
    slides_service = build('slides', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    print(f"Uploading images to presentation: {PRESENTATION_ID}")

    # First, get the presentation to find the slide ID
    presentation = slides_service.presentations().get(
        presentationId=PRESENTATION_ID
    ).execute()

    # Get the first slide ID (where we'll add images)
    slide_id = presentation['slides'][0]['objectId']
    print(f"Adding images to slide: {slide_id}")

    # Prepare batch requests for all images
    requests = []

    for img_info in IMAGES:
        img_path = os.path.join(IMAGE_DIR, img_info['file'])

        if not os.path.exists(img_path):
            print(f"Warning: Image not found: {img_path}")
            continue

        print(f"Processing: {img_info['file']}")

        # Upload image to Google Drive
        file_metadata = {
            'name': img_info['file'],
            'mimeType': 'image/png'
        }

        media = MediaFileUpload(img_path, mimetype='image/png', resumable=True)

        drive_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webContentLink'
        ).execute()

        file_id = drive_file.get('id')
        print(f"  Uploaded to Drive: {file_id}")

        # Make the file publicly accessible
        drive_service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()

        # Get the image URL
        image_url = f"https://drive.google.com/uc?export=view&id={file_id}"

        # Create request to insert image into slide
        requests.append({
            'createImage': {
                'url': image_url,
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'width': {'magnitude': inches_to_emu(img_info['width']), 'unit': 'EMU'},
                        'height': {'magnitude': inches_to_emu(img_info['height']), 'unit': 'EMU'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': inches_to_emu(img_info['x']),
                        'translateY': inches_to_emu(img_info['y']),
                        'unit': 'EMU'
                    }
                }
            }
        })

    # Execute all image insertions in one batch
    if requests:
        print(f"\nInserting {len(requests)} images into slide...")
        body = {'requests': requests}
        slides_service.presentations().batchUpdate(
            presentationId=PRESENTATION_ID,
            body=body
        ).execute()
        print("All images inserted successfully!")

    # Get shareable link
    presentation_url = f"https://docs.google.com/presentation/d/{PRESENTATION_ID}/edit"

    return presentation_url

if __name__ == "__main__":
    try:
        url = upload_images_to_slides()
        print(f"\nEcosystem Coloring Sheet Complete!")
        print(f"\nGoogle Slides URL:")
        print(url)
        print("\nImages uploaded:")
        for img in IMAGES:
            print(f"  - {img['file']}")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
