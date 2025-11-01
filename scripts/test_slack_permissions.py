#!/usr/bin/env python3
"""Test Slack API permissions"""

import os
import requests

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")

print("Testing Slack API connection...\n")

# Test 1: Auth test
print("1. Testing authentication...")
response = requests.get(
    "https://slack.com/api/auth.test",
    headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
)
result = response.json()
if result.get("ok"):
    print(f"   [OK] Authenticated as: {result.get('user')}")
    print(f"   [OK] Bot ID: {result.get('user_id')}")
    print(f"   [OK] Team: {result.get('team')}")
else:
    print(f"   [FAIL] Auth failed: {result.get('error')}")

# Test 2: Check scopes
print("\n2. Checking bot scopes...")
scopes_response = requests.get(
    "https://slack.com/api/auth.test",
    headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
)
if scopes_response.ok:
    print(f"   Token type: {scopes_response.json().get('url', 'N/A')}")

# Test 3: Try to search messages
print("\n3. Testing search permissions...")
search_response = requests.get(
    "https://slack.com/api/search.messages",
    headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
    params={"query": "test", "count": 1}
)
search_result = search_response.json()
if search_result.get("ok"):
    print("   [OK] Search works!")
else:
    print(f"   [FAIL] Search failed: {search_result.get('error')}")
    print("   -> This might be why the bot can't see mentions")

# Test 4: Try to post a test message
print("\n4. Testing posting capability...")
print("   (Skipping actual post to avoid spam)")

print("\n" + "="*60)
print("DIAGNOSIS:")
print("="*60)
if not search_result.get("ok"):
    print("[X] PROBLEM: Bot can't search messages")
    print("\nSOLUTION NEEDED:")
    print("The Slack bot token needs 'search:read' scope")
    print("\nFix at: https://api.slack.com/apps")
    print("1. Find your app ('Slacking')")
    print("2. OAuth & Permissions")
    print("3. Add 'search:read' scope")
    print("4. Reinstall app to workspace")
else:
    print("[OK] All permissions look good!")
    print("Issue might be elsewhere...")
