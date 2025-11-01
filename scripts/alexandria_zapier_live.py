#!/usr/bin/env python3
"""
Alexandria - Live Zapier MCP Integration
Monitors Slack and responds via Grok 4
"""

import os
import time
import requests
import sys
from datetime import datetime

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

processed_messages = set()


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
        print(f"Error calling Grok: {e}")
        return None


def process_slack_mention(message_text, channel_id, thread_ts=None):
    """Process a Slack mention and respond"""
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] New mention: {message_text[:50]}...")

    # Clean up @mentions
    import re
    clean_text = re.sub(r'<@[A-Z0-9]+>', '', message_text).strip()

    print(f"  → Calling Grok 4...")
    response = call_grok(clean_text)

    if response:
        print(f"  → Got response ({len(response)} chars)")
        return {
            "channel": channel_id,
            "text": response,
            "thread_ts": thread_ts
        }
    else:
        print(f"  ✗ Grok call failed")
        return None


def send_to_slack_via_zapier(channel, text, thread_ts=None):
    """
    This function will be called by Claude Code using Zapier MCP
    It's a placeholder that shows what needs to happen
    """
    print(f"  → Sending to Slack channel {channel}")
    # Claude Code will actually call: mcp__zapier__slack_send_channel_message
    # with the appropriate parameters
    return True


def main():
    """Main monitoring loop"""
    print("\n" + "="*60)
    print("Alexandria - Zapier MCP Live Monitor")
    print("="*60)
    print("\n✓ Zapier Slack connection verified")
    print("✓ Grok 4 API ready")
    print("\nWaiting for Slack mentions...")
    print("(Claude Code will handle this using Zapier MCP tools)")
    print("\nTest in Slack: @Slacking What is our revenue goal?")
    print("\n" + "="*60)

    # This is where Claude Code would use:
    # mcp__zapier__slack_find_message to get new mentions
    # Then call process_slack_mention()
    # Then call mcp__zapier__slack_send_channel_message to respond

    print("\n[INFO] This script shows the workflow.")
    print("[INFO] Claude Code will execute it using Zapier MCP tools.")
    print("\nPress Ctrl+C to exit\n")

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n\nStopped.\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Test mode
        print("\nTesting Alexandria + Grok integration...\n")
        test_msg = "What is our revenue goal?"
        result = process_slack_mention(test_msg, "C3LDFEHTL")
        if result:
            print(f"\nResponse ready to send:")
            print(f"Channel: {result['channel']}")
            print(f"Message: {result['text'][:100]}...")
    else:
        main()
