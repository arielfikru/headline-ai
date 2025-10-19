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

### 🌐 Web Interface (Recommended)

**NEW!** Gunakan Web UI untuk experience yang lebih mudah:

```bash
# Quick start
./run_web.sh

# Or manually
python app.py
```

Buka browser di `http://localhost:5000`

**Features:**
- ✨ Dark mode interface yang clean
- 📱 Responsive design (mobile & desktop)
- ⚡ Simple mode: Input API key sekali, langsung generate
- ⚙️ Advanced mode: Edit semua config dari browser
- 🖼️ Gallery untuk lihat semua hasil
- 📊 Real-time progress tracking

**Lihat [WEB_UI_GUIDE.md](WEB_UI_GUIDE.md) untuk dokumentasi lengkap!**

---

### Command Line

```bash
python headline_generator.py <article_url> [options]
```

**Options:**
- `-o, --output FILENAME` - Custom output filename
- `-b, --brand TEXT` - Brand text to show in bottom left corner
- `-s, --style STYLE` - Headline style: `clickbait`, `formal`, `casual`, `question`, `storytelling`
- `-h, --help` - Show help message

**Examples:**

```bash
# Basic usage (default: clickbait)
python headline_generator.py https://www.example.com/news/article

# With formal style
python headline_generator.py https://www.example.com/news/article --style formal

# With question style
python headline_generator.py https://www.example.com/news/article -s question

# All options combined
python headline_generator.py https://www.example.com/news/article \
    --style storytelling \
    --brand "MyBrand" \
    -o output.png
```

### 🎨 **5 Headline Styles Available:**

| Style | Description | Best For |
|-------|-------------|----------|
| 🔥 **Clickbait** | Sensational, curiosity-driven | Viral content, social media |
| 📰 **Formal** | Professional, journalistic | News portals, corporate |
| 💬 **Casual** | Friendly, conversational | Blogs, lifestyle |
| ❓ **Question** | Engaging questions | Educational, discussion |
| 📖 **Storytelling** | Narrative, emotional | Human interest, features |

**Lihat [HEADLINE_STYLES.md](HEADLINE_STYLES.md) untuk guide lengkap dengan examples!**

---

### Python API

```python
from headline_generator import HeadlineGenerator

# Initialize generator
generator = HeadlineGenerator()

# Generate post (basic - default clickbait)
output_path = generator.generate_post(
    url="https://www.example.com/news/article"
)

# Generate with formal style
output_path = generator.generate_post(
    url="https://www.example.com/news/article",
    style="formal"
)

# Generate with question style and branding
output_path = generator.generate_post(
    url="https://www.example.com/news/article",
    style="question",
    brand_text="MyBrand"
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
BRAND_TEXT=MyBrand
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

### All Settings in config.py

**IMPORTANT:** Semua konfigurasi sekarang ada di `config.py`. JANGAN edit hardcoded values di `headline_generator.py`.

Edit `config.py` untuk mengubah:

- **Image dimensions**: `IMAGE_WIDTH`, `IMAGE_HEIGHT`
- **Font settings**: `TITLE_FONT_SIZE`, font paths, etc
- **Colors**: `WHITE_BOX_COLOR`, `TEXT_COLOR`, `BRAND_COLOR`, etc
- **Box styling**: `BOX_MARGIN`, `BOX_PADDING`, `BOX_RADIUS`
- **AI settings**: `GEMINI_MODEL`, `GEMINI_TEMPERATURE`
- **AI Prompt**: `AI_PROMPT_TEMPLATE` - customize clickbait style
- **Image extraction**: `MIN_IMAGE_WIDTH`, `MAX_IMAGE_CANDIDATES`
- **Output**: Format, quality, directories

**Lihat [CONFIG_GUIDE.md](CONFIG_GUIDE.md) untuk panduan lengkap!**

### Quick Examples

```python
# config.py

# Ubah ukuran ke Instagram Square
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1080

# Ubah style prompt jadi lebih formal
GEMINI_TEMPERATURE = 0.3
AI_PROMPT_TEMPLATE = """Buat headline FORMAL..."""

# Ubah warna
WHITE_BOX_COLOR = (240, 240, 240, 250)
BRAND_COLOR = (255, 0, 0, 255)  # Red branding
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
