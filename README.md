# Headline AI - News Post Generator

Generate beautiful social media posts from news articles automatically using AI.

## Features

- Fetch article content from any URL
- Extract title and main image using Gemini AI
- Create Instagram-style posts (1080x1350px)
- Automatic text wrapping and layout
- Source attribution
- Professional design with white text box overlay

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Add your Gemini API key to `.env`:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage

### Command Line

```bash
python headline_generator.py <article_url> [options]
```

**Options:**
- `-o, --output FILENAME` - Custom output filename
- `-b, --brand TEXT` - Brand text to show in bottom left corner
- `-h, --help` - Show help message

**Examples:**

```bash
# Basic usage
python headline_generator.py https://www.example.com/news/article

# With custom output filename
python headline_generator.py https://www.example.com/news/article -o my_post.png

# With custom branding
python headline_generator.py https://www.example.com/news/article --brand "FOLKATIVE"

# With both custom output and branding
python headline_generator.py https://www.example.com/news/article --brand "My Brand" -o output.png
```

### Python API

```python
from headline_generator import HeadlineGenerator

# Initialize generator
generator = HeadlineGenerator()

# Generate post (basic)
output_path = generator.generate_post(
    url="https://www.example.com/news/article"
)

# Generate post with custom filename
output_path = generator.generate_post(
    url="https://www.example.com/news/article",
    output_filename="my_post.png"
)

# Generate post with custom branding
output_path = generator.generate_post(
    url="https://www.example.com/news/article",
    brand_text="FOLKATIVE"
)

# Generate post with all options
output_path = generator.generate_post(
    url="https://www.example.com/news/article",
    output_filename="my_post.png",
    brand_text="My Brand"
)

print(f"Post created: {output_path}")
```

### Using Environment Variables

You can set a default brand text in your `.env` file:

```bash
GEMINI_API_KEY=your_api_key_here
BRAND_TEXT=FOLKATIVE
```

When `BRAND_TEXT` is set in `.env`, it will be used automatically unless overridden by the `--brand` parameter.

## How It Works

1. **Fetch Article**: Downloads HTML content from the provided URL
2. **AI Analysis**: Uses Gemini AI to:
   - Extract article title/headline
   - Find the main article image
   - Generate summary if needed
3. **Image Processing**: Downloads article image and resizes to 1080x1350
4. **Design Creation**:
   - Creates white overlay box for text
   - Adds wrapped headline text
   - Adds branding in bottom left (if specified)
   - Adds source attribution in bottom right
5. **Export**: Saves final design as PNG in `output/` folder

## Project Structure

```
headline-ai/
├── headline_generator.py  # Main script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your API keys (git-ignored)
├── .gitignore           # Git ignore rules
├── output/              # Generated posts
└── temp_images/         # Temporary image storage
```

## Configuration

### Design Customization

You can modify the following in `headline_generator.py`:

- **Image size**: Change `target_size = (1080, 1350)` in `create_post_design()`
- **Font sizes**: Modify `title_font` and `source_font` size parameters
- **Box styling**: Adjust `box_margin`, `box_padding`, colors, and radius
- **Branding**: Change "FOLKATIVE" text or remove it

### Gemini Model

The script uses `gemini-1.5-flash-latest`. You can change this in the `__init__` method:

```python
self.model = "gemini-1.5-flash-latest"  # or other Gemini models
```

## Requirements

- Python 3.7+
- Gemini API key
- Internet connection
- Fonts (uses DejaVu Sans by default, falls back to default if not available)

## Troubleshooting

### "GEMINI_API_KEY not found"
Make sure you've created a `.env` file and added your API key.

### Font errors
The script tries to use DejaVu Sans fonts. If not available, it falls back to default fonts. Install fonts:

```bash
# Ubuntu/Debian
sudo apt-get install fonts-dejavu

# macOS (usually pre-installed)
# Windows: Download DejaVu fonts manually
```

### Image download fails
Some websites block automated requests. The script will use a default background if image download fails.

## API Key

Get your Gemini API key from: https://ai.google.dev/

## License

MIT License

## Author

Created for Folkative Indonesia
