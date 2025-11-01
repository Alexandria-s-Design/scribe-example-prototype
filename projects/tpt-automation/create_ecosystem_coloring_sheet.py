#!/usr/bin/env python3
"""
Create Ecosystem Coloring Sheet Prototype in Google Slides
Author: Alexandria's Design
Purpose: Demonstrate TPT product creation process
"""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os

# Account configuration (same as create_google_doc.py)
ACCOUNTS_CONFIG_FILE = r'C:\Users\MarieLexisDad\Old Files\google-workspace-mcp\accounts.json'
TOKEN_FILE = r'C:\Users\MarieLexisDad\Old Files\google-workspace-mcp\token-personal.json'

def authenticate():
    """Authenticate with Google Slides API using existing token"""
    try:
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
        return creds
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return None

def create_ecosystem_coloring_sheet():
    """Create a prototype ecosystem coloring sheet in Google Slides"""

    creds = authenticate()
    if not creds:
        print("Authentication failed")
        return None

    slides_service = build('slides', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    # Create a new presentation
    presentation = slides_service.presentations().create(body={
        'title': 'Ecosystem Coloring Sheet - 3rd Grade Prototype'
    }).execute()

    presentation_id = presentation['presentationId']
    print(f'Created presentation: {presentation_id}')

    # Get the first slide
    slides = slides_service.presentations().get(presentationId=presentation_id).execute().get('slides', [])
    slide_id = slides[0]['objectId']

    print('Note: Please manually set page size to 8.5" x 11" via File > Page setup > Custom')
    print('      (Google Slides API limitations)')

    # Build requests to add content
    requests = [

        # Add title
        {
            'createShape': {
                'objectId': 'title_box',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'height': {'magnitude': 60, 'unit': 'PT'},
                        'width': {'magnitude': 550, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': 30,
                        'translateY': 30,
                        'unit': 'PT'
                    }
                }
            }
        },
        {
            'insertText': {
                'objectId': 'title_box',
                'text': 'Forest Ecosystem Coloring Sheet'
            }
        },
        {
            'updateTextStyle': {
                'objectId': 'title_box',
                'style': {
                    'bold': True,
                    'fontSize': {'magnitude': 24, 'unit': 'PT'},
                    'foregroundColor': {
                        'opaqueColor': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}}
                    }
                },
                'fields': 'bold,fontSize,foregroundColor'
            }
        },

        # Add student info box
        {
            'createShape': {
                'objectId': 'student_info',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'height': {'magnitude': 40, 'unit': 'PT'},
                        'width': {'magnitude': 550, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': 30,
                        'translateY': 100,
                        'unit': 'PT'
                    }
                }
            }
        },
        {
            'insertText': {
                'objectId': 'student_info',
                'text': 'Name: _________________     Date: __________'
            }
        },

        # Add instructions box
        {
            'createShape': {
                'objectId': 'instructions',
                'shapeType': 'RECTANGLE',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'height': {'magnitude': 60, 'unit': 'PT'},
                        'width': {'magnitude': 550, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': 30,
                        'translateY': 150,
                        'unit': 'PT'
                    }
                }
            }
        },
        {
            'updateShapeProperties': {
                'objectId': 'instructions',
                'shapeProperties': {
                    'outline': {
                        'outlineFill': {
                            'solidFill': {
                                'color': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}}
                            }
                        },
                        'weight': {'magnitude': 2, 'unit': 'PT'}
                    }
                },
                'fields': 'outline'
            }
        },
        {
            'insertText': {
                'objectId': 'instructions',
                'text': 'Instructions: Color the living and non-living things in this forest ecosystem. Label each part!'
            }
        },
        {
            'updateTextStyle': {
                'objectId': 'instructions',
                'style': {
                    'fontSize': {'magnitude': 12, 'unit': 'PT'}
                },
                'fields': 'fontSize'
            }
        },

        # Add main coloring area with ecosystem elements descriptions
        {
            'createShape': {
                'objectId': 'ecosystem_area',
                'shapeType': 'RECTANGLE',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'height': {'magnitude': 450, 'unit': 'PT'},
                        'width': {'magnitude': 550, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': 30,
                        'translateY': 230,
                        'unit': 'PT'
                    }
                }
            }
        },
        {
            'updateShapeProperties': {
                'objectId': 'ecosystem_area',
                'shapeProperties': {
                    'outline': {
                        'outlineFill': {
                            'solidFill': {
                                'color': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}}
                            }
                        },
                        'weight': {'magnitude': 3, 'unit': 'PT'}
                    }
                },
                'fields': 'outline'
            }
        },

        # Add ecosystem elements as text labels (teacher will add drawings or use clipart)
        {
            'createShape': {
                'objectId': 'elements_guide',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'height': {'magnitude': 400, 'unit': 'PT'},
                        'width': {'magnitude': 500, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': 55,
                        'translateY': 250,
                        'unit': 'PT'
                    }
                }
            }
        },
        {
            'insertText': {
                'objectId': 'elements_guide',
                'text': '''Draw and Color These Ecosystem Parts:

Living Things:
• Oak tree (producer)
• Deer (consumer)
• Rabbit (consumer)
• Mushrooms (decomposer)
• Grass and flowers

Non-Living Things:
• Sun (provides energy)
• Rocks
• Water (pond or stream)
• Soil'''
            }
        },
        {
            'updateTextStyle': {
                'objectId': 'elements_guide',
                'style': {
                    'fontSize': {'magnitude': 14, 'unit': 'PT'}
                },
                'fields': 'fontSize'
            }
        },

        # Add vocabulary box at bottom
        {
            'createShape': {
                'objectId': 'vocabulary',
                'shapeType': 'RECTANGLE',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'height': {'magnitude': 60, 'unit': 'PT'},
                        'width': {'magnitude': 550, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': 30,
                        'translateY': 700,
                        'unit': 'PT'
                    }
                }
            }
        },
        {
            'updateShapeProperties': {
                'objectId': 'vocabulary',
                'shapeProperties': {
                    'shapeBackgroundFill': {
                        'solidFill': {
                            'color': {'rgbColor': {'red': 0.95, 'green': 0.95, 'blue': 0.95}}
                        }
                    },
                    'outline': {
                        'outlineFill': {
                            'solidFill': {
                                'color': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}}
                            }
                        },
                        'weight': {'magnitude': 2, 'unit': 'PT'}
                    }
                },
                'fields': 'shapeBackgroundFill,outline'
            }
        },
        {
            'insertText': {
                'objectId': 'vocabulary',
                'text': 'Vocabulary: Ecosystem • Producer • Consumer • Decomposer • Habitat'
            }
        },
        {
            'updateTextStyle': {
                'objectId': 'vocabulary',
                'style': {
                    'fontSize': {'magnitude': 11, 'unit': 'PT'},
                    'bold': True
                },
                'fields': 'fontSize,bold'
            }
        }
    ]

    # Filter out empty requests
    requests = [r for r in requests if r]

    # Execute all requests
    try:
        slides_service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': requests}
        ).execute()
        print('Successfully created coloring sheet content')
    except Exception as e:
        print(f'Error creating content: {e}')
        return None

    # Get shareable link
    try:
        permission = drive_service.permissions().create(
            fileId=presentation_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()

        file_link = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
        print(f'\n[SUCCESS] Coloring Sheet Created!')
        print(f'View/Edit: {file_link}')

        return {
            'presentation_id': presentation_id,
            'link': file_link
        }
    except Exception as e:
        print(f'Error sharing file: {e}')
        return None

if __name__ == '__main__':
    print("Creating Ecosystem Coloring Sheet Prototype...")
    print("=" * 60)
    result = create_ecosystem_coloring_sheet()

    if result:
        print("\n" + "=" * 60)
        print("NEXT STEPS:")
        print("1. Open the link above to view your prototype")
        print("2. Add drawings/clipart for the ecosystem elements")
        print("3. Export as PDF for printing")
        print("4. Use this as a template for automation!")
