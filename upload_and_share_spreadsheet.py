"""
Upload Excel to Google Drive and share with email
"""
import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

# Scopes needed
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]

def get_google_drive_service():
    """Authenticate and return Google Drive service"""
    creds = None

    # Check for existing token
    if os.path.exists('token_drive.pickle'):
        with open('token_drive.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Check for credentials.json
            if not os.path.exists('scripts/credentials.json'):
                print("ERROR: credentials.json not found!")
                print("Please download OAuth 2.0 credentials from Google Cloud Console")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(
                'scripts/credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        # Save credentials
        with open('token_drive.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def upload_and_share_spreadsheet(file_path, share_email):
    """Upload Excel to Drive and share with email"""

    service = get_google_drive_service()
    if not service:
        return None

    # Upload file and convert to Google Sheets
    file_metadata = {
        'name': 'ModelIT Blog Schedule - Complete with HTML',
        'mimeType': 'application/vnd.google-apps.spreadsheet'
    }

    media = MediaFileUpload(
        file_path,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        resumable=True
    )

    print("Uploading file to Google Drive...")
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()

    file_id = file.get('id')
    web_link = file.get('webViewLink')

    print(f"SUCCESS: File uploaded to Google Drive")
    print(f"File ID: {file_id}")
    print(f"Link: {web_link}")

    # Share with email address
    print(f"\nSharing with {share_email}...")

    permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': share_email
    }

    service.permissions().create(
        fileId=file_id,
        body=permission,
        fields='id',
        sendNotificationEmail=True,
        emailMessage='Hi! Here is the complete ModelIT blog schedule with HTML content and embedded images. All 52 weeks are ready to post!'
    ).execute()

    print(f"SUCCESS: Shared with {share_email} (Editor access)")

    return web_link

# Main execution
if __name__ == "__main__":
    excel_file = 'modelit-blog-schedule-final-with-html.xlsx'
    share_with = 'bilalrazaswe@gmail.com'

    if not os.path.exists(excel_file):
        print(f"ERROR: {excel_file} not found!")
    else:
        link = upload_and_share_spreadsheet(excel_file, share_with)
        if link:
            print("\n" + "="*60)
            print("ALL DONE!")
            print(f"Spreadsheet Link: {link}")
            print(f"Shared with: {share_with}")
            print("="*60)
