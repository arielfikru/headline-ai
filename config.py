"""
Configuration file for Headline Generator
Modify these values to customize the design
"""

# ============================================================================
# IMAGE SETTINGS
# ============================================================================

# Image dimensions
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1080

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
# BRANDING & SOURCE
# ============================================================================

BRAND_TEXT = ""
SHOW_BRAND = False  # Set to False to hide branding
SHOW_SOURCE = True  # Set to False to hide source attribution
SOURCE_TEXT = "Sumber"  # Text for source label (default: "Sumber")

# ============================================================================
# LAYOUT SETTINGS
# ============================================================================

# Available layouts
AVAILABLE_LAYOUTS = {
    "layout1": {
        "name": "White Box (Classic)",
        "description": "White box overlay dengan title dan source di bawah",
        "type": "white_box"
    },
    "layout2": {
        "name": "Modern Gradient",
        "description": "Gradient overlay di bawah, source logo di atas, text over image",
        "type": "modern_gradient"
    }
}

DEFAULT_LAYOUT = "layout1"

# Layout 2 (Modern Gradient) specific settings
LAYOUT2_BADGE_TEXT = "NEWS UPDATE"  # Not used anymore (badge removed)
LAYOUT2_BADGE_BG_COLOR = (220, 20, 60, 255)  # Not used anymore
LAYOUT2_BADGE_TEXT_COLOR = (255, 255, 255, 255)  # Not used anymore
LAYOUT2_BADGE_PADDING = 20  # Not used anymore
LAYOUT2_BADGE_MARGIN = 30  # Used for source logo margin
LAYOUT2_GRADIENT_HEIGHT = 550  # Height of bottom gradient overlay (increased for thicker gradient)
LAYOUT2_GRADIENT_COLOR = (0, 0, 0, 220)  # Dark with stronger transparency
LAYOUT2_TEXT_COLOR = (255, 255, 255, 255)  # White text for overlay

# ============================================================================
# GEMINI AI SETTINGS
# ============================================================================

GEMINI_MODEL = "models/gemini-flash-latest"
GEMINI_TEMPERATURE = 0.9  # Higher for more creative clickbait
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# ============================================================================
# AI PROMPT TEMPLATES - 5 PRESET STYLES
# ============================================================================

# Default style to use
DEFAULT_HEADLINE_STYLE = "clickbait"

# Available headline styles
HEADLINE_STYLES = {
    "clickbait": {
        "name": "Clickbait",
        "description": "Sensational, curiosity-driven headlines",
        "temperature": 0.9,
        "prompt": """Analisis HTML berita berikut dan buat headline CLICKBAIT yang menarik:

URL: {url}
HTML: {html_content}

Tugas kamu:
1. Baca dan pahami inti berita dari HTML
2. Identifikasi SUMBER berita (nama media/publisher, seperti "Kompas", "Detik", "CNN Indonesia", dll)
3. Buat headline CLICKBAIT yang menarik perhatian, seperti:
   - "Gak Nyangka! [fakta mengejutkan dari berita]"
   - "Ternyata Ini Alasan [topik berita]"
   - "Viral! [topik berita] Bikin Netizen [reaksi]"
   - "[Angka/Fakta] yang Bikin [reaksi emosional]"
   - "Berani Coba? [Topik berita]"

4. Headline harus:
   - Maksimal {max_title_length} karakter
   - Bahasa Indonesia yang gaul dan menarik
   - Mengandung unsur penasaran (curiosity gap)
   - TIDAK boleh hanya copy judul asli
   - Harus membuat orang ingin tahu lebih lanjut

Response JSON: {{"title": "headline clickbait", "summary": "ringkasan", "source": "nama media"}}
PENTING: Response HARUS valid JSON tanpa markdown!"""
    },

    "formal": {
        "name": "Formal",
        "description": "Professional, journalistic style",
        "temperature": 0.3,
        "prompt": """Analisis HTML berita berikut dan buat headline FORMAL yang profesional:

URL: {url}
HTML: {html_content}

Tugas kamu:
1. Baca dan pahami inti berita dari HTML
2. Identifikasi SUMBER berita (nama media/publisher, seperti "Kompas", "Detik", "CNN Indonesia", dll)
3. Buat headline FORMAL dan informatif seperti media mainstream:
   - "[Subjek] [Predikat] [Objek/Keterangan]"
   - "Pemerintah Umumkan [Kebijakan Baru]"
   - "Pakar: [Statement atau Prediksi]"
   - "[Institusi] Luncurkan [Program/Produk]"
   - "Studi Terbaru: [Temuan Penelitian]"

4. Headline harus:
   - Maksimal {max_title_length} karakter
   - Bahasa Indonesia baku dan formal
   - Fokus pada fakta, bukan sensasi
   - Objektif dan informatif
   - Kredibel seperti headline Kompas/Tempo

Response JSON: {{"title": "headline formal", "summary": "ringkasan", "source": "nama media"}}
PENTING: Response HARUS valid JSON tanpa markdown!"""
    },

    "casual": {
        "name": "Casual",
        "description": "Friendly, conversational tone",
        "temperature": 0.7,
        "prompt": """Analisis HTML berita berikut dan buat headline CASUAL yang santai:

URL: {url}
HTML: {html_content}

Tugas kamu:
1. Baca dan pahami inti berita dari HTML
2. Identifikasi SUMBER berita (nama media/publisher, seperti "Kompas", "Detik", "CNN Indonesia", dll)
3. Buat headline CASUAL dengan gaya ngobrol santai:
   - "[Topik] yang Lagi Rame Dibahas"
   - "Eh, Ternyata [Fakta Menarik] Lho!"
   - "Akhirnya! [Event/Kejadian]"
   - "Seru Nih: [Topik Menarik]"
   - "[Subjek] Bikin [Reaksi Positif]"

4. Headline harus:
   - Maksimal {max_title_length} karakter
   - Bahasa Indonesia casual, seperti ngobrol sama teman
   - Bersahabat dan approachable
   - Tetap informatif tapi tidak kaku
   - Hindari clickbait berlebihan

Response JSON: {{"title": "headline casual", "summary": "ringkasan", "source": "nama media"}}
PENTING: Response HARUS valid JSON tanpa markdown!"""
    },

    "question": {
        "name": "Question",
        "description": "Engaging question-based headlines",
        "temperature": 0.8,
        "prompt": """Analisis HTML berita berikut dan buat headline berbentuk PERTANYAAN yang engaging:

URL: {url}
HTML: {html_content}

Tugas kamu:
1. Baca dan pahami inti berita dari HTML
2. Identifikasi SUMBER berita (nama media/publisher, seperti "Kompas", "Detik", "CNN Indonesia", dll)
3. Buat headline berbentuk PERTANYAAN yang membuat penasaran:
   - "Kenapa [Topik] Jadi [Kondisi]?"
   - "Apa yang Terjadi Kalau [Skenario]?"
   - "Siapa Sangka [Subjek] Bisa [Aksi]?"
   - "Kapan [Event] Akan [Terjadi]?"
   - "Bagaimana [Proses] Bisa [Hasil]?"

4. Headline harus:
   - Maksimal {max_title_length} karakter
   - Berbentuk pertanyaan (5W1H: Apa, Siapa, Kenapa, Kapan, Dimana, Bagaimana)
   - Membuat pembaca penasaran ingin tahu jawabannya
   - Natural dan tidak dipaksakan
   - Bahasa Indonesia yang jelas

Response JSON: {{"title": "headline pertanyaan", "summary": "ringkasan", "source": "nama media"}}
PENTING: Response HARUS valid JSON tanpa markdown!"""
    },

    "storytelling": {
        "name": "Storytelling",
        "description": "Narrative-driven, emotional headlines",
        "temperature": 0.8,
        "prompt": """Analisis HTML berita berikut dan buat headline STORYTELLING yang naratif:

URL: {url}
HTML: {html_content}

Tugas kamu:
1. Baca dan pahami inti berita dari HTML
2. Identifikasi SUMBER berita (nama media/publisher, seperti "Kompas", "Detik", "CNN Indonesia", dll)
3. Buat headline STORYTELLING dengan pendekatan cerita:
   - "Kisah [Subjek] yang [Perjalanan Emosional]"
   - "Dari [Kondisi Awal] Hingga [Kondisi Akhir]"
   - "Perjuangan [Subjek] Melawan [Tantangan]"
   - "Di Balik [Kejadian], Ada [Cerita Tersembunyi]"
   - "[Subjek] Mengubah [Kondisi] Menjadi [Hasil]"

4. Headline harus:
   - Maksimal {max_title_length} karakter
   - Menggunakan pendekatan naratif/bercerita
   - Memiliki arc emosional (perjalanan/transformasi)
   - Humanis dan relatable
   - Bahasa Indonesia yang mengalir seperti cerita

Response JSON: {{"title": "headline storytelling", "summary": "ringkasan", "source": "nama media"}}
PENTING: Response HARUS valid JSON tanpa markdown!"""
    }
}

# Backward compatibility: Keep AI_PROMPT_TEMPLATE as default clickbait style
AI_PROMPT_TEMPLATE = HEADLINE_STYLES["clickbait"]["prompt"]

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
