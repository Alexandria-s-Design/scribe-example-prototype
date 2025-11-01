#!/usr/bin/env python3
"""
Alexandria - Slack AI Bot using Event-based approach
Works with Zapier MCP + Grok 4
"""

import os
import sys
import json
import requests
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Configuration
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
            return f"Error: {response.status_code}"

    except Exception as e:
        return f"Exception: {str(e)}"


def send_slack_message(channel, text, thread_ts=None):
    """Send message to Slack"""
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
        return result.get("ok", False)

    except Exception as e:
        print(f"Error sending to Slack: {e}")
        return False


def check_manual_mentions():
    """
    Manual polling approach using Zapier MCP
    This is the simplified version that works
    """
    print("\n" + "="*60)
    print("Alexandria - Manual Testing Mode")
    print("="*60)
    print("\nInstructions:")
    print("1. Go to Slack")
    print("2. Type: @Slacking [your message]")
    print("3. Copy the CHANNEL ID and MESSAGE")
    print("4. Paste them here")
    print("\nTo find Channel ID:")
    print("- Right-click channel name")
    print("- 'View channel details'")
    print("- Scroll down to see Channel ID")
    print("\n" + "="*60)

    try:
        channel = input("\nEnter Channel ID: ").strip()
        message = input("Enter your message: ").strip()

        if not channel or not message:
            print("Invalid input!")
            return

        print(f"\nProcessing: {message}")
        print("Calling Grok 4...")

        response = call_grok(message)

        print("\n" + "-"*60)
        print("Alexandria's Response:")
        print("-"*60)
        print(response)
        print("-"*60)

        send = input("\nSend this to Slack? (y/n): ").strip().lower()
        if send == 'y':
            print("Sending to Slack...")
            success = send_slack_message(channel, response)
            if success:
                print("[OK] Message sent!")
            else:
                print("[FAIL] Could not send message")

    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"Error: {e}")


def interactive_mode():
    """Interactive chat mode (no Slack)"""
    print("\n" + "="*60)
    print("Alexandria - Interactive Mode")
    print("="*60)
    print("Chat with Alexandria (type 'quit' to exit)")
    print("="*60 + "\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break

            if not user_input:
                continue

            print("Alexandria: ", end="", flush=True)
            response = call_grok(user_input)
            print(response + "\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


def test_mode():
    """Simple test"""
    print("\n" + "="*60)
    print("Alexandria - Test Mode")
    print("="*60 + "\n")

    test_message = "What is our revenue goal?"
    print(f"Test: {test_message}\n")
    print("Calling Grok 4...")

    response = call_grok(test_message)

    print("\n" + "-"*60)
    print("Response:")
    print("-"*60)
    print(response)
    print("-"*60 + "\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Alexandria - Slack AI Bot")
    print("="*60)
    print("\nModes:")
    print("1. test      - Test Grok connection")
    print("2. chat      - Interactive chat (no Slack)")
    print("3. manual    - Manual Slack posting")
    print("="*60 + "\n")

    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        mode = input("Choose mode (test/chat/manual): ").strip().lower()

    if mode == "test":
        test_mode()
    elif mode == "chat":
        interactive_mode()
    elif mode == "manual":
        check_manual_mentions()
    else:
        print(f"Unknown mode: {mode}")
        print("Use: test, chat, or manual")
