#!/usr/bin/env python3
"""Simple test script for Grok API without emoji issues."""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from grok_helper import GrokHelper

def main():
    print("=" * 60)
    print("Grok API Test")
    print("=" * 60)

    try:
        # Initialize helper
        helper = GrokHelper()
        print("\n[+] Grok client initialized")

        # Show available models
        print("\nAvailable Models:")
        for model in helper.list_models():
            print(f"  - {model}")

        # Test connection
        print("\n[*] Testing connection...")
        response = helper.simple_chat("In one sentence, what is xAI?")

        print("\n[SUCCESS] Connection test passed!")
        print(f"\nGrok's Response:")
        print(f"  {response}")

        # Get model capabilities
        print("\n" + "=" * 60)
        info = helper.get_model_info()
        print("Capabilities:")
        for capability in info["capabilities"]:
            print(f"  [+] {capability}")

        print("\n[READY] Grok API is configured and working!")
        print("=" * 60)

    except ValueError as e:
        print(f"\n[ERROR] Configuration issue: {e}")
        print("\nSetup Instructions:")
        print("1. Get API key from: https://console.x.ai/")
        print("2. Add to .env file:")
        print("   GROK_API_KEY=your_api_key_here")
        return False
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
