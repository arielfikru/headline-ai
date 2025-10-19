#!/usr/bin/env python3
"""
Example usage of Headline Generator
"""

from headline_generator import HeadlineGenerator


def main():
    # Initialize the generator
    print("Initializing Headline Generator...")
    generator = HeadlineGenerator()

    # Example URLs (replace with actual news URLs)
    example_urls = [
        "https://www.detik.com/terbaru",
        "https://www.kompas.com/",
        # Add more URLs here
    ]

    print("\n" + "="*60)
    print("HEADLINE AI - Example Usage")
    print("="*60)

    # You can use this script in multiple ways:

    # Method 1: Generate from a single URL
    print("\n1. Single URL Generation:")
    url = input("Enter article URL: ").strip()

    if url:
        try:
            output = generator.generate_post(url)
            print(f"\n✓ Success! Post saved to: {output}")
        except Exception as e:
            print(f"\n✗ Error: {e}")

    # Method 2: Batch processing (uncomment to use)
    """
    print("\n2. Batch Processing:")
    for i, url in enumerate(example_urls, 1):
        try:
            print(f"\nProcessing {i}/{len(example_urls)}: {url}")
            output = generator.generate_post(url, f"post_{i}.png")
            print(f"✓ Saved: {output}")
        except Exception as e:
            print(f"✗ Failed: {e}")
    """

    print("\n" + "="*60)
    print("Check the 'output' folder for generated posts!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
