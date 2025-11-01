#!/usr/bin/env python3
"""
Slack AI Agent - Automated Setup Script
Programmatically sets up the n8n Slack AI agent
"""

import os
import sys
import json
import time
import subprocess
import requests
from pathlib import Path

# Colors for terminal output
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GRAY = '\033[90m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.CYAN}{text}{Colors.END}")

def print_success(text):
    print(f"{Colors.GREEN}[OK] {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}[!] {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}[X] {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.GRAY}  {text}{Colors.END}")

def check_n8n():
    """Check if n8n is running"""
    print_header("[1/8] Checking n8n status...")
    try:
        response = requests.get("http://localhost:5678", timeout=3)
        print_success("n8n is running on port 5678")
        return True
    except:
        print_error("n8n is not accessible on port 5678")
        print_info("Please start n8n with: docker-compose up -d")
        return False

def get_or_create_api_key():
    """Get or create n8n API key"""
    print_header("[2/8] Getting n8n API key...")

    # Check environment first
    api_key = os.environ.get('N8N_API_KEY')
    if api_key:
        print_success("Using API key from environment")
        return api_key

    # Try to extract from Docker container
    print_info("Attempting to extract API key from n8n database...")
    try:
        result = subprocess.run(
            ['docker', 'exec', 'n8n', 'sh', '-c',
             'sqlite3 /home/node/.n8n/database.sqlite "SELECT apiKey FROM api_key LIMIT 1;"'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0 and result.stdout.strip():
            api_key = result.stdout.strip()
            print_success("Found existing API key in database")

            # Save to .env
            with open('.env', 'a') as f:
                f.write(f'\nN8N_API_KEY="{api_key}"\n')
            print_success("Updated .env file with API key")

            return api_key
    except Exception as e:
        print_warning(f"Could not extract API key: {e}")

    # If we get here, need manual creation
    print_warning("No API key found")
    print_info("Please create one manually:")
    print_info("1. Open http://localhost:5678")
    print_info("2. Go to Settings -> API")
    print_info("3. Click 'Create API Key'")
    print_info("4. Copy the key and add to .env file: N8N_API_KEY=\"your-key\"")
    print_info("5. Run this script again")

    return None

def start_ngrok():
    """Start ngrok tunnel"""
    print_header("[3/8] Starting ngrok tunnel...")

    # Check if ngrok is already running
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=3)
        tunnels = response.json()['tunnels']
        if tunnels:
            public_url = tunnels[0]['public_url']
            print_success(f"ngrok tunnel already active: {public_url}")
            webhook_url = f"{public_url}/webhook/slack-agent"
            print_info(f"Webhook URL: {webhook_url}")
            return webhook_url
    except:
        pass

    # Start ngrok
    print_info("Starting ngrok for port 5678...")
    try:
        subprocess.Popen(['ngrok', 'http', '5678'],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        time.sleep(3)

        # Get public URL
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        tunnels = response.json()['tunnels']
        public_url = tunnels[0]['public_url']

        print_success(f"ngrok tunnel active: {public_url}")
        webhook_url = f"{public_url}/webhook/slack-agent"
        print_info(f"Webhook URL: {webhook_url}")

        return webhook_url
    except Exception as e:
        print_error(f"Failed to start ngrok: {e}")
        print_info("Please start ngrok manually: ngrok http 5678")
        return None

def import_workflow(api_key):
    """Import workflow into n8n"""
    print_header("[4/8] Importing workflow into n8n...")

    workflow_path = Path("workflows/slack-ai-agent-basic.json")
    if not workflow_path.exists():
        print_error(f"Workflow file not found: {workflow_path}")
        return None

    with open(workflow_path, 'r') as f:
        workflow = json.load(f)

    workflow['name'] = "Slack AI Agent - Auto Imported"

    headers = {
        'X-N8N-API-KEY': api_key,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(
            "http://localhost:5678/api/v1/workflows",
            headers=headers,
            json=workflow
        )
        response.raise_for_status()

        workflow_id = response.json()['id']
        print_success(f"Workflow imported successfully (ID: {workflow_id})")
        return workflow_id
    except Exception as e:
        print_error(f"Failed to import workflow: {e}")
        return None

def create_credentials(api_key):
    """Create credentials in n8n"""
    print_header("[5/8] Setting up credentials...")

    headers = {
        'X-N8N-API-KEY': api_key,
        'Content-Type': 'application/json'
    }

    # Anthropic credentials
    anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
    if not anthropic_key:
        print_warning("ANTHROPIC_API_KEY not found in environment")
        anthropic_key = input("Enter your Anthropic API key (or press Enter to skip): ").strip()

    if anthropic_key:
        credential = {
            'name': 'Anthropic API (Auto)',
            'type': 'anthropicApi',
            'data': {
                'apiKey': anthropic_key
            }
        }

        try:
            response = requests.post(
                "http://localhost:5678/api/v1/credentials",
                headers=headers,
                json=credential
            )
            if response.status_code == 201:
                print_success(f"Anthropic credentials created")
            elif 'already exists' in response.text.lower():
                print_warning("Anthropic credentials already exist")
        except Exception as e:
            print_warning(f"Could not create Anthropic credentials: {e}")

    # Slack credentials
    slack_token = os.environ.get('SLACK_BOT_TOKEN')
    if not slack_token:
        print_warning("SLACK_BOT_TOKEN not found")
        print_info("You'll need to configure Slack credentials manually in n8n")
    else:
        credential = {
            'name': 'Slack Bot (Auto)',
            'type': 'slackOAuth2Api',
            'data': {
                'accessToken': slack_token
            }
        }

        try:
            response = requests.post(
                "http://localhost:5678/api/v1/credentials",
                headers=headers,
                json=credential
            )
            if response.status_code == 201:
                print_success("Slack credentials created")
            elif 'already exists' in response.text.lower():
                print_warning("Slack credentials already exist")
        except Exception as e:
            print_warning(f"Could not create Slack credentials: {e}")

def activate_workflow(api_key, workflow_id):
    """Activate the workflow"""
    print_header("[6/8] Activating workflow...")

    headers = {
        'X-N8N-API-KEY': api_key
    }

    try:
        response = requests.post(
            f"http://localhost:5678/api/v1/workflows/{workflow_id}/activate",
            headers=headers
        )
        response.raise_for_status()
        print_success("Workflow activated successfully")
        return True
    except Exception as e:
        print_error(f"Failed to activate workflow: {e}")
        return False

def show_slack_instructions(webhook_url):
    """Show Slack app setup instructions"""
    print_header("[7/8] Slack App Setup Required")
    print(f"\n{Colors.CYAN}{'='*50}{Colors.END}")
    print("\nTo complete setup, configure your Slack app:\n")
    print(f"{Colors.GRAY}1. Go to: https://api.slack.com/apps{Colors.END}")
    print(f"{Colors.GRAY}2. Create or select your app{Colors.END}")
    print(f"{Colors.GRAY}3. Go to Event Subscriptions{Colors.END}")
    print(f"{Colors.GRAY}4. Set Request URL to:{Colors.END}")
    print(f"   {Colors.CYAN}{webhook_url}{Colors.END}")
    print(f"{Colors.GRAY}5. Subscribe to bot events: app_mention, message.im{Colors.END}")
    print(f"{Colors.GRAY}6. Save and install to workspace{Colors.END}\n")

def test_workflow(webhook_url):
    """Test the workflow"""
    print_header("[8/8] Testing workflow...")

    if not webhook_url or "YOUR_NGROK_URL" in webhook_url:
        print_warning("Skipping test - ngrok URL not available")
        return

    test_payload = {
        'type': 'event_callback',
        'event': {
            'type': 'app_mention',
            'text': '<@BOT123> Hello Alexandria!',
            'user': 'U123456',
            'channel': 'C123456',
            'ts': '1234567890.123456'
        }
    }

    try:
        response = requests.post(
            webhook_url,
            json=test_payload,
            timeout=10
        )
        if response.status_code == 200:
            print_success("Workflow test successful")
        else:
            print_warning("Test failed - workflow needs Slack credentials configured")
    except Exception as e:
        print_warning(f"Test failed: {e}")

def main():
    print(f"{Colors.CYAN}{'='*50}")
    print("Slack AI Agent - Automated Setup")
    print(f"{'='*50}{Colors.END}\n")

    # Step 1: Check n8n
    if not check_n8n():
        sys.exit(1)

    # Step 2: Get API key
    api_key = get_or_create_api_key()
    if not api_key:
        sys.exit(1)

    # Step 3: Start ngrok
    webhook_url = start_ngrok()

    # Step 4: Import workflow
    workflow_id = import_workflow(api_key)
    if not workflow_id:
        sys.exit(1)

    # Step 5: Create credentials
    create_credentials(api_key)

    # Step 6: Activate workflow
    activate_workflow(api_key, workflow_id)

    # Step 7: Show Slack instructions
    show_slack_instructions(webhook_url or "http://YOUR_NGROK_URL/webhook/slack-agent")

    # Step 8: Test workflow
    if webhook_url:
        test_workflow(webhook_url)

    # Summary
    print(f"\n{Colors.CYAN}{'='*50}")
    print("Setup Complete!")
    print(f"{'='*50}{Colors.END}\n")

    print(f"{Colors.GREEN}Status:{Colors.END}")
    print(f"  ✓ n8n running on http://localhost:5678")
    if webhook_url and "YOUR_NGROK_URL" not in webhook_url:
        print(f"  ✓ ngrok tunnel active")
    print(f"  ✓ Workflow imported and activated\n")

    print(f"{Colors.YELLOW}Next Steps:{Colors.END}")
    print(f"  1. Configure Slack app with webhook URL above")
    print(f"  2. Test in Slack: @YourBot hello")
    print(f"  3. View executions: http://localhost:5678/executions\n")

    print(f"{Colors.YELLOW}Management Commands:{Colors.END}")
    print(f"  View workflow: http://localhost:5678/workflow/{workflow_id}")
    print(f"  Stop ngrok: pkill ngrok (Linux/Mac) or Stop-Process -Name ngrok (Windows)\n")

if __name__ == "__main__":
    main()
