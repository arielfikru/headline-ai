#!/usr/bin/env python3
"""
Flask Web UI for Headline AI Generator
"""

import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import config
from headline_generator import HeadlineGenerator

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Store settings in a JSON file
SETTINGS_FILE = 'web_settings.json'


def load_settings():
    """Load settings from JSON file"""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_settings(settings):
    """Save settings to JSON file"""
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)


@app.route('/')
def index():
    """Main page"""
    settings = load_settings()
    return render_template('index.html', settings=settings)


@app.route('/settings')
def settings_page():
    """Advanced settings page"""
    # Get all config values
    config_values = {
        'IMAGE_WIDTH': config.IMAGE_WIDTH,
        'IMAGE_HEIGHT': config.IMAGE_HEIGHT,
        'TITLE_FONT_SIZE': config.TITLE_FONT_SIZE,
        'SOURCE_FONT_SIZE': config.SOURCE_FONT_SIZE,
        'BOX_MARGIN': config.BOX_MARGIN,
        'BOX_PADDING': config.BOX_PADDING,
        'BOX_RADIUS': config.BOX_RADIUS,
        'LINE_HEIGHT': config.LINE_HEIGHT,
        'MAX_TITLE_LENGTH': config.MAX_TITLE_LENGTH,
        'GEMINI_MODEL': config.GEMINI_MODEL,
        'GEMINI_TEMPERATURE': config.GEMINI_TEMPERATURE,
        'MIN_IMAGE_WIDTH': config.MIN_IMAGE_WIDTH,
        'MIN_IMAGE_HEIGHT': config.MIN_IMAGE_HEIGHT,
        'MAX_IMAGE_CANDIDATES': config.MAX_IMAGE_CANDIDATES,
        'AI_PROMPT_TEMPLATE': config.AI_PROMPT_TEMPLATE,
    }

    settings = load_settings()
    return render_template('settings.html', config=config_values, settings=settings)


@app.route('/gallery')
def gallery():
    """Gallery of generated posts"""
    output_dir = config.OUTPUT_DIR
    posts = []

    if os.path.exists(output_dir):
        for filename in sorted(os.listdir(output_dir), reverse=True):
            if filename.endswith('.png'):
                filepath = os.path.join(output_dir, filename)
                stat = os.stat(filepath)
                posts.append({
                    'filename': filename,
                    'created': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
                    'size': f"{stat.st_size / 1024:.1f} KB"
                })

    return render_template('gallery.html', posts=posts)


@app.route('/api/save-api-key', methods=['POST'])
def save_api_key():
    """Save API key to settings"""
    data = request.get_json()
    api_key = data.get('api_key', '').strip()

    if not api_key:
        return jsonify({'success': False, 'error': 'API key is required'})

    # Save to .env file
    env_content = []
    env_file = '.env'

    # Read existing .env
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            env_content = f.readlines()

    # Update or add GEMINI_API_KEY
    updated = False
    for i, line in enumerate(env_content):
        if line.startswith('GEMINI_API_KEY='):
            env_content[i] = f'GEMINI_API_KEY={api_key}\n'
            updated = True
            break

    if not updated:
        env_content.append(f'GEMINI_API_KEY={api_key}\n')

    # Write back to .env
    with open(env_file, 'w') as f:
        f.writelines(env_content)

    # Update settings
    settings = load_settings()
    settings['api_key_set'] = True
    save_settings(settings)

    return jsonify({'success': True})


@app.route('/api/save-settings', methods=['POST'])
def save_advanced_settings():
    """Save advanced settings"""
    data = request.get_json()

    # Update config.py with new values
    config_content = []

    with open('config.py', 'r') as f:
        config_content = f.readlines()

    # Update values (simple string replacement)
    replacements = {
        'IMAGE_WIDTH': data.get('IMAGE_WIDTH'),
        'IMAGE_HEIGHT': data.get('IMAGE_HEIGHT'),
        'TITLE_FONT_SIZE': data.get('TITLE_FONT_SIZE'),
        'SOURCE_FONT_SIZE': data.get('SOURCE_FONT_SIZE'),
        'BOX_MARGIN': data.get('BOX_MARGIN'),
        'BOX_PADDING': data.get('BOX_PADDING'),
        'BOX_RADIUS': data.get('BOX_RADIUS'),
        'LINE_HEIGHT': data.get('LINE_HEIGHT'),
        'MAX_TITLE_LENGTH': data.get('MAX_TITLE_LENGTH'),
        'GEMINI_TEMPERATURE': data.get('GEMINI_TEMPERATURE'),
        'MIN_IMAGE_WIDTH': data.get('MIN_IMAGE_WIDTH'),
        'MIN_IMAGE_HEIGHT': data.get('MIN_IMAGE_HEIGHT'),
        'MAX_IMAGE_CANDIDATES': data.get('MAX_IMAGE_CANDIDATES'),
    }

    for i, line in enumerate(config_content):
        for key, value in replacements.items():
            if value is not None and line.strip().startswith(f'{key} ='):
                config_content[i] = f'{key} = {value}\n'

    # Handle prompt template separately
    if data.get('AI_PROMPT_TEMPLATE'):
        # This is complex, skip for now or handle carefully
        pass

    with open('config.py', 'w') as f:
        f.writelines(config_content)

    # Reload config module
    import importlib
    importlib.reload(config)

    return jsonify({'success': True})


@app.route('/api/generate', methods=['POST'])
def generate_post():
    """Generate post from URL"""
    data = request.get_json()
    url = data.get('url', '').strip()
    brand_text = data.get('brand_text', '').strip()

    if not url:
        return jsonify({'success': False, 'error': 'URL is required'})

    # Check if API key is set
    if not os.getenv('GEMINI_API_KEY'):
        return jsonify({'success': False, 'error': 'API key not set. Please set it in settings.'})

    try:
        generator = HeadlineGenerator()
        output_path = generator.generate_post(url, brand_text=brand_text or None)

        # Get filename
        filename = os.path.basename(output_path)

        return jsonify({
            'success': True,
            'filename': filename,
            'url': f'/output/{filename}'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/output/<filename>')
def serve_output(filename):
    """Serve generated images"""
    return send_from_directory(config.OUTPUT_DIR, filename)


@app.route('/api/delete/<filename>', methods=['DELETE'])
def delete_post(filename):
    """Delete a generated post"""
    try:
        filepath = os.path.join(config.OUTPUT_DIR, secure_filename(filename))
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'File not found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    # Create output directory
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    # Run app
    print("\n" + "="*60)
    print("Headline AI - Web Interface")
    print("="*60)
    print("\nStarting server at http://localhost:5000")
    print("Press Ctrl+C to stop\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
