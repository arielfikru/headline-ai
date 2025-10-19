# Web UI Guide - Headline AI

## Overview

Headline AI sekarang hadir dengan **Web Interface** yang user-friendly! Tidak perlu lagi menggunakan command line - cukup buka browser dan generate posts dengan mudah.

## Features

### 🎨 **Dark Mode UI**
- Clean, modern dark interface
- Responsive design untuk mobile & desktop
- Tailwind CSS tanpa gradient (solid colors only)

### 🚀 **Simple Mode (Default)**
1. Input API key sekali (disimpan otomatis)
2. Paste URL berita
3. Klik Generate
4. Download hasilnya!

### ⚙️ **Advanced Mode (Settings)**
Edit semua konfigurasi dari `config.py` langsung di web:
- Image dimensions dengan presets (Instagram, Twitter, dll)
- Typography settings
- Layout & spacing
- AI temperature
- Image extraction parameters
- AI prompt template

### 🖼️ **Gallery**
- Lihat semua posts yang sudah dibuat
- Preview, download, atau delete
- View full size dengan modal

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Web Server

```bash
python app.py
```

Server akan berjalan di `http://localhost:5000`

### 3. First Time Setup

1. Buka browser ke `http://localhost:5000`
2. Masukkan Gemini API key (hanya sekali)
3. Mulai generate!

## Usage

### Generate Post (Simple)

1. **Home Page** (`/`)
   - Paste article URL
   - (Optional) Add brand text
   - Click "Generate Post"
   - Wait for processing
   - Download hasil

### Advanced Settings

1. **Settings Page** (`/settings`)
   - Ubah image dimensions
   - Preset untuk Instagram Portrait/Square, Instagram Story, Twitter
   - Customize typography (font sizes, line height)
   - Adjust layout (margins, padding, radius)
   - Tune AI creativity (temperature slider)
   - Edit AI prompt template
   - Save changes

### Gallery

1. **Gallery Page** (`/gallery`)
   - View all generated posts
   - Grid view responsive
   - Download individual posts
   - View full size
   - Delete posts

## Responsive Design

### Mobile (< 768px)
- Single column layout
- Collapsible menu
- Touch-optimized buttons
- Full-width cards

### Tablet (768px - 1024px)
- 2-column gallery grid
- Side-by-side forms

### Desktop (> 1024px)
- Multi-column gallery (3-4 columns)
- Optimized spacing
- Larger preview images

## API Endpoints

### `POST /api/save-api-key`
Save Gemini API key to `.env`

**Request:**
```json
{
  "api_key": "your_key_here"
}
```

### `POST /api/generate`
Generate post from URL

**Request:**
```json
{
  "url": "https://example.com/article",
  "brand_text": "MyBrand"
}
```

**Response:**
```json
{
  "success": true,
  "filename": "post_xxx.png",
  "url": "/output/post_xxx.png"
}
```

### `POST /api/save-settings`
Save advanced settings to `config.py`

**Request:**
```json
{
  "IMAGE_WIDTH": 1080,
  "IMAGE_HEIGHT": 1350,
  ...
}
```

### `DELETE /api/delete/<filename>`
Delete generated post

### `GET /output/<filename>`
Serve generated image

## File Structure

```
headline-ai/
├── app.py                    # Flask application
├── templates/
│   ├── base.html            # Base template dengan Tailwind
│   ├── index.html           # Generate page
│   ├── gallery.html         # Gallery page
│   └── settings.html        # Settings page
├── static/
│   ├── css/                 # (Optional) Custom CSS
│   └── js/                  # (Optional) Custom JS
├── output/                  # Generated posts
└── web_settings.json        # Web UI settings
```

## Dark Mode Theme

### Color Palette

```javascript
{
  bg: '#0f172a',      // Background
  card: '#1e293b',    // Cards
  border: '#334155',  // Borders
  hover: '#475569',   // Hover states
}
```

### No Gradients
- All solid colors
- Clean, professional look
- Easy on the eyes

## Tips & Tricks

### 1. Quick Presets
Di Settings page, gunakan preset buttons untuk format umum:
- Instagram Portrait (1080x1350)
- Instagram Square (1080x1080)
- Instagram Story (1080x1920)
- Twitter (1200x675)

### 2. API Key Storage
- API key disimpan di `.env` file
- Aman dan persist across sessions
- Tidak perlu re-enter setiap kali

### 3. Progress Tracking
- Real-time progress bar
- Step-by-step status updates
- Estimated completion time

### 4. Keyboard Shortcuts
- `ESC` - Close image modal in gallery

## Troubleshooting

### Port Already in Use

```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### API Key Not Saving

- Check file permissions on `.env`
- Ensure web server has write access

### Settings Not Applying

- Click "Save Settings" button
- Restart Flask server untuk apply changes
- Check `config.py` untuk verify changes

### Images Not Loading

- Check `output/` directory exists
- Verify file permissions
- Clear browser cache

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using nginx

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /output/ {
        alias /path/to/headline-ai/output/;
    }
}
```

### Environment Variables

```bash
export FLASK_ENV=production
export SECRET_KEY=your_secret_key_here
python app.py
```

## Security Notes

⚠️ **Important for Production:**

1. Change `SECRET_KEY` in `app.py`
2. Set `debug=False` in production
3. Use environment variables for sensitive data
4. Add authentication if exposing publicly
5. Rate limit API endpoints
6. Validate all user inputs

## Screenshots

### Home Page
- Clean input form
- API key setup prompt
- Progress tracking
- Result preview

### Gallery
- Responsive grid
- Quick actions (download, view, delete)
- Image modal for full size view

### Settings
- Organized sections
- Preset buttons
- Real-time preview values
- Save/Reset options

## Support

- **Documentation**: [README.md](README.md)
- **Config Guide**: [CONFIG_GUIDE.md](CONFIG_GUIDE.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)

---

**Enjoy using Headline AI Web Interface!** 🎉
