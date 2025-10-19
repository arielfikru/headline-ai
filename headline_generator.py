#!/usr/bin/env python3
"""
Headline AI - Generate social media posts from news articles
"""

import os
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from urllib.parse import urlparse, urljoin
from dotenv import load_dotenv
from openai import OpenAI
import json

# Load environment variables
load_dotenv()

# Import all configuration
import config


class HeadlineGenerator:
    def __init__(self):
        """Initialize the Headline Generator with Gemini API"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")

        # Initialize OpenAI client for Gemini
        self.client = OpenAI(
            api_key=api_key,
            base_url=config.GEMINI_BASE_URL
        )
        self.model = config.GEMINI_MODEL

        # Create output directory
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        os.makedirs(config.TEMP_DIR, exist_ok=True)

    def fetch_article_content(self, url):
        """Fetch HTML content from URL"""
        print(f"Fetching article from: {url}")
        headers = {
            'User-Agent': config.USER_AGENT
        }
        response = requests.get(url, headers=headers, timeout=config.REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.text

    def extract_images_from_html(self, html_content, base_url):
        """Extract all possible images from HTML using BeautifulSoup"""
        soup = BeautifulSoup(html_content, 'html.parser')
        image_urls = []

        # Priority 1: Open Graph image
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            image_urls.append(og_image['content'])

        # Priority 2: Twitter card image
        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        if twitter_image and twitter_image.get('content'):
            image_urls.append(twitter_image['content'])

        # Priority 3: Article images
        article_imgs = soup.select('article img, .article img, .content img, .post-content img')
        for img in article_imgs[:config.MAX_ARTICLE_IMAGES]:
            if img.get('src'):
                image_urls.append(img['src'])
            elif img.get('data-src'):  # Lazy loaded images
                image_urls.append(img['data-src'])

        # Priority 4: All images with reasonable size attributes
        all_imgs = soup.find_all('img')
        for img in all_imgs[:config.MAX_GENERAL_IMAGES]:
            if img.get('src'):
                # Skip small images (icons, logos, etc)
                width = img.get('width', '0')
                height = img.get('height', '0')
                try:
                    if width and height:
                        if int(width) > 200 and int(height) > 200:
                            image_urls.append(img['src'])
                    else:
                        image_urls.append(img['src'])
                except:
                    image_urls.append(img['src'])

        # Make URLs absolute
        absolute_urls = []
        for url in image_urls:
            if url.startswith('http'):
                absolute_urls.append(url)
            else:
                absolute_urls.append(urljoin(base_url, url))

        # Remove duplicates while preserving order
        seen = set()
        unique_urls = []
        for url in absolute_urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)

        return unique_urls

    def extract_content_with_gemini(self, html_content, url, style="clickbait"):
        """Use Gemini to extract article content, title, and image URL

        Args:
            html_content: HTML content of the article
            url: Article URL
            style: Headline style (clickbait, formal, casual, question, storytelling)
        """
        print(f"Analyzing article content with Gemini (Style: {style})...")

        # First extract images using BeautifulSoup
        image_candidates = self.extract_images_from_html(html_content, url)
        print(f"Found {len(image_candidates)} image candidates")

        # Truncate HTML if too long
        if len(html_content) > config.MAX_HTML_LENGTH:
            html_content = html_content[:config.MAX_HTML_LENGTH] + "..."

        # Get style config
        if style not in config.HEADLINE_STYLES:
            print(f"Warning: Style '{style}' not found, using default")
            style = config.DEFAULT_HEADLINE_STYLE

        style_config = config.HEADLINE_STYLES[style]

        # Use prompt template from selected style
        prompt = style_config["prompt"].format(
            url=url,
            html_content=html_content,
            max_title_length=config.MAX_TITLE_LENGTH
        )

        # Use temperature from style config
        temperature = style_config.get("temperature", config.GEMINI_TEMPERATURE)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
        )

        result_text = response.choices[0].message.content

        # Extract JSON from response
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(result_text)

            # Extract title from response (support multiple key names for compatibility)
            result['title'] = result.get('title', result.get('clickbait_title', 'Berita Terkini'))
            result['image_url'] = image_candidates[0] if image_candidates else None

            # Extract source from AI response, fallback to domain if not provided
            if 'source' not in result or not result['source']:
                # Fallback to domain parsing
                from urllib.parse import urlparse
                parsed_url = urlparse(url)
                result['source'] = parsed_url.netloc
            else:
                result['source'] = result['source']

        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            print(f"Response was: {result_text}")
            # Fallback: parse domain from URL
            from urllib.parse import urlparse
            parsed_url = urlparse(url)
            fallback_source = parsed_url.netloc

            result = {
                "title": "Berita Terkini yang Mengejutkan!",
                "summary": "Baca berita selengkapnya",
                "image_url": image_candidates[0] if image_candidates else None,
                "source": fallback_source,
            }

        return result

    def download_image(self, image_url):
        """Download image from URL with validation"""
        print(f"Downloading image from: {image_url}")
        headers = {
            'User-Agent': config.USER_AGENT,
            'Referer': image_url
        }

        try:
            response = requests.get(image_url, headers=headers, timeout=config.REQUEST_TIMEOUT, allow_redirects=True)
            response.raise_for_status()

            # Validate it's actually an image
            content_type = response.headers.get('content-type', '')
            if 'image' not in content_type.lower():
                print(f"Warning: URL doesn't appear to be an image (content-type: {content_type})")

            img = Image.open(BytesIO(response.content))

            # Validate image size
            if img.width < config.MIN_IMAGE_WIDTH or img.height < config.MIN_IMAGE_HEIGHT:
                print(f"Warning: Image too small ({img.width}x{img.height}), skipping...")
                return None

            return img
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None

    def create_default_image(self):
        """Create a default background image if no image is found"""
        print("Creating default background image...")
        # Create a gradient background
        img = Image.new('RGB', (config.IMAGE_WIDTH, config.IMAGE_HEIGHT), color='#1a1a1a')
        return img

    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            # Create a temporary draw object to measure text
            temp_img = Image.new('RGB', (1, 1))
            temp_draw = ImageDraw.Draw(temp_img)
            line_text = ' '.join(current_line)
            bbox = temp_draw.textbbox((0, 0), line_text, font=font)
            line_width = bbox[2] - bbox[0]

            if line_width > max_width:
                if len(current_line) == 1:
                    lines.append(current_line.pop())
                else:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def create_post_design_layout2(self, background_img, title, source_name, output_path, brand_text=None):
        """Create post design with Layout 2 - Modern gradient overlay style"""
        print("Creating post design (Layout 2 - Modern Gradient)...")

        # Resize and crop background image to fill canvas
        target_size = (config.IMAGE_WIDTH, config.IMAGE_HEIGHT)
        img_ratio = background_img.width / background_img.height
        target_ratio = target_size[0] / target_size[1]

        if img_ratio > target_ratio:
            new_height = target_size[1]
            new_width = int(new_height * img_ratio)
        else:
            new_width = target_size[0]
            new_height = int(new_width / img_ratio)

        background_img = background_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Crop to center
        left = (new_width - target_size[0]) // 2
        top = (new_height - target_size[1]) // 2
        background_img = background_img.crop((left, top, left + target_size[0], top + target_size[1]))

        # Convert to RGBA for overlay support
        background_img = background_img.convert('RGBA')

        # Create overlay layer
        overlay = Image.new('RGBA', target_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Load fonts
        try:
            title_font = ImageFont.truetype(config.TITLE_FONT_PATH, config.TITLE_FONT_SIZE)
            source_font = ImageFont.truetype(config.SOURCE_FONT_PATH, config.SOURCE_FONT_SIZE)
        except:
            title_font = ImageFont.load_default()
            source_font = ImageFont.load_default()

        # 1. Draw source logo/text at top right
        if source_name:
            source_bbox = draw.textbbox((0, 0), source_name, font=source_font)
            source_width = source_bbox[2] - source_bbox[0]
            source_x = config.IMAGE_WIDTH - source_width - config.LAYOUT2_BADGE_MARGIN
            source_y = config.LAYOUT2_BADGE_MARGIN

            draw.text(
                (source_x, source_y),
                source_name,
                fill=(255, 255, 255, 240),  # White with slight transparency
                font=source_font
            )

        # 2. Draw gradient overlay at bottom (taller and more opaque)
        gradient_height = config.LAYOUT2_GRADIENT_HEIGHT
        for i in range(gradient_height):
            # Create gradient from transparent to dark
            # More aggressive gradient curve for better opacity at top
            progress = i / gradient_height
            # Use power curve for more opacity earlier
            alpha = int((progress ** 0.7) * config.LAYOUT2_GRADIENT_COLOR[3])
            color = (config.LAYOUT2_GRADIENT_COLOR[0],
                    config.LAYOUT2_GRADIENT_COLOR[1],
                    config.LAYOUT2_GRADIENT_COLOR[2],
                    alpha)
            y_pos = config.IMAGE_HEIGHT - gradient_height + i
            draw.line([(0, y_pos), (config.IMAGE_WIDTH, y_pos)], fill=color, width=1)

        # 3. Draw headline text at bottom over gradient (positioned higher)
        max_width = config.IMAGE_WIDTH - (config.BOX_MARGIN * 2)
        wrapped_lines = self.wrap_text(title, title_font, max_width)

        # Calculate total text height
        total_height = len(wrapped_lines) * config.LINE_HEIGHT
        # Position text higher up in the gradient area
        start_y = config.IMAGE_HEIGHT - gradient_height + 80

        # Draw each line
        for i, line in enumerate(wrapped_lines):
            y = start_y + (i * config.LINE_HEIGHT)
            draw.text(
                (config.BOX_MARGIN, y),
                line,
                fill=config.LAYOUT2_TEXT_COLOR,
                font=title_font
            )

        # 4. Optional: Draw brand text at bottom left if provided
        if brand_text:
            brand_y = config.IMAGE_HEIGHT - config.BOX_MARGIN - 10
            draw.text(
                (config.BOX_MARGIN, brand_y),
                brand_text,
                fill=(255, 255, 255, 200),
                font=source_font
            )

        # Composite overlay onto background
        background_img = Image.alpha_composite(background_img, overlay)

        # Convert to RGB and save
        background_img = background_img.convert('RGB')
        background_img.save(output_path, config.OUTPUT_FORMAT, quality=config.OUTPUT_QUALITY)
        print(f"Post saved to: {output_path}")

    def create_post_design(self, background_img, title, source_name, output_path, brand_text=None, layout="layout1"):
        """Create the final post design with AI-extracted source name

        Args:
            layout: "layout1" (white box) or "layout2" (news update)
        """
        # Route to appropriate layout
        if layout == "layout2":
            return self.create_post_design_layout2(background_img, title, source_name, output_path, brand_text)

        # Default: Layout 1 (original white box design)
        print("Creating post design (Layout 1 - White Box)...")

        # Resize and crop background image
        target_size = (config.IMAGE_WIDTH, config.IMAGE_HEIGHT)

        # Calculate resize ratio to cover the entire canvas
        img_ratio = background_img.width / background_img.height
        target_ratio = target_size[0] / target_size[1]

        if img_ratio > target_ratio:
            # Image is wider, fit by height
            new_height = target_size[1]
            new_width = int(new_height * img_ratio)
        else:
            # Image is taller, fit by width
            new_width = target_size[0]
            new_height = int(new_width / img_ratio)

        background_img = background_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Crop to center
        left = (new_width - target_size[0]) // 2
        top = (new_height - target_size[1]) // 2
        right = left + target_size[0]
        bottom = top + target_size[1]
        background_img = background_img.crop((left, top, right, bottom))

        # Create a semi-transparent overlay
        overlay = Image.new('RGBA', target_size, config.OVERLAY_COLOR)
        background_img = background_img.convert('RGBA')
        background_img = Image.alpha_composite(background_img, overlay)

        # Create white box for text
        draw = ImageDraw.Draw(background_img)

        # Box dimensions from config
        box_left = config.BOX_MARGIN
        box_right = target_size[0] - config.BOX_MARGIN
        box_width = box_right - box_left

        # Try to load fonts, fallback to default if not available
        try:
            title_font = ImageFont.truetype(config.TITLE_FONT_PATH, config.TITLE_FONT_SIZE)
            source_font = ImageFont.truetype(config.SOURCE_FONT_PATH, config.SOURCE_FONT_SIZE)
        except:
            print("Custom fonts not found, using default...")
            title_font = ImageFont.load_default()
            source_font = ImageFont.load_default()

        # Wrap title text
        text_max_width = box_width - (config.BOX_PADDING * 2)
        wrapped_lines = self.wrap_text(title, title_font, text_max_width)

        # Calculate text height
        temp_img = Image.new('RGB', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        total_text_height = len(wrapped_lines) * config.LINE_HEIGHT

        # Position white box in lower third
        box_height = total_text_height + (config.BOX_PADDING * 2) + 80  # Extra space for source
        box_top = target_size[1] - box_height - config.BOX_MARGIN - 60
        box_bottom = box_top + box_height

        # Draw white box with rounded corners
        draw.rounded_rectangle(
            [box_left, box_top, box_right, box_bottom],
            radius=config.BOX_RADIUS,
            fill=config.WHITE_BOX_COLOR
        )

        # Draw text
        y_position = box_top + config.BOX_PADDING
        for line in wrapped_lines:
            draw.text(
                (box_left + config.BOX_PADDING, y_position),
                line,
                fill=config.TEXT_COLOR,
                font=title_font
            )
            y_position += config.LINE_HEIGHT

        # Conditional positioning based on SHOW_SOURCE and brand_text
        # Logic:
        # - Source ON + Brand ON  = Source kanan bawah, Brand kiri bawah
        # - Source OFF + Brand ON = Brand kanan bawah
        # - Source ON + Brand OFF = Source kanan bawah

        bottom_y = box_bottom - config.BOX_PADDING - 30

        if config.SHOW_SOURCE:
            # Show source attribution (AI-extracted source name, not domain)
            source_text = f"{config.SOURCE_TEXT}: {source_name}"
            source_bbox = draw.textbbox((0, 0), source_text, font=source_font)
            source_width = source_bbox[2] - source_bbox[0]
            source_x = box_right - config.BOX_PADDING - source_width

            draw.text(
                (source_x, bottom_y),
                source_text,
                fill=config.SOURCE_COLOR,
                font=source_font
            )

            # If brand text provided, show at bottom left
            if brand_text:
                brand_x = box_left + config.BOX_PADDING
                draw.text(
                    (brand_x, bottom_y),
                    brand_text,
                    fill=config.BRAND_COLOR,
                    font=source_font
                )

        else:
            # Source is OFF
            if brand_text:
                # Brand text takes the right position (where source would be)
                brand_bbox = draw.textbbox((0, 0), brand_text, font=source_font)
                brand_width = brand_bbox[2] - brand_bbox[0]
                brand_x = box_right - config.BOX_PADDING - brand_width

                draw.text(
                    (brand_x, bottom_y),
                    brand_text,
                    fill=config.BRAND_COLOR,
                    font=source_font
                )

        # Convert back to RGB and save
        background_img = background_img.convert('RGB')
        background_img.save(output_path, config.OUTPUT_FORMAT, quality=config.OUTPUT_QUALITY)
        print(f"Post saved to: {output_path}")

    def generate_post(self, url, output_filename=None, brand_text=None, style="clickbait", show_source=None, layout="layout1"):
        """Main method to generate post from URL

        Args:
            url: Article URL
            output_filename: Custom output filename (optional)
            brand_text: Brand text for bottom left (optional)
            style: Headline style - clickbait, formal, casual, question, storytelling
            show_source: Override SHOW_SOURCE config (True/False/None for default)
            layout: Layout style - "layout1" (white box) or "layout2" (news update)
        """
        try:
            # Get brand text from parameter, environment variable, or None
            if brand_text is None:
                brand_text = os.getenv("BRAND_TEXT", None)

            # Override show_source if specified
            original_show_source = config.SHOW_SOURCE
            if show_source is not None:
                config.SHOW_SOURCE = show_source

            # Fetch article
            html_content = self.fetch_article_content(url)

            # Extract content with Gemini using selected style
            article_data = self.extract_content_with_gemini(html_content, url, style=style)

            print(f"\nExtracted data:")
            print(f"Title: {article_data['title']}")
            print(f"Summary: {article_data.get('summary', 'N/A')}")
            print(f"Source: {article_data.get('source', 'N/A')}")

            # Get source from AI extraction (Gemini determines the source name)
            source_name = article_data.get('source', 'Unknown Source')

            # Try to download image from candidates
            background_img = None

            # Get all image candidates
            image_candidates = self.extract_images_from_html(html_content, url)

            if image_candidates:
                print(f"\nTrying {len(image_candidates)} image candidates...")
                for i, img_url in enumerate(image_candidates[:config.MAX_IMAGE_CANDIDATES], 1):
                    print(f"Attempt {i}/{min(config.MAX_IMAGE_CANDIDATES, len(image_candidates))}: {img_url[:80]}...")
                    background_img = self.download_image(img_url)
                    if background_img:
                        print(f"✓ Successfully downloaded image from candidate {i}")
                        break

            if not background_img:
                print("\nNo valid images found, using default background...")
                background_img = self.create_default_image()

            # Generate output filename
            if not output_filename:
                safe_title = re.sub(r'[^\w\s-]', '', article_data['title'])[:50]
                safe_title = re.sub(r'[-\s]+', '-', safe_title)
                output_filename = f"post_{safe_title}.png"

            output_path = os.path.join(config.OUTPUT_DIR, output_filename)

            # Create the design (using AI-extracted source name)
            self.create_post_design(
                background_img,
                article_data['title'],
                source_name,
                output_path,
                brand_text=brand_text,
                layout=layout
            )

            # Restore original config
            if show_source is not None:
                config.SHOW_SOURCE = original_show_source

            return output_path

        except Exception as e:
            # Restore original config even on error
            if show_source is not None:
                config.SHOW_SOURCE = original_show_source
            print(f"Error generating post: {e}")
            raise


def main():
    """Main function for CLI usage"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate social media posts from news articles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python headline_generator.py https://example.com/article
  python headline_generator.py https://example.com/article -o my_post.png
  python headline_generator.py https://example.com/article --brand "MyBrand"
  python headline_generator.py https://example.com/article --brand "My Brand" -o output.png
  python headline_generator.py https://example.com/article --hide-source
  python headline_generator.py https://example.com/article --style formal --hide-source
  python headline_generator.py https://example.com/article --layout layout2
  python headline_generator.py https://example.com/article --style clickbait --layout layout2
        """
    )

    parser.add_argument('url', help='Article URL to generate post from')
    parser.add_argument('-o', '--output', dest='output_filename',
                        help='Output filename (optional)')
    parser.add_argument('-b', '--brand', dest='brand_text',
                        help='Brand text to show in bottom left (optional)')
    parser.add_argument('-s', '--style', dest='style',
                        choices=['clickbait', 'formal', 'casual', 'question', 'storytelling'],
                        default='clickbait',
                        help='Headline style (default: clickbait)')
    parser.add_argument('-l', '--layout', dest='layout',
                        choices=['layout1', 'layout2'],
                        default='layout1',
                        help='Layout style: layout1 (white box) or layout2 (news update)')
    parser.add_argument('--hide-source', dest='hide_source',
                        action='store_true',
                        help='Hide source attribution (overrides config)')
    parser.add_argument('--show-source', dest='show_source',
                        action='store_true',
                        help='Show source attribution (overrides config)')

    args = parser.parse_args()

    # Determine show_source value
    show_source_override = None
    if args.hide_source:
        show_source_override = False
    elif args.show_source:
        show_source_override = True

    # Show configuration
    print(f"\nUsing style: {config.HEADLINE_STYLES[args.style]['name']}")
    print(f"Description: {config.HEADLINE_STYLES[args.style]['description']}")
    print(f"Layout: {config.AVAILABLE_LAYOUTS[args.layout]['name']}")
    if show_source_override is not None:
        print(f"Source attribution: {'ON' if show_source_override else 'OFF'}")
    print()

    generator = HeadlineGenerator()
    output_path = generator.generate_post(
        args.url,
        output_filename=args.output_filename,
        brand_text=args.brand_text,
        style=args.style,
        show_source=show_source_override,
        layout=args.layout
    )

    print(f"\n✓ Successfully generated post: {output_path}")


if __name__ == "__main__":
    main()
