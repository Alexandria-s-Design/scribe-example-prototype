#!/usr/bin/env python3
"""
Alexandria - Slack AI Bot using Zapier MCP + Grok 4
Direct integration - no guides needed!
"""

import os
import sys
import json
import requests
import time
from datetime import datetime

# Configuration
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
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
            return f"Error calling Grok: {response.status_code}"

    except Exception as e:
        return f"Exception: {str(e)}"


def send_slack_message(channel, text, thread_ts=None):
    """Send message to Slack using Slack API"""
    try:
        payload = {
            "channel": channel,
            "text": text
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

        result = response.json()
        if result.get("ok"):
            return True
        else:
            print(f"Slack error: {result.get('error')}")
            return False

    except Exception as e:
        print(f"Exception sending to Slack: {e}")
        return False


def get_slack_mentions(since_minutes=5):
    """Get recent mentions of the bot"""
    try:
        # Get bot user ID
        auth_response = requests.get(
            "https://slack.com/api/auth.test",
            headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
            timeout=10
        )
        bot_id = auth_response.json().get("user_id")

        # Search for mentions
        oldest = int(time.time()) - (since_minutes * 60)

        response = requests.get(
            "https://slack.com/api/search.messages",
            headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
            params={
                "query": f"<@{bot_id}>",
                "sort": "timestamp",
                "sort_dir": "desc",
                "count": 10
            },
            timeout=10
        )

        result = response.json()
        if result.get("ok"):
            messages = result.get("messages", {}).get("matches", [])
            return [m for m in messages if float(m.get("ts", 0)) > oldest]
        else:
            print(f"Search error: {result.get('error')}")
            return []

    except Exception as e:
        print(f"Exception getting mentions: {e}")
        return []


def process_message(message):
    """Process a single mention"""
    try:
        text = message.get("text", "")
        channel = message.get("channel", {}).get("id", "")
        ts = message.get("ts", "")

        # Clean up the mention
        import re
        clean_text = re.sub(r'<@[A-Z0-9]+>', '', text).strip()

        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Processing: {clean_text}")

        # Call Grok
        print("  → Calling Grok 4...")
        response = call_grok(clean_text)

        # Send to Slack
        print(f"  → Sending response to Slack...")
        success = send_slack_message(channel, response, thread_ts=ts)

        if success:
            print(f"  ✓ Response sent!")
        else:
            print(f"  ✗ Failed to send")

        return success

    except Exception as e:
        print(f"Error processing message: {e}")
        return False


def monitor_mode():
    """Continuous monitoring mode"""
    print("="*60)
    print("Alexandria - Slack AI Bot (Zapier MCP + Grok 4)")
    print("="*60)
    print("\nMonitoring Slack mentions...")
    print("Press Ctrl+C to stop\n")

    processed = set()

    try:
        while True:
            # Get recent mentions
            mentions = get_slack_mentions(since_minutes=2)

            # Process new mentions
            for msg in mentions:
                msg_id = msg.get("ts")
                if msg_id and msg_id not in processed:
                    process_message(msg)
                    processed.add(msg_id)

            # Wait before checking again
            time.sleep(10)

    except KeyboardInterrupt:
        print("\n\nStopping Alexandria...\n")


def test_mode(test_message="What is our revenue goal?"):
    """Test mode - single message"""
    print("="*60)
    print("Alexandria - Test Mode")
    print("="*60)
    print(f"\nTest message: {test_message}\n")

    # Call Grok
    print("Calling Grok 4...")
    response = call_grok(test_message)

    print("\n" + "-"*60)
    print("Alexandria's Response:")
    print("-"*60)
    print(response)
    print("-"*60 + "\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            test_mode()
        elif sys.argv[1] == "monitor":
            monitor_mode()
        else:
            print("Usage:")
            print("  python alexandria_slack_bot.py test     - Test Grok response")
            print("  python alexandria_slack_bot.py monitor  - Monitor Slack mentions")
    else:
        # Default: monitor mode
        monitor_mode()
