# Headline AI - Generator Post Berita Otomatis

Generate post social media yang menarik dari artikel berita secara otomatis menggunakan AI.

![Version](https://img.shields.io/badge/version-1.3.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## 📌 Fitur Utama

### 🤖 AI-Powered Generation
- **Gemini AI** untuk ekstraksi konten dan headline generation
- **AI Source Extraction** - Gemini otomatis identifikasi nama media (bukan domain mentah)
- **5 Style Headline** berbeda (Clickbait, Formal, Casual, Question, Storytelling)
- **2 Layout Design** (White Box Classic & News Update Modern)

### 🎨 Design & Layout
- **Layout 1: White Box (Classic)** - Clean dengan white overlay box
- **Layout 2: News Update (Modern)** - Badge + gradient overlay style
- **Ukuran Instagram Portrait** (1080x1350px) - langsung upload ready
- **Auto image extraction** dari artikel dengan multiple fallback
- **Text wrapping otomatis** untuk headline panjang

### ⚙️ Customization
- **Semua konfigurasi di config.py** - no hardcoded values!
- **Custom branding** support (optional)
- **Source attribution** yang bisa di-toggle on/off
- **Badge text customizable** untuk Layout 2
- **Warna dan spacing** semuanya adjustable

### 🌐 Dual Interface
- **Web UI (Recommended)** - Dark mode, responsive, real-time progress
- **CLI** - Untuk automation dan scripting
- **Python API** - Integrate ke aplikasi sendiri

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup API Key
```bash
# Buat file .env
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

**Dapatkan API Key gratis di:** https://ai.google.dev/

### 3. Run Web UI (Recommended)
```bash
python app.py
```

Buka browser: **http://localhost:5000**

### 4. Atau Gunakan CLI
```bash
python headline_generator.py https://www.kompas.com/artikel-example
```

---

## 🌐 Web Interface

### Screenshot & Features

**Web UI** menyediakan interface yang mudah dengan fitur lengkap:

✨ **Features:**
- Dark mode interface yang modern dan clean
- Responsive design (mobile & desktop friendly)
- Real-time progress tracking saat generate
- Gallery untuk melihat semua hasil
- Settings panel untuk edit konfigurasi
- Simple mode: Sekali input API key, langsung generate

### Cara Pakai Web UI

1. **Setup API Key** (pertama kali saja)
   - Klik tab "Settings"
   - Input Gemini API key
   - Klik "Save API Key"

2. **Generate Post**
   - Klik tab "Generate"
   - Paste URL artikel berita
   - Pilih **Headline Style**:
     - 🔥 Clickbait - Sensational & viral
     - 📰 Formal - Professional & factual
     - 💬 Casual - Friendly & conversational
     - ❓ Question - Engaging questions
     - 📖 Storytelling - Narrative & emotional
   - Pilih **Layout Style**:
     - 📄 White Box (Classic)
     - 🎨 News Update (Modern) - **NEW!**
   - (Optional) Tambah brand text
   - Klik "Generate Post"

3. **Lihat Hasil di Gallery**
   - Klik tab "Gallery"
   - Download atau delete hasil
   - Badge "NEW" untuk post < 24 jam

### Advanced Settings

Di tab **Settings**, kamu bisa customize:
- Image dimensions (Instagram Portrait/Square/Story, Twitter, dll)
- Font sizes dan typography
- Layout spacing (margin, padding, radius)
- AI temperature per style
- **System prompts untuk tiap headline style** (Advanced!)
- Source attribution settings
- Image extraction parameters

**Dokumentasi lengkap:** [WEB_UI_GUIDE.md](WEB_UI_GUIDE.md)

---

## 💻 Command Line Interface (CLI)

### Syntax Dasar
```bash
python headline_generator.py <url> [options]
```

### Options Lengkap
```
-o, --output FILENAME    Output filename custom
-b, --brand TEXT         Brand text untuk branding
-s, --style STYLE        Headline style (clickbait/formal/casual/question/storytelling)
-l, --layout LAYOUT      Layout style (layout1/layout2)
--hide-source            Hide source attribution
--show-source            Show source attribution
-h, --help              Show help message
```

### Contoh Penggunaan

#### Basic
```bash
# Generate dengan default settings (clickbait + layout1)
python headline_generator.py https://www.kompas.com/artikel

# Output akan di save ke: output/post_[title].png
```

#### Dengan Style
```bash
# Formal style untuk berita profesional
python headline_generator.py https://www.detik.com/artikel --style formal

# Casual style untuk konten santai
python headline_generator.py https://example.com/artikel -s casual

# Question style untuk engagement
python headline_generator.py https://example.com/artikel -s question
```

#### Dengan Layout
```bash
# Layout 2 (News Update - Modern)
python headline_generator.py https://www.kompas.com/artikel --layout layout2

# Kombinasi style + layout
python headline_generator.py https://www.cnnindonesia.com/artikel \
    --style clickbait \
    --layout layout2
```

#### Dengan Branding
```bash
# Tambah brand text
python headline_generator.py https://example.com/artikel --brand "MyBrand"

# Hide source attribution
python headline_generator.py https://example.com/artikel --hide-source

# Full combination
python headline_generator.py https://www.kompas.com/artikel \
    --style formal \
    --layout layout2 \
    --brand "MyMedia" \
    --show-source \
    -o hasil_berita.png
```

### Output
Hasil akan disimpan di folder `output/` dengan format:
```
output/post_[judul-artikel].png
```

---

## 🎨 Headline Styles - 5 Pilihan

Setiap style punya karakteristik dan AI prompt yang berbeda:

### 1️⃣ Clickbait (Temperature: 0.9)
**Tujuan:** Viral, sensational, curiosity-driven

**Contoh:**
- "Gak Nyangka! Ternyata Ini Alasan Kenapa..."
- "Viral! Kejadian Ini Bikin Netizen Heboh"
- "Berani Coba? Fakta Mengejutkan Tentang..."

**Best for:** Social media, viral content, entertainment

### 2️⃣ Formal (Temperature: 0.3)
**Tujuan:** Professional, journalistic, factual

**Contoh:**
- "Pemerintah Umumkan Kebijakan Baru Soal..."
- "Pakar: Ekonomi Indonesia Diprediksi..."
- "Studi Terbaru: Temuan Penelitian Menunjukkan..."

**Best for:** News portals, corporate, official announcements

### 3️⃣ Casual (Temperature: 0.7)
**Tujuan:** Friendly, conversational, approachable

**Contoh:**
- "Eh, Ternyata Fakta Menarik Ini Lho!"
- "Akhirnya! Event yang Ditunggu-tunggu"
- "Seru Nih: Topik yang Lagi Rame Dibahas"

**Best for:** Lifestyle blogs, community content, relatable stories

### 4️⃣ Question (Temperature: 0.8)
**Tujuan:** Engaging, curiosity-provoking

**Contoh:**
- "Kenapa Topik Ini Jadi Viral?"
- "Apa yang Terjadi Kalau Skenario Ini Terjadi?"
- "Siapa Sangka Subjek Ini Bisa Aksi Begitu?"

**Best for:** Educational content, discussion starters, engagement

### 5️⃣ Storytelling (Temperature: 0.8)
**Tujuan:** Narrative, emotional, humanistic

**Contoh:**
- "Kisah Inspiratif di Balik Kejadian Ini"
- "Dari Kondisi Sulit Hingga Sukses Gemilang"
- "Perjuangan Melawan Tantangan yang Luar Biasa"

**Best for:** Human interest stories, features, emotional content

**Guide lengkap:** [HEADLINE_STYLES.md](HEADLINE_STYLES.md)

---

## 📐 Layout Styles - 2 Pilihan

### Layout 1: White Box (Classic)

**Karakteristik:**
- White overlay box di tengah/bawah
- Text hitam di dalam box
- Source attribution di bottom right
- Brand text di bottom left (optional)
- Clean dan professional

**Visual:**
```
┌─────────────────────────────┐
│                             │
│   [Background Image]        │
│   (Slightly Darkened)       │
│                             │
│  ┌──────────────────────┐   │
│  │ Headline Text Here   │   │
│  │                      │   │
│  │ Brand     Sumber: XX │   │
│  └──────────────────────┘   │
└─────────────────────────────┘
```

**Best for:** Professional content, news articles, formal announcements

### Layout 2: News Update (Modern) - **NEW!**

**Karakteristik:**
- Badge "NEWS UPDATE" di top left (red background)
- Source logo di top right (AI-extracted)
- Full background image (no darkening)
- Gradient overlay di bottom
- Text putih di atas gradient
- Modern dan eye-catching

**Visual:**
```
┌─────────────────────────────┐
│ ┌───────────┐      Kompas   │
│ │NEWS UPDATE│               │
│ └───────────┘               │
│                             │
│   [Full Background Image]   │
│                             │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │
│ ▓ Headline Text Putih     ▓ │
│ ▓ Di Atas Gradient        ▓ │
└─────────────────────────────┘
```

**Best for:** Breaking news, viral content, social media stories

**Dokumentasi lengkap:** [LAYOUT2_DOCUMENTATION.md](LAYOUT2_DOCUMENTATION.md)

---

## 🤖 AI Source Extraction

Sistem sekarang menggunakan **Gemini AI** untuk mengidentifikasi nama media, bukan hanya parsing domain!

### Sebelumnya (Manual Domain Parsing)
```
URL: https://www.kompas.com/artikel
Output: Sumber: www.kompas.com  ← Domain mentah
```

### Sekarang (AI Extraction)
```
URL: https://www.kompas.com/artikel
Output: Sumber: Kompas  ← Nama media yang clean!
```

### Contoh Hasil

| URL | AI-Extracted Source |
|-----|---------------------|
| www.kompas.com | **Kompas** |
| news.detik.com | **Detik** |
| www.cnnindonesia.com | **CNN Indonesia** |
| katadata.co.id | **Katadata** |
| tirto.id | **Tirto** |

**Keuntungan:**
- ✅ Lebih user-friendly dan professional
- ✅ Konsisten untuk semua media
- ✅ AI bisa identify dari HTML metadata
- ✅ Fallback ke domain jika AI gagal
- ✅ No manual mapping needed!

**Dokumentasi:** [AI_SOURCE_EXTRACTION.md](AI_SOURCE_EXTRACTION.md)

---

## 🐍 Python API

Integrate ke aplikasi Python kamu sendiri:

```python
from headline_generator import HeadlineGenerator

# Initialize
generator = HeadlineGenerator()

# Basic - default settings
output_path = generator.generate_post(
    url="https://www.kompas.com/artikel"
)

# Dengan style
output_path = generator.generate_post(
    url="https://www.detik.com/artikel",
    style="formal"  # clickbait/formal/casual/question/storytelling
)

# Dengan layout
output_path = generator.generate_post(
    url="https://www.cnnindonesia.com/artikel",
    style="clickbait",
    layout="layout2"  # layout1 (default) or layout2
)

# Full options
output_path = generator.generate_post(
    url="https://example.com/artikel",
    output_filename="my_post.png",
    brand_text="MyBrand",
    style="storytelling",
    layout="layout2",
    show_source=True  # True/False/None (use config)
)

print(f"✓ Post created: {output_path}")
```

### Batch Processing
```python
urls = [
    "https://www.kompas.com/artikel1",
    "https://www.detik.com/artikel2",
    "https://www.cnnindonesia.com/artikel3"
]

generator = HeadlineGenerator()

for url in urls:
    try:
        output = generator.generate_post(
            url=url,
            style="clickbait",
            layout="layout2"
        )
        print(f"✓ Generated: {output}")
    except Exception as e:
        print(f"✗ Failed {url}: {e}")
```

---

## ⚙️ Configuration

### Lokasi Konfigurasi

**Semua settings ada di `config.py`** - JANGAN edit hardcoded values di script!

### Kategori Settings

#### 1. Image Settings
```python
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1350  # Instagram Portrait

# Preset lain:
# 1080 x 1080  - Instagram Square
# 1080 x 1920  - Instagram Story
# 1200 x 675   - Twitter
```

#### 2. Font Settings
```python
TITLE_FONT_SIZE = 48
SOURCE_FONT_SIZE = 24
TITLE_FONT_PATH = "/path/to/font.ttf"
```

#### 3. Colors (RGBA)
```python
WHITE_BOX_COLOR = (255, 255, 255, 240)  # White box
TEXT_COLOR = (0, 0, 0, 255)  # Black text
SOURCE_COLOR = (100, 100, 100, 255)  # Gray
BRAND_COLOR = (50, 50, 50, 255)  # Dark gray
```

#### 4. Layout Spacing
```python
BOX_MARGIN = 40    # Distance from edge
BOX_PADDING = 30   # Padding inside box
BOX_RADIUS = 20    # Corner radius
LINE_HEIGHT = 60   # Space between lines
```

#### 5. Branding & Source
```python
SHOW_SOURCE = True  # Toggle source attribution
SOURCE_TEXT = "Sumber"  # Label text
SHOW_BRAND = False
BRAND_TEXT = ""
```

#### 6. Layout 2 Settings
```python
LAYOUT2_BADGE_TEXT = "NEWS UPDATE"
LAYOUT2_BADGE_BG_COLOR = (220, 20, 60, 255)  # Red
LAYOUT2_GRADIENT_HEIGHT = 400
LAYOUT2_TEXT_COLOR = (255, 255, 255, 255)  # White
```

#### 7. AI Settings
```python
GEMINI_MODEL = "models/gemini-flash-latest"
GEMINI_TEMPERATURE = 0.9  # Per style bisa beda
```

#### 8. Headline Styles (Advanced)
```python
HEADLINE_STYLES = {
    "clickbait": {
        "name": "Clickbait",
        "temperature": 0.9,
        "prompt": """..."""  # Custom prompt
    },
    # ... 4 styles lainnya
}
```

**Guide lengkap:** [CONFIG_GUIDE.md](CONFIG_GUIDE.md)

---

## 📁 Project Structure

```
headline-ai/
├── headline_generator.py      # Core generator script
├── app.py                     # Flask web server
├── config.py                  # ⚙️ SEMUA KONFIGURASI DI SINI
├── requirements.txt           # Python dependencies
├── .env                       # API keys (git-ignored)
├── .env.example               # Template .env
│
├── templates/                 # Web UI templates
│   ├── base.html             # Base template (dark mode)
│   ├── index.html            # Generate page
│   ├── gallery.html          # Gallery page
│   └── settings.html         # Settings page
│
├── output/                    # 📁 Generated posts
├── web_settings.json         # Web UI settings cache
│
├── README.md                 # 📖 Dokumentasi utama (ini!)
├── CONFIG_GUIDE.md           # Guide konfigurasi
├── WEB_UI_GUIDE.md           # Guide Web UI
├── HEADLINE_STYLES.md        # Guide 5 headline styles
├── LAYOUT2_DOCUMENTATION.md  # Guide Layout 2
├── AI_SOURCE_EXTRACTION.md   # Guide AI source extraction
└── SOURCE_ATTRIBUTION_UPDATE.md  # Guide source customization
```

---

## 🔧 Troubleshooting

### API Key Error
```
Error: GEMINI_API_KEY not found
```
**Solution:**
```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```

### Font Error
```
Warning: Font not found, using default
```
**Solution:** Install DejaVu fonts
```bash
# Ubuntu/Debian
sudo apt-get install fonts-dejavu

# macOS - usually pre-installed
# Windows - download manually
```

### Image Download Gagal
```
Warning: No valid images found, using default background
```
**Penyebab:**
- Website blocking automated requests
- Image tidak ditemukan di HTML
- Image size terlalu kecil

**Solution:**
- Script akan auto fallback ke default background
- Atau adjust `MIN_IMAGE_WIDTH` dan `MIN_IMAGE_HEIGHT` di config.py

### Import Error
```
ModuleNotFoundError: No module named 'openai'
```
**Solution:**
```bash
pip install -r requirements.txt
```

### Port Already in Use (Web UI)
```
Error: Address already in use
```
**Solution:**
```bash
# Kill process di port 5000
lsof -ti:5000 | xargs kill -9

# Atau ganti port di app.py
app.run(port=5001)
```

---

## 📊 Requirements

- **Python 3.7+**
- **Gemini API Key** (gratis dari https://ai.google.dev/)
- **Internet connection**
- **Fonts**: DejaVu Sans (optional, fallback tersedia)

### Python Packages
```
openai
requests
beautifulsoup4
pillow
python-dotenv
flask
jinja2
```

Install semua:
```bash
pip install -r requirements.txt
```

---

## 🎯 Use Cases

### 1. News Portal / Media
- Generate post Instagram otomatis dari artikel
- Konsisten branding dengan custom badge
- Multiple styles untuk different sections

### 2. Content Creator / Influencer
- Repurpose artikel jadi IG post
- Clickbait style untuk viral content
- Question style untuk engagement

### 3. Social Media Manager
- Batch generate posts dari multiple URLs
- Gallery untuk manage semua hasil
- Quick customization via Web UI

### 4. Automation / Bot
- Integrate ke workflow otomatis
- Python API untuk scripting
- CLI untuk cron jobs

---

## 🚀 Roadmap

### ✅ Implemented
- [x] 5 Headline styles dengan custom prompts
- [x] 2 Layout designs (White Box + News Update)
- [x] AI source extraction (Gemini identifies media name)
- [x] Web UI dengan dark mode
- [x] Gallery dengan sorting & NEW badge
- [x] Customizable source attribution
- [x] CLI dengan full options
- [x] Python API

### 🔮 Future Ideas
- [ ] Layout 3: Minimalist style
- [ ] Video/GIF support untuk Instagram Story
- [ ] Multi-language headline generation
- [ ] Template system untuk custom layouts
- [ ] Integration dengan Instagram API (auto post)
- [ ] Bulk upload dari CSV
- [ ] A/B testing untuk headlines

---

## 📄 License

MIT License - bebas untuk digunakan, dimodifikasi, dan didistribusikan.

---

## 👨‍💻 Credits

**Developed by:** Claude (Anthropic AI)
**For:** Folkative Indonesia & Open Source Community

**Powered by:**
- Gemini AI (Google)
- Python
- Flask
- Tailwind CSS

---

## 📞 Support & Dokumentasi

### Dokumentasi Lengkap
- **[CONFIG_GUIDE.md](CONFIG_GUIDE.md)** - Panduan konfigurasi lengkap
- **[WEB_UI_GUIDE.md](WEB_UI_GUIDE.md)** - Guide Web Interface
- **[HEADLINE_STYLES.md](HEADLINE_STYLES.md)** - 5 Headline styles dengan contoh
- **[LAYOUT2_DOCUMENTATION.md](LAYOUT2_DOCUMENTATION.md)** - Layout 2 documentation
- **[AI_SOURCE_EXTRACTION.md](AI_SOURCE_EXTRACTION.md)** - AI source extraction guide
- **[SOURCE_ATTRIBUTION_UPDATE.md](SOURCE_ATTRIBUTION_UPDATE.md)** - Source customization

### Quick Links
- **Get API Key:** https://ai.google.dev/
- **Gemini Docs:** https://ai.google.dev/docs
- **Issue Tracker:** (Add your repo link here)

---

## 🌟 Getting Started Checklist

- [ ] Install Python 3.7+
- [ ] Clone/download project
- [ ] Run `pip install -r requirements.txt`
- [ ] Get Gemini API key dari https://ai.google.dev/
- [ ] Create `.env` file dengan API key
- [ ] Run `python app.py` untuk Web UI
- [ ] Atau `python headline_generator.py <url>` untuk CLI
- [ ] Explore settings di config.py
- [ ] Generate post pertama kamu!
- [ ] Baca dokumentasi untuk advanced features

---

**Happy Generating! 🎉**
