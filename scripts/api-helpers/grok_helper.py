#!/usr/bin/env python3
"""
Grok API Helper - Access xAI's Grok 4 models

Provides access to xAI's Grok 4 language models:
- Grok 4 (latest, most capable - 256K context window)
- Grok 4 Fast (2M token context, reasoning/non-reasoning variants)
- Grok Vision Beta (vision capabilities)
- Real-time information access (knowledge cutoff: November 2024)

Setup:
    pip install openai  # Grok uses OpenAI-compatible API
    Set GROK_API_KEY or XAI_API_KEY in .env file

API Documentation:
    https://docs.x.ai/api

Usage from Claude Code:
    Claude will ask: "Would you like to use Grok 4 for [task]?"
    Available for: real-time info, reasoning, vision, code generation
"""

import os
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GrokHelper:
    """Helper class for xAI Grok API operations."""

    # Available Grok 4 models
    AVAILABLE_MODELS = [
        "grok-4",  # Main Grok 4 model (alias for grok-4-0709)
        "grok-4-0709",  # Grok 4 with specific version
        "grok-vision-beta",  # Vision-specific model
        "grok-4-fast-reasoning",  # Fast model with reasoning (2M context)
        "grok-4-fast-non-reasoning",  # Fast model without reasoning (2M context)
    ]

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Grok client.

        Args:
            api_key: Optional API key. If not provided, reads from GROK_API_KEY or XAI_API_KEY env var
        """
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("OpenAI library not installed. Run: pip install openai")

        self.api_key = api_key or os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY")
        if not self.api_key:
            raise ValueError("GROK_API_KEY or XAI_API_KEY not found in environment variables or .env file")

        self.client = OpenAI(
            base_url="https://api.x.ai/v1",
            api_key=self.api_key
        )

    # ==================== CHAT COMPLETIONS ====================

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "grok-4",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """Chat completion using Grok models.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model ID (see AVAILABLE_MODELS)
            temperature: 0.0-2.0 (lower = more focused)
            max_tokens: Maximum tokens in response
            stream: Enable streaming responses

        Returns:
            Response dict with 'content', 'model', and usage info
        """
        print(f"[*] Using Grok model: {model}")

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream
        )

        if stream:
            return response  # Return stream object

        return {
            "content": response.choices[0].message.content,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            "finish_reason": response.choices[0].finish_reason
        }

    def simple_chat(self, user_message: str, model: str = "grok-4") -> str:
        """Simple one-shot chat interaction.

        Args:
            user_message: The user's message
            model: Model to use

        Returns:
            Grok's response text
        """
        messages = [{"role": "user", "content": user_message}]
        response = self.chat(messages, model=model)
        return response["content"]

    # ==================== VISION CAPABILITIES ====================

    def analyze_image(
        self,
        image_url: str,
        prompt: str = "Describe this image in detail",
        model: str = "grok-vision-beta"
    ) -> str:
        """Analyze an image using Grok's vision capabilities.

        Args:
            image_url: URL to image (can be data URL or web URL)
            prompt: Question about the image
            model: Vision-capable model

        Returns:
            Analysis text
        """
        print(f"[*] Using Grok Vision: {model}")

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ]
        )

        return response.choices[0].message.content

    # ==================== STREAMING ====================

    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        model: str = "grok-4",
        temperature: float = 0.7
    ):
        """Stream chat responses in real-time.

        Args:
            messages: List of message dicts
            model: Model to use
            temperature: Temperature setting

        Yields:
            Text chunks as they arrive
        """
        print(f"[*] Streaming from Grok: {model}")

        stream = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    # ==================== UTILITY FUNCTIONS ====================

    def list_models(self) -> List[str]:
        """Get list of available Grok models.

        Returns:
            List of model IDs
        """
        return self.AVAILABLE_MODELS.copy()

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about Grok models.

        Returns:
            Dict with model info and capabilities
        """
        return {
            "models": self.AVAILABLE_MODELS,
            "capabilities": [
                "Advanced reasoning and problem-solving",
                "Real-time information access (knowledge cutoff: Nov 2024)",
                "Vision analysis (grok-vision-beta)",
                "Code generation and debugging",
                "Long context understanding (256K tokens, 2M for fast models)",
                "Native tool use integration",
                "Streaming responses"
            ],
            "pricing": {
                "input": "$3 per 1M tokens",
                "output": "$15 per 1M tokens",
                "cached": "$0.75 per 1M tokens"
            },
            "api_docs": "https://docs.x.ai/api",
            "base_url": "https://api.x.ai/v1"
        }

    def test_connection(self) -> bool:
        """Test if API key is valid and connection works.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.simple_chat("Say 'Connection successful' if you can read this.")
            print(f"[SUCCESS] Connection test passed!")
            print(f"Response: {response}")
            return True
        except Exception as e:
            print(f"[ERROR] Connection test failed: {e}")
            return False


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("Grok API Helper - Testing Connection")
    print("=" * 60)

    try:
        helper = GrokHelper()

        print("\n📋 Available Grok Models:")
        for model in helper.list_models():
            print(f"  • {model}")

        print("\n🔧 Capabilities:")
        info = helper.get_model_info()
        for capability in info["capabilities"]:
            print(f"  ✓ {capability}")

        print("\n🧪 Testing Connection...")
        if helper.test_connection():
            print("\n✅ Grok API is ready to use!")

            # Simple test query
            print("\n💬 Test Query: What is xAI?")
            response = helper.simple_chat("In one sentence, what is xAI?")
            print(f"Response: {response}")

        else:
            print("\n❌ Connection failed. Check your API key.")

    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nSetup Instructions:")
        print("1. Get API key from: https://console.x.ai/")
        print("2. Add to .env file:")
        print("   GROK_API_KEY=your_api_key_here")
        print("   or")
        print("   XAI_API_KEY=your_api_key_here")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")

    print("\n" + "=" * 60)
