#!/usr/bin/env python3
"""
Alexandria - Automatic Slack Bot
Uses Flask webhook to receive Slack events automatically
"""

import os
import sys
import json
import requests
from flask import Flask, request, jsonify
import threading
import time

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
GROK_API_KEY = os.getenv("GROK_API_KEY", "")
BOT_USER_ID = "U09QSBHFBCY"

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

app = Flask(__name__)
processed_events = set()


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
        return None

    except Exception as e:
        print(f"Grok error: {e}")
        return None


def send_to_slack(channel, text, thread_ts=None):
    """Send message via Slack API"""
    try:
        # Add signature
        text_with_signature = f"{text}\n\n- Alexandria"

        payload = {
            "channel": channel,
            "text": text_with_signature
        }
        if thread_ts:
            payload["thread_ts"] = thread_ts

        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={
                "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=10
        )

        return response.json().get("ok", False)

    except Exception as e:
        print(f"Slack send error: {e}")
        return False


def process_mention(event):
    """Process app_mention event"""
    event_id = event.get("client_msg_id") or event.get("ts")

    # Avoid duplicates
    if event_id in processed_events:
        return
    processed_events.add(event_id)

    # Ignore bot's own messages
    if event.get("user") == BOT_USER_ID:
        return

    text = event.get("text", "")
    channel = event.get("channel")
    ts = event.get("ts")

    # Clean up @mention
    import re
    clean_text = re.sub(r'<@[A-Z0-9]+>', '', text).strip()

    print(f"\n[MENTION] {clean_text[:50]}...")

    # Call Grok
    response = call_grok(clean_text)

    if response:
        print(f"[RESPONSE] Sending to Slack...")
        success = send_to_slack(channel, response, thread_ts=ts)
        if success:
            print(f"[OK] Sent!")
        else:
            print(f"[FAIL] Could not send")


@app.route('/slack/events', methods=['POST'])
def slack_events():
    """Handle Slack events"""
    data = request.json

    # URL verification
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})

    # Event callback
    if data.get("type") == "event_callback":
        event = data.get("event", {})

        # Handle app_mention
        if event.get("type") == "app_mention":
            # Process in background to respond quickly
            threading.Thread(target=process_mention, args=(event,)).start()

        return jsonify({"ok": True})

    return jsonify({"ok": True})


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "bot": "Alexandria"})


def main():
    print("\n" + "="*60)
    print("Alexandria - Automatic Slack Bot")
    print("="*60)
    print("\n[INFO] Starting webhook server on port 3000...")
    print("[INFO] Slack will send events here automatically\n")
    print("Setup Steps:")
    print("1. This server is running on http://localhost:3000")
    print("2. You need ngrok or cloudflare tunnel to expose it")
    print("3. Configure Slack Event Subscriptions with the public URL")
    print("\n" + "="*60 + "\n")

    # Run Flask
    app.run(host='0.0.0.0', port=3000, debug=False)


if __name__ == "__main__":
    # Check if Flask is installed
    try:
        import flask
    except ImportError:
        print("\n[ERROR] Flask not installed")
        print("Run: pip install flask")
        sys.exit(1)

    main()
