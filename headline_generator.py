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
from urllib.parse import urlparse
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


class HeadlineGenerator:
    def __init__(self):
        """Initialize the Headline Generator with Gemini API"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")

        # Initialize OpenAI client for Gemini
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        self.model = "models/gemini-flash-latest"

        # Create output directory
        os.makedirs("output", exist_ok=True)
        os.makedirs("temp_images", exist_ok=True)

    def fetch_article_content(self, url):
        """Fetch HTML content from URL"""
        print(f"Fetching article from: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
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
        for img in article_imgs[:5]:  # Get first 5 article images
            if img.get('src'):
                image_urls.append(img['src'])
            elif img.get('data-src'):  # Lazy loaded images
                image_urls.append(img['data-src'])

        # Priority 4: All images with reasonable size attributes
        all_imgs = soup.find_all('img')
        for img in all_imgs[:10]:
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
        from urllib.parse import urljoin
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

    def extract_content_with_gemini(self, html_content, url):
        """Use Gemini to extract article content, title, and image URL"""
        print("Analyzing article content with Gemini...")

        # First extract images using BeautifulSoup
        image_candidates = self.extract_images_from_html(html_content, url)
        print(f"Found {len(image_candidates)} image candidates")

        # Truncate HTML if too long (keep first 30000 chars)
        if len(html_content) > 30000:
            html_content = html_content[:30000] + "..."

        prompt = f"""Analisis HTML berita berikut dan buat headline CLICKBAIT yang menarik:

URL: {url}

HTML:
{html_content}

Tugas kamu:
1. Baca dan pahami inti berita dari HTML
2. Buat headline CLICKBAIT yang menarik perhatian, seperti:
   - "Gak Nyangka! [fakta mengejutkan dari berita]"
   - "Ternyata Ini Alasan [topik berita]"
   - "Viral! [topik berita] Bikin Netizen [reaksi]"
   - "[Angka/Fakta] yang Bikin [reaksi emosional]"
   - "Berani Coba? [Topik berita]"

3. Headline harus:
   - Maksimal 150 karakter
   - Bahasa Indonesia yang gaul dan menarik
   - Mengandung unsur penasaran (curiosity gap)
   - TIDAK boleh hanya copy judul asli
   - Harus membuat orang ingin tahu lebih lanjut

4. Buat juga summary singkat 1 kalimat untuk context

Response dalam format JSON:
{{
    "clickbait_title": "headline clickbait yang menarik",
    "summary": "ringkasan 1 kalimat"
}}

PENTING: Response HARUS valid JSON tanpa markdown atau text lain!"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,  # Higher temperature for more creative clickbait
        )

        result_text = response.choices[0].message.content

        # Extract JSON from response
        import json
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(result_text)

            # Use clickbait_title as the main title
            result['title'] = result.get('clickbait_title', result.get('title', 'Berita Terkini'))
            result['image_url'] = image_candidates[0] if image_candidates else None

        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            print(f"Response was: {result_text}")
            result = {
                "title": "Berita Terkini yang Mengejutkan!",
                "summary": "Baca berita selengkapnya",
                "image_url": image_candidates[0] if image_candidates else None,
            }

        return result

    def download_image(self, image_url):
        """Download image from URL with validation"""
        print(f"Downloading image from: {image_url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': image_url
        }

        try:
            response = requests.get(image_url, headers=headers, timeout=30, allow_redirects=True)
            response.raise_for_status()

            # Validate it's actually an image
            content_type = response.headers.get('content-type', '')
            if 'image' not in content_type.lower():
                print(f"Warning: URL doesn't appear to be an image (content-type: {content_type})")

            img = Image.open(BytesIO(response.content))

            # Validate image size
            if img.width < 300 or img.height < 300:
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
        img = Image.new('RGB', (1080, 1350), color='#1a1a1a')
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

    def create_post_design(self, background_img, title, source_domain, output_path):
        """Create the final post design"""
        print("Creating post design...")

        # Resize and crop background image to 1080x1350
        target_size = (1080, 1350)

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
        overlay = Image.new('RGBA', target_size, (0, 0, 0, 100))
        background_img = background_img.convert('RGBA')
        background_img = Image.alpha_composite(background_img, overlay)

        # Create white box for text
        draw = ImageDraw.Draw(background_img)

        # Box dimensions
        box_margin = 40
        box_padding = 30
        box_left = box_margin
        box_right = target_size[0] - box_margin
        box_width = box_right - box_left

        # Try to load fonts, fallback to default if not available
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            source_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except:
            print("Custom fonts not found, using default...")
            title_font = ImageFont.load_default()
            source_font = ImageFont.load_default()

        # Wrap title text
        text_max_width = box_width - (box_padding * 2)
        wrapped_lines = self.wrap_text(title, title_font, text_max_width)

        # Calculate text height
        temp_img = Image.new('RGB', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        line_height = 60
        total_text_height = len(wrapped_lines) * line_height

        # Position white box in lower third
        box_height = total_text_height + (box_padding * 2) + 80  # Extra space for source
        box_top = target_size[1] - box_height - box_margin - 60
        box_bottom = box_top + box_height

        # Draw white box with rounded corners
        draw.rounded_rectangle(
            [box_left, box_top, box_right, box_bottom],
            radius=20,
            fill=(255, 255, 255, 240)
        )

        # Draw text
        y_position = box_top + box_padding
        for line in wrapped_lines:
            draw.text(
                (box_left + box_padding, y_position),
                line,
                fill=(0, 0, 0, 255),
                font=title_font
            )
            y_position += line_height

        # Draw source at bottom right
        source_text = f"Source: {source_domain}"
        source_bbox = draw.textbbox((0, 0), source_text, font=source_font)
        source_width = source_bbox[2] - source_bbox[0]
        source_x = box_right - box_padding - source_width
        source_y = box_bottom - box_padding - 30

        draw.text(
            (source_x, source_y),
            source_text,
            fill=(100, 100, 100, 255),
            font=source_font
        )

        # Convert back to RGB and save
        background_img = background_img.convert('RGB')
        background_img.save(output_path, 'PNG', quality=95)
        print(f"Post saved to: {output_path}")

    def generate_post(self, url, output_filename=None):
        """Main method to generate post from URL"""
        try:
            # Extract domain for source
            parsed_url = urlparse(url)
            source_domain = parsed_url.netloc

            # Fetch article
            html_content = self.fetch_article_content(url)

            # Extract content with Gemini
            article_data = self.extract_content_with_gemini(html_content, url)

            print(f"\nExtracted data:")
            print(f"Title: {article_data['title']}")
            print(f"Summary: {article_data.get('summary', 'N/A')}")

            # Try to download image from candidates
            background_img = None

            # Get all image candidates
            image_candidates = self.extract_images_from_html(html_content, url)

            if image_candidates:
                print(f"\nTrying {len(image_candidates)} image candidates...")
                for i, img_url in enumerate(image_candidates[:5], 1):  # Try first 5
                    print(f"Attempt {i}/{min(5, len(image_candidates))}: {img_url[:80]}...")
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

            output_path = os.path.join("output", output_filename)

            # Create the design
            self.create_post_design(
                background_img,
                article_data['title'],
                source_domain,
                output_path
            )

            return output_path

        except Exception as e:
            print(f"Error generating post: {e}")
            raise


def main():
    """Main function for CLI usage"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python headline_generator.py <article_url> [output_filename]")
        print("\nExample:")
        print("  python headline_generator.py https://example.com/article")
        print("  python headline_generator.py https://example.com/article my_post.png")
        sys.exit(1)

    url = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) > 2 else None

    generator = HeadlineGenerator()
    output_path = generator.generate_post(url, output_filename)

    print(f"\n✓ Successfully generated post: {output_path}")


if __name__ == "__main__":
    main()
