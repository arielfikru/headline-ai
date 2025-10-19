# Configuration Guide

## Overview

Semua konfigurasi untuk Headline AI Generator sekarang berada di `config.py`. File ini memungkinkan Anda untuk mengubah semua aspek dari generator tanpa perlu mengedit code utama.

## File Structure

```
headline-ai/
├── config.py              # ← SEMUA KONFIGURASI DI SINI
├── headline_generator.py  # Script utama (NO hardcoded values)
├── .env                   # API keys dan secrets
└── ...
```

## Configuration Sections

### 1. IMAGE SETTINGS

```python
IMAGE_WIDTH = 1080   # Lebar output image (px)
IMAGE_HEIGHT = 1350  # Tinggi output image (px)
```

**Contoh Custom:**
- Instagram Square: `1080 x 1080`
- Instagram Story: `1080 x 1920`
- Twitter: `1200 x 675`

---

### 2. FONT SETTINGS

```python
TITLE_FONT_SIZE = 48      # Ukuran font untuk headline
SOURCE_FONT_SIZE = 24     # Ukuran font untuk source
BRAND_FONT_SIZE = 24      # Ukuran font untuk branding

TITLE_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SOURCE_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
```

**Custom Fonts:**
- Set path ke font favorit Anda
- Atau set `None` untuk menggunakan default system font

---

### 3. COLOR SETTINGS

Semua warna dalam format RGBA: `(R, G, B, Alpha)`

```python
WHITE_BOX_COLOR = (255, 255, 255, 240)  # Kotak putih
TEXT_COLOR = (0, 0, 0, 255)             # Warna teks
SOURCE_COLOR = (100, 100, 100, 255)     # Warna source text
BRAND_COLOR = (50, 50, 50, 255)         # Warna branding
OVERLAY_COLOR = (0, 0, 0, 100)          # Overlay gelap di background
```

**Tips:**
- Alpha: 0 = transparan penuh, 255 = solid
- RGB: 0-255 untuk setiap channel

---

### 4. BOX STYLING

```python
BOX_MARGIN = 40   # Jarak kotak dari edge gambar
BOX_PADDING = 30  # Padding dalam kotak
BOX_RADIUS = 20   # Radius sudut kotak (rounded corners)
```

---

### 5. TEXT STYLING

```python
LINE_HEIGHT = 60           # Jarak antar baris teks
MAX_TITLE_LENGTH = 150     # Maksimal karakter untuk title
```

---

### 6. BRANDING

```python
BRAND_TEXT = ""         # Default brand text (bisa override via CLI)
SHOW_BRAND = False      # Show/hide branding
```

---

### 7. GEMINI AI SETTINGS

```python
GEMINI_MODEL = "models/gemini-flash-latest"
GEMINI_TEMPERATURE = 0.9  # 0.0 = conservative, 1.0 = creative
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
```

**Temperature Guide:**
- `0.0 - 0.3`: Formal, conservative
- `0.4 - 0.7`: Balanced
- `0.8 - 1.0`: Creative, clickbait-y

---

### 8. AI PROMPT TEMPLATE

Ini adalah template prompt yang dikirim ke Gemini AI:

```python
AI_PROMPT_TEMPLATE = """Analisis HTML berita berikut dan buat headline CLICKBAIT yang menarik:

URL: {url}

HTML:
{html_content}

Tugas kamu:
1. Baca dan pahami inti berita dari HTML
2. Buat headline CLICKBAIT yang menarik perhatian, seperti:
   - "Gak Nyangka! [fakta mengejutkan dari berita]"
   - "Ternyata Ini Alasan [topik berita]"
   ...
"""
```

**Customization:**
- Edit instruksi untuk mengubah style headline
- Tambahkan contoh-contoh baru
- Ubah bahasa atau tone

**Variables Available:**
- `{url}`: Article URL
- `{html_content}`: HTML content
- `{max_title_length}`: Maximum title length

---

### 9. IMAGE EXTRACTION SETTINGS

```python
MIN_IMAGE_WIDTH = 300          # Minimum lebar image yang valid
MIN_IMAGE_HEIGHT = 300         # Minimum tinggi image yang valid
MAX_IMAGE_CANDIDATES = 5       # Berapa banyak image dicoba download
MAX_ARTICLE_IMAGES = 5         # Max article images to extract
MAX_GENERAL_IMAGES = 10        # Max general images to check
```

---

### 10. OUTPUT SETTINGS

```python
OUTPUT_DIR = "output"        # Folder output
TEMP_DIR = "temp_images"     # Folder temporary
OUTPUT_FORMAT = "PNG"        # Format: PNG, JPEG, etc
OUTPUT_QUALITY = 95          # Quality: 1-100
```

---

### 11. REQUEST SETTINGS

```python
REQUEST_TIMEOUT = 30  # Timeout untuk HTTP requests (seconds)
USER_AGENT = 'Mozilla/5.0...'  # User agent string
```

---

## Quick Customization Examples

### Example 1: Ubah Style ke Minimalis

```python
# config.py
BOX_MARGIN = 60
BOX_PADDING = 40
OVERLAY_COLOR = (0, 0, 0, 150)  # Darker overlay
WHITE_BOX_COLOR = (255, 255, 255, 250)  # More solid white
```

### Example 2: Ubah Prompt ke Formal (Bukan Clickbait)

```python
# config.py
GEMINI_TEMPERATURE = 0.3  # Lower temperature

AI_PROMPT_TEMPLATE = """Analisis HTML berita berikut dan buat headline FORMAL:

URL: {url}
HTML: {html_content}

Tugas:
1. Buat headline FORMAL dan informatif
2. Maksimal {max_title_length} karakter
3. Fokus pada fakta, bukan sensasi

Response JSON:
{{
    "clickbait_title": "headline formal",
    "summary": "ringkasan"
}}
"""
```

### Example 3: Twitter Format (Horizontal)

```python
# config.py
IMAGE_WIDTH = 1200
IMAGE_HEIGHT = 675
TITLE_FONT_SIZE = 56
LINE_HEIGHT = 70
```

---

## Environment Variables (.env)

File `.env` untuk secrets:

```bash
GEMINI_API_KEY=your_api_key_here
BRAND_TEXT=FOLKATIVE  # Optional default branding
```

---

## Validation

Setelah mengubah config, test dengan:

```bash
# Check syntax
python3 -m py_compile config.py

# Test generation
python headline_generator.py https://example.com/article
```

---

## Best Practices

1. **Backup config.py** sebelum major changes
2. **Test perubahan** dengan 1 article dulu sebelum batch processing
3. **Document custom changes** dengan comments
4. **Version control**: Commit setiap perubahan konfigurasi

---

## Troubleshooting

**Q: Perubahan tidak apply?**
- Restart Python script (config di-load saat import)
- Pastikan tidak ada typo di variable name

**Q: Error setelah ubah prompt?**
- Pastikan `{url}`, `{html_content}`, `{max_title_length}` tetap ada
- JSON format dalam prompt harus valid

**Q: Font tidak load?**
- Check path font dengan `ls /path/to/font`
- Atau set `None` untuk fallback ke default

---

## Support

Untuk dokumentasi lengkap, lihat:
- [README.md](README.md) - Full documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
