# Headline Style Presets

Headline AI Generator hadir dengan **5 preset styles** yang bisa dipilih sesuai kebutuhan konten Anda.

## Available Styles

### 1. 🔥 **Clickbait** (Default)

**Best for:** Viral content, social media engagement, entertainment news

**Characteristics:**
- Sensational and curiosity-driven
- Creates "curiosity gap" yang membuat orang penasaran
- Menggunakan bahasa gaul dan menarik
- Temperature: 0.9 (very creative)

**Examples:**
```
❌ Original: "Harga Minyak Goreng Naik 20%"
✅ Clickbait: "Gak Nyangka! Harga Minyak Goreng Tembus Angka Ini"

❌ Original: "Indonesia Juara Badminton Dunia"
✅ Clickbait: "Viral! Atlet Indonesia Bikin Netizen Menangis Haru"
```

**When to use:**
- Social media posts
- Entertainment news
- Lifestyle content
- Viral stories

---

### 2. 📰 **Formal**

**Best for:** Professional media, news portals, corporate communications

**Characteristics:**
- Professional and journalistic
- Fokus pada fakta, bukan sensasi
- Objektif dan kredibel
- Bahasa Indonesia baku
- Temperature: 0.3 (conservative)

**Examples:**
```
❌ Clickbait: "Geger! Kebijakan Pemerintah Bikin Heboh"
✅ Formal: "Pemerintah Umumkan Kebijakan Baru Subsidi Energi"

❌ Clickbait: "Ternyata Ini Alasan Ekonomi Membaik!"
✅ Formal: "Studi Terbaru: Pertumbuhan Ekonomi Capai 5.2 Persen"
```

**When to use:**
- News portals
- Government announcements
- Corporate communications
- Academic content
- Press releases

---

### 3. 💬 **Casual**

**Best for:** Blogs, community content, friendly brands

**Characteristics:**
- Santai dan conversational
- Seperti ngobrol dengan teman
- Bersahabat dan approachable
- Tetap informatif
- Temperature: 0.7 (balanced)

**Examples:**
```
❌ Formal: "Pemerintah Luncurkan Aplikasi Pelayanan Publik"
✅ Casual: "Akhirnya! Ada Aplikasi Baru yang Bikin Urusan Surat-surat Jadi Gampang"

❌ Clickbait: "Viral! Kopi Ini Bikin Netizen Penasaran"
✅ Casual: "Seru Nih: Kopi Lokal yang Lagi Rame Dibahas"
```

**When to use:**
- Personal blogs
- Community pages
- Lifestyle brands
- Friendly B2C companies
- Food & beverage content

---

### 4. ❓ **Question**

**Best for:** Engagement-focused content, educational topics, discussion starters

**Characteristics:**
- Berbentuk pertanyaan (5W1H)
- Membuat pembaca penasaran ingin tahu jawabannya
- Natural dan engaging
- Temperature: 0.8 (creative)

**Examples:**
```
❌ Statement: "Harga Properti Terus Meningkat"
✅ Question: "Kenapa Harga Rumah Makin Mahal Padahal Gaji Segitu-gitu Aja?"

❌ Statement: "Indonesia Masuk 10 Besar Ekonomi Dunia"
✅ Question: "Apa yang Terjadi Kalau Indonesia Jadi Negara Terkaya di Asia?"
```

**When to use:**
- Educational content
- Discussion starters
- Engagement posts
- Quiz/poll content
- Thought-provoking topics

---

### 5. 📖 **Storytelling**

**Best for:** Human interest stories, feature articles, emotional content

**Characteristics:**
- Pendekatan naratif
- Ada arc emosional (perjalanan/transformasi)
- Humanis dan relatable
- Menggunakan bahasa yang mengalir seperti cerita
- Temperature: 0.8 (creative)

**Examples:**
```
❌ Formal: "Petani Berhasil Tingkatkan Hasil Panen"
✅ Storytelling: "Dari Gagal Panen Hingga Jadi Jutawan: Kisah Inspiratif Pak Tani"

❌ Clickbait: "Gak Nyangka! Anak SMA Ini Sukses Bisnis"
✅ Storytelling: "Perjuangan Anak SMA Mengubah Hobi Jadi Bisnis Ratusan Juta"
```

**When to use:**
- Human interest stories
- Success stories
- Feature articles
- Inspirational content
- Emotional narratives

---

## Usage

### CLI

```bash
# Default (Clickbait)
python headline_generator.py https://example.com/article

# Formal style
python headline_generator.py https://example.com/article --style formal

# Question style
python headline_generator.py https://example.com/article -s question

# All options
python headline_generator.py https://example.com/article \
    --style storytelling \
    --brand "MyBrand" \
    -o output.png
```

### Web UI

1. Buka `http://localhost:5000`
2. Pilih salah satu dari 5 style presets
3. Input URL artikel
4. Generate!

### Python API

```python
from headline_generator import HeadlineGenerator

generator = HeadlineGenerator()

# Default clickbait
generator.generate_post("https://example.com/article")

# Formal style
generator.generate_post(
    "https://example.com/article",
    style="formal"
)

# Question style with branding
generator.generate_post(
    "https://example.com/article",
    style="question",
    brand_text="MyBrand"
)
```

---

## Choosing the Right Style

| Content Type | Recommended Style |
|--------------|------------------|
| Entertainment News | Clickbait |
| Viral Stories | Clickbait |
| Corporate News | Formal |
| Government Announcements | Formal |
| Press Releases | Formal |
| Lifestyle Blog | Casual |
| Food & Beverage | Casual |
| Community Content | Casual |
| Educational Content | Question |
| Discussion Topics | Question |
| Feature Articles | Storytelling |
| Success Stories | Storytelling |
| Human Interest | Storytelling |

---

## Temperature Settings

Setiap style memiliki temperature yang optimal:

| Style | Temperature | Creativity Level |
|-------|------------|-----------------|
| Clickbait | 0.9 | Very High |
| Formal | 0.3 | Low (Factual) |
| Casual | 0.7 | Medium-High |
| Question | 0.8 | High |
| Storytelling | 0.8 | High |

**Note:** Temperature bisa di-override di `config.py` atau via advanced settings di Web UI.

---

## Customization

### Edit Prompts

Semua prompt templates ada di `config.py`:

```python
HEADLINE_STYLES = {
    "clickbait": {
        "name": "Clickbait",
        "description": "Sensational, curiosity-driven headlines",
        "temperature": 0.9,
        "prompt": """Your custom prompt here..."""
    },
    # ... other styles
}
```

### Add New Style

```python
# config.py

HEADLINE_STYLES["mynewstyle"] = {
    "name": "My Custom Style",
    "description": "Description here",
    "temperature": 0.7,
    "prompt": """
    Your custom prompt template...
    Use {url}, {html_content}, {max_title_length}
    """
}
```

---

## Examples by Industry

### E-Commerce
- **Product Launch:** Clickbait or Question
- **Sale Announcement:** Casual
- **Brand Story:** Storytelling

### News Media
- **Breaking News:** Formal
- **Feature Articles:** Storytelling
- **Opinion Pieces:** Question

### Education
- **Course Announcements:** Formal
- **Study Tips:** Casual or Question
- **Student Success:** Storytelling

### Technology
- **Product Reviews:** Casual
- **Tech News:** Formal or Clickbait
- **Tutorials:** Question

---

## Tips

1. **Know Your Audience**
   - B2B → Formal
   - B2C → Casual/Clickbait
   - Mixed → Question

2. **Platform Matters**
   - LinkedIn → Formal
   - Instagram → Clickbait/Casual
   - Twitter → Question/Casual
   - Corporate Site → Formal

3. **Content Type**
   - Hard News → Formal
   - Soft News → Casual/Storytelling
   - Viral Content → Clickbait

4. **Test Different Styles**
   - Generate dengan beberapa style
   - A/B test performance
   - Lihat mana yang paling engage

---

## See Also

- [CONFIG_GUIDE.md](CONFIG_GUIDE.md) - Customize prompts
- [README.md](README.md) - General documentation
- [WEB_UI_GUIDE.md](WEB_UI_GUIDE.md) - Web interface guide
