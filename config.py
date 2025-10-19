"""
Configuration file for Headline Generator
Modify these values to customize the design
"""

# ============================================================================
# IMAGE SETTINGS
# ============================================================================

# Image dimensions
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1350

# ============================================================================
# FONT SETTINGS
# ============================================================================

# Font sizes
TITLE_FONT_SIZE = 48
SOURCE_FONT_SIZE = 24
BRAND_FONT_SIZE = 24

# Font paths (set to None to use default fonts)
TITLE_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SOURCE_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# ============================================================================
# COLOR SETTINGS (RGBA format)
# ============================================================================

WHITE_BOX_COLOR = (255, 255, 255, 240)  # White with slight transparency
TEXT_COLOR = (0, 0, 0, 255)  # Black
SOURCE_COLOR = (100, 100, 100, 255)  # Gray
BRAND_COLOR = (50, 50, 50, 255)  # Dark gray
OVERLAY_COLOR = (0, 0, 0, 100)  # Semi-transparent black overlay on background

# ============================================================================
# BOX STYLING
# ============================================================================

BOX_MARGIN = 40  # Distance from edge
BOX_PADDING = 30  # Padding inside the box
BOX_RADIUS = 20  # Corner radius

# ============================================================================
# TEXT STYLING
# ============================================================================

LINE_HEIGHT = 60  # Space between lines
MAX_TITLE_LENGTH = 150  # Maximum characters for title

# ============================================================================
# BRANDING
# ============================================================================

BRAND_TEXT = ""
SHOW_BRAND = False  # Set to False to hide branding

# ============================================================================
# GEMINI AI SETTINGS
# ============================================================================

GEMINI_MODEL = "models/gemini-flash-latest"
GEMINI_TEMPERATURE = 0.9  # Higher for more creative clickbait
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# ============================================================================
# AI PROMPT TEMPLATE
# ============================================================================

AI_PROMPT_TEMPLATE = """Analisis HTML berita berikut dan buat headline CLICKBAIT yang menarik:

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
   - Maksimal {max_title_length} karakter
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

# Maximum HTML content length to send to AI (characters)
MAX_HTML_LENGTH = 30000

# ============================================================================
# IMAGE EXTRACTION SETTINGS
# ============================================================================

# Minimum image dimensions to consider (pixels)
MIN_IMAGE_WIDTH = 300
MIN_IMAGE_HEIGHT = 300

# Maximum number of image candidates to try downloading
MAX_IMAGE_CANDIDATES = 5

# Number of article images to extract
MAX_ARTICLE_IMAGES = 5

# Number of general images to check
MAX_GENERAL_IMAGES = 10

# ============================================================================
# OUTPUT SETTINGS
# ============================================================================

OUTPUT_DIR = "output"
TEMP_DIR = "temp_images"
OUTPUT_FORMAT = "PNG"
OUTPUT_QUALITY = 95

# ============================================================================
# REQUEST SETTINGS
# ============================================================================

REQUEST_TIMEOUT = 30  # seconds
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
