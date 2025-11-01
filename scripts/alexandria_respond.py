#!/usr/bin/env python3
"""
Alexandria - Manual Response Handler
Usage: python alexandria_respond.py "channel_id" "message text"
"""

import os
import sys
import requests

GROK_API_KEY = os.getenv("GROK_API_KEY", "")

ALEXANDRIA_PROMPT = """You are Alexandria, an AI teammate for Alexandria's Design, founded by Charles Martin and Dr. Marie Martin.

BUSINESS CONTEXT:
- Educational technology consulting for K-12, higher ed, government, military
- Revenue goal: $30k/month ("let's get to the bread")
- Products: ModelIt!, Alexandria's World, professional development

YOUR CAPABILITIES:
- Email: Office 365, Gmail
- Calendar: Google Calendar, Office 365
- Projects: Monday.com
- Files: OneDrive, Google Drive

PERSONALITY:
- Professional yet friendly
- Revenue-focused and practical
- Proactive
- Educational expertise

ALWAYS:
- Think revenue-first
- Be concise in Slack
- Ask clarifying questions"""


def call_grok(message_text):
    """Call Grok 4 API"""
    try:
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "grok-2-latest",
                "messages": [
                    {"role": "system", "content": ALEXANDRIA_PROMPT},
                    {"role": "user", "content": message_text}
                ],
                "temperature": 0.7
            },
            timeout=30
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python alexandria_respond.py \"message text\"")
        print("\nExample:")
        print("  python alexandria_respond.py \"What is our revenue goal?\"")
        print("\nThis will:")
        print("  1. Call Grok 4 with the message")
        print("  2. Return Alexandria's response")
        print("  3. You can copy/paste to Slack")
        sys.exit(1)

    message = " ".join(sys.argv[1:])

    print(f"\nProcessing: {message}\n")
    print("Calling Grok 4...")

    response = call_grok(message)

    if response:
        # Add Alexandria signature
        response_with_signature = f"{response}\n\n- Alexandria"

        print("\n" + "="*60)
        print("Alexandria's Response:")
        print("="*60)
        print(response_with_signature)
        print("="*60 + "\n")
        print("Copy the response above and paste it in Slack!")
    else:
        print("\n[ERROR] Failed to get response from Grok")
