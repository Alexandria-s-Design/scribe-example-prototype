#!/usr/bin/env python3
"""
Share the Ecosystem Coloring Sheet Google Slides presentation
Sets permissions to anyone with the link can view
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
    """Authenticate with Google Drive API using existing token"""
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

def share_presentation():
    """Share the presentation with anyone who has the link"""

    creds = authenticate()
    drive_service = build('drive', 'v3', credentials=creds)

    print(f"Sharing presentation: {PRESENTATION_ID}")

    # Set permissions to anyone with the link can view
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }

    try:
        drive_service.permissions().create(
            fileId=PRESENTATION_ID,
            body=permission
        ).execute()
        print("Sharing enabled: Anyone with the link can view")

    except Exception as e:
        if 'already exists' in str(e).lower():
            print("Sharing already enabled")
        else:
            raise

    # Get file details
    file = drive_service.files().get(
        fileId=PRESENTATION_ID,
        fields='name, webViewLink, permissions'
    ).execute()

    return file

if __name__ == "__main__":
    try:
        file = share_presentation()
        print(f"\nPresentation Name: {file['name']}")
        print(f"\nShareable Link:")
        print(file['webViewLink'])
        print("\nPermissions: Anyone with the link can view")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
