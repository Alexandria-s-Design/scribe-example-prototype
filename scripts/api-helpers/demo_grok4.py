#!/usr/bin/env python3
"""Demo script showing Grok 4 capabilities."""

from grok_helper import GrokHelper

def main():
    print("=" * 60)
    print("GROK 4 DEMO - Alexandria's Design")
    print("=" * 60)

    helper = GrokHelper()

    print("\n[1] Testing Grok 4 with a practical Alexandria's Design query...")
    print("-" * 60)

    query = """
    What are the key trends in K-12 AI literacy education that emerged in 2024?
    Focus on professional development approaches for teachers.
    Provide 3 specific trends with brief descriptions.
    """

    print(f"Query: {query.strip()}")
    print("\nGrok 4 Response:")
    print("-" * 60)

    response = helper.simple_chat(query.strip())
    print(response)

    print("\n" + "=" * 60)
    print("[2] Model Information")
    print("-" * 60)

    info = helper.get_model_info()
    print(f"\nAvailable Models: {len(info['models'])}")
    for model in info['models']:
        print(f"  - {model}")

    print(f"\nPricing:")
    print(f"  - Input: {info['pricing']['input']}")
    print(f"  - Output: {info['pricing']['output']}")
    print(f"  - Cached: {info['pricing']['cached']}")

    print(f"\nKey Capabilities:")
    for cap in info['capabilities'][:4]:
        print(f"  - {cap}")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE - Grok 4 is ready for Alexandria's Design!")
    print("=" * 60)

if __name__ == "__main__":
    main()
