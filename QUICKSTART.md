# Quick Start Guide

## Setup (5 menit)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup API Key
Edit file `.env` dan masukkan API key Gemini:
```bash
nano .env
```

Isi dengan:
```
GEMINI_API_KEY=AIza...your_key_here
```

## Cara Pakai

### Opsi 1: Command Line (Paling Mudah)

```bash
python headline_generator.py https://www.detik.com/news/berita/d-12345/artikel-berita
```

Output: File PNG di folder `output/`

### Opsi 2: Interactive Mode

```bash
python example.py
```

Masukkan URL ketika diminta.

### Opsi 3: Python Script

Buat file `my_script.py`:

```python
from headline_generator import HeadlineGenerator

generator = HeadlineGenerator()

# Single post
generator.generate_post("https://www.kompas.com/article")

# Multiple posts
urls = [
    "https://www.detik.com/article1",
    "https://www.kompas.com/article2",
]

for i, url in enumerate(urls):
    generator.generate_post(url, f"post_{i}.png")
```

Run:
```bash
python my_script.py
```

## Contoh Output

Post yang dihasilkan akan:
- Ukuran: 1080x1350 px (Instagram portrait)
- Background: Gambar dari artikel
- Teks: Judul/ringkasan di kotak putih
- Source: Domain artikel di pojok kanan bawah
- Branding: "FOLKATIVE" di pojok kanan atas

## Troubleshooting

**Error: GEMINI_API_KEY not found**
→ Pastikan file `.env` sudah dibuat dan berisi API key

**Error: No module named 'xxx'**
→ Run: `pip install -r requirements.txt`

**Image download gagal**
→ Script akan otomatis pakai background default

## Mendapatkan Gemini API Key

1. Buka: https://ai.google.dev/
2. Login dengan Google Account
3. Klik "Get API Key"
4. Copy API key
5. Paste ke file `.env`

## Tips

- Gunakan URL artikel yang lengkap (bukan homepage)
- Artikel dengan gambar akan menghasilkan post lebih menarik
- Cek folder `output/` untuk hasil
- Customize design di `headline_generator.py` baris 200-300

## Support

Lihat [README.md](README.md) untuk dokumentasi lengkap.
