"""
Configuration file for Headline Generator
Modify these values to customize the design
"""

# Image dimensions
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1350

# Font sizes
TITLE_FONT_SIZE = 48
SOURCE_FONT_SIZE = 24
BRAND_FONT_SIZE = 24

# Font paths (set to None to use default fonts)
TITLE_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SOURCE_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Colors (RGBA format)
WHITE_BOX_COLOR = (255, 255, 255, 240)  # White with slight transparency
TEXT_COLOR = (0, 0, 0, 255)  # Black
SOURCE_COLOR = (100, 100, 100, 255)  # Gray
BRAND_COLOR = (50, 50, 50, 255)  # Dark gray
OVERLAY_COLOR = (0, 0, 0, 100)  # Semi-transparent black overlay on background

# Box styling
BOX_MARGIN = 40  # Distance from edge
BOX_PADDING = 30  # Padding inside the box
BOX_RADIUS = 20  # Corner radius

# Text styling
LINE_HEIGHT = 60  # Space between lines
MAX_TITLE_LENGTH = 150  # Maximum characters for title

# Branding
BRAND_TEXT = ""
SHOW_BRAND = False  # Set to False to hide branding

# Gemini settings
GEMINI_MODEL = "gemini-1.5-flash-latest"
GEMINI_TEMPERATURE = 0.7

# Output settings
OUTPUT_DIR = "output"
TEMP_DIR = "temp_images"
OUTPUT_FORMAT = "PNG"
OUTPUT_QUALITY = 95

# Request settings
REQUEST_TIMEOUT = 30  # seconds
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
