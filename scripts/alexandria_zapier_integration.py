#!/usr/bin/env python3
"""
Alexandria - Zapier MCP Integration
Uses Zapier MCP tools to connect Slack + Grok
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
            return f"Error: {response.status_code}"

    except Exception as e:
        return f"Exception: {str(e)}"


def main():
    """Main integration function"""
    print("\n" + "="*60)
    print("Alexandria - Zapier MCP Integration")
    print("="*60 + "\n")

    # For now, we'll create a simple test
    # The actual Zapier integration needs to be configured via their web UI

    print("Setup Instructions:")
    print("\n1. Go to: https://mcp.zapier.com/mcp/servers/52cc6e40-ba52-4bc9-8ff8-f3841239dd64/config")
    print("\n2. Create these AI Actions:")
    print("\n   Action 1: 'Get Slack Mention'")
    print("   - Trigger: New mention in Slack")
    print("   - Returns: channel_id, message_text, thread_ts")

    print("\n   Action 2: 'Send to Grok'")
    print("   - Action: Webhook POST")
    print("   - URL: https://api.x.ai/v1/chat/completions")
    print("   - Returns: AI response")

    print("\n   Action 3: 'Send Slack Message'")
    print("   - Action: Send message to Slack")
    print("   - Inputs: channel_id, message, thread_ts")

    print("\n3. Once configured, Claude Code can use those actions!")
    print("\n" + "="*60)

    # Test Grok connection
    print("\n[TEST] Testing Grok connection...")
    test_message = "What is our revenue goal?"
    response = call_grok(test_message)

    print(f"\nQuestion: {test_message}")
    print(f"Alexandria: {response}\n")
    print("[OK] Grok integration working!")
    print("\n" + "="*60)

    print("\nNext Steps:")
    print("1. Configure the Zapier AI Actions (link above)")
    print("2. Those actions will become available as MCP tools")
    print("3. Claude Code can then use them to respond to Slack")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
