#!/usr/bin/env python3
"""
Rebuild Google Slides Presentation with Correct Layout
Deletes all broken elements and recreates with proper sizing and positioning
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

# Image layout - 4 across top, 4 across bottom
# Each image 1.5" × 1.5", with 0.5" margins and 0.25" spacing
IMAGES = [
    {"file": "oak_tree.png", "x": 0.5, "y": 2.0, "name": "Oak Tree"},
    {"file": "deer.png", "x": 2.25, "y": 2.0, "name": "Deer"},
    {"file": "rabbit.png", "x": 4.0, "y": 2.0, "name": "Rabbit"},
    {"file": "mushrooms.png", "x": 5.75, "y": 2.0, "name": "Mushrooms"},
    {"file": "sun.png", "x": 0.5, "y": 4.0, "name": "Sun"},
    {"file": "rocks.png", "x": 2.25, "y": 4.0, "name": "Rocks"},
    {"file": "pond.png", "x": 4.0, "y": 4.0, "name": "Pond"},
    {"file": "grass_flowers.png", "x": 5.75, "y": 4.0, "name": "Grass"}
]

IMAGE_SIZE = 1.5  # inches

def inches_to_emu(inches):
    """Convert inches to EMU"""
    return int(inches * 914400)

def authenticate():
    """Authenticate with Google APIs"""
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

def rebuild_presentation():
    """Completely rebuild the presentation with correct layout"""

    creds = authenticate()
    slides_service = build('slides', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    print("="*80)
    print("REBUILDING GOOGLE SLIDES PRESENTATION")
    print("="*80)

    # Get current presentation
    presentation = slides_service.presentations().get(
        presentationId=PRESENTATION_ID
    ).execute()

    slide_id = presentation['slides'][0]['objectId']
    print(f"\nSlide ID: {slide_id}")

    # Step 1: Delete ALL existing elements
    print("\nStep 1: Clearing all existing elements...")
    page_elements = presentation['slides'][0].get('pageElements', [])

    delete_requests = []
    for element in page_elements:
        delete_requests.append({
            'deleteObject': {
                'objectId': element['objectId']
            }
        })

    if delete_requests:
        slides_service.presentations().batchUpdate(
            presentationId=PRESENTATION_ID,
            body={'requests': delete_requests}
        ).execute()
        print(f"  Deleted {len(delete_requests)} elements")

    # Step 2: Add title and instructions
    print("\nStep 2: Adding title and instructions...")

    text_requests = [
        # Title
        {
            'createShape': {
                'objectId': 'title_box',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'width': {'magnitude': inches_to_emu(7.5), 'unit': 'EMU'},
                        'height': {'magnitude': inches_to_emu(0.6), 'unit': 'EMU'}
                    },
                    'transform': {
                        'scaleX': 1, 'scaleY': 1,
                        'translateX': inches_to_emu(0.5),
                        'translateY': inches_to_emu(0.5),
                        'unit': 'EMU'
                    }
                }
            }
        },
        {
            'insertText': {
                'objectId': 'title_box',
                'text': 'Ecosystem Coloring Sheet - 3rd Grade'
            }
        },
        # Student info
        {
            'createShape': {
                'objectId': 'student_info',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'width': {'magnitude': inches_to_emu(7.5), 'unit': 'EMU'},
                        'height': {'magnitude': inches_to_emu(0.4), 'unit': 'EMU'}
                    },
                    'transform': {
                        'scaleX': 1, 'scaleY': 1,
                        'translateX': inches_to_emu(0.5),
                        'translateY': inches_to_emu(1.2),
                        'unit': 'EMU'
                    }
                }
            }
        },
        {
            'insertText': {
                'objectId': 'student_info',
                'text': 'Name: ________________     Date: __________'
            }
        },
        # Instructions
        {
            'createShape': {
                'objectId': 'instructions',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'width': {'magnitude': inches_to_emu(7.5), 'unit': 'EMU'},
                        'height': {'magnitude': inches_to_emu(0.4), 'unit': 'EMU'}
                    },
                    'transform': {
                        'scaleX': 1, 'scaleY': 1,
                        'translateX': inches_to_emu(0.5),
                        'translateY': inches_to_emu(1.7),
                        'unit': 'EMU'
                    }
                }
            }
        },
        {
            'insertText': {
                'objectId': 'instructions',
                'text': 'Instructions: Color each ecosystem element below'
            }
        },
        # Vocabulary footer
        {
            'createShape': {
                'objectId': 'vocabulary',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'width': {'magnitude': inches_to_emu(7.5), 'unit': 'EMU'},
                        'height': {'magnitude': inches_to_emu(0.6), 'unit': 'EMU'}
                    },
                    'transform': {
                        'scaleX': 1, 'scaleY': 1,
                        'translateX': inches_to_emu(0.5),
                        'translateY': inches_to_emu(6.0),
                        'unit': 'EMU'
                    }
                }
            }
        },
        {
            'insertText': {
                'objectId': 'vocabulary',
                'text': 'Vocabulary: Ecosystem - Producer - Consumer - Decomposer'
            }
        }
    ]

    slides_service.presentations().batchUpdate(
        presentationId=PRESENTATION_ID,
        body={'requests': text_requests}
    ).execute()
    print("  Text elements added")

    # Step 3: Upload and add images
    print("\nStep 3: Adding ecosystem images...")

    image_requests = []
    for i, img_info in enumerate(IMAGES):
        img_path = os.path.join(IMAGE_DIR, img_info['file'])

        if not os.path.exists(img_path):
            print(f"  WARNING: {img_info['file']} not found")
            continue

        print(f"  Processing: {img_info['name']}")

        # Upload to Drive
        file_metadata = {'name': img_info['file'], 'mimeType': 'image/png'}
        media = MediaFileUpload(img_path, mimetype='image/png', resumable=True)
        drive_file = drive_service.files().create(
            body=file_metadata, media_body=media, fields='id'
        ).execute()

        file_id = drive_file.get('id')

        # Make public
        drive_service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()

        image_url = f"https://drive.google.com/uc?export=view&id={file_id}"

        # Add to slide
        image_requests.append({
            'createImage': {
                'url': image_url,
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'width': {'magnitude': inches_to_emu(IMAGE_SIZE), 'unit': 'EMU'},
                        'height': {'magnitude': inches_to_emu(IMAGE_SIZE), 'unit': 'EMU'}
                    },
                    'transform': {
                        'scaleX': 1, 'scaleY': 1,
                        'translateX': inches_to_emu(img_info['x']),
                        'translateY': inches_to_emu(img_info['y']),
                        'unit': 'EMU'
                    }
                }
            }
        })

    if image_requests:
        slides_service.presentations().batchUpdate(
            presentationId=PRESENTATION_ID,
            body={'requests': image_requests}
        ).execute()
        print(f"  Added {len(image_requests)} images")

    print("\n" + "="*80)
    print("REBUILD COMPLETE")
    print("="*80)
    print(f"\nPresentation URL:")
    print(f"https://docs.google.com/presentation/d/{PRESENTATION_ID}/edit")

if __name__ == "__main__":
    try:
        rebuild_presentation()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
