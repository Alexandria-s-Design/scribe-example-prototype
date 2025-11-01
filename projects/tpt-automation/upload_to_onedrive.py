#!/usr/bin/env python3
"""
Upload PPTX to OneDrive and get shareable link
Using Office 365 MCP tools via Python
"""

import os
import json
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

# Configuration
PPTX_FILE = "C:/Users/MarieLexisDad/projects/tpt-automation/Ecosystem_Coloring_Sheet.pptx"
TOKEN_FILE = "C:/Users/MarieLexisDad/Old Files/google-workspace-mcp/token-personal.json"
ACCOUNTS_CONFIG_FILE = "C:/Users/MarieLexisDad/Old Files/google-workspace-mcp/accounts.json"

def authenticate():
    """Authenticate with Google Drive"""
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

def upload_to_drive():
    """Upload PowerPoint to Google Drive and get shareable link"""

    print("="*80)
    print("UPLOADING TO GOOGLE DRIVE")
    print("="*80)

    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    # Upload file
    file_metadata = {
        'name': 'Ecosystem Coloring Sheet - 3rd Grade.pptx',
        'mimeType': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    }

    print(f"\nUploading: {PPTX_FILE}")
    print(f"Size: {os.path.getsize(PPTX_FILE) / 1024:.1f} KB")

    media = MediaFileUpload(
        PPTX_FILE,
        mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
        resumable=True
    )

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink, webContentLink'
    ).execute()

    file_id = file.get('id')
    print(f"\nUploaded successfully!")
    print(f"File ID: {file_id}")

    # Make it shareable (anyone with link can view)
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }

    service.permissions().create(
        fileId=file_id,
        body=permission
    ).execute()

    print("\nSharing enabled: Anyone with the link can view")

    # Get file details
    file_details = service.files().get(
        fileId=file_id,
        fields='name, webViewLink, webContentLink, size'
    ).execute()

    print("\n" + "="*80)
    print("UPLOAD COMPLETE")
    print("="*80)
    print(f"\nFile Name: {file_details['name']}")
    print(f"\nView in Browser:")
    print(file_details['webViewLink'])
    print(f"\nDirect Download:")
    print(file_details['webContentLink'])

    return file_details

if __name__ == "__main__":
    try:
        upload_to_drive()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
