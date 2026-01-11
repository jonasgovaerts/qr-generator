from flask import Flask, render_template, request, send_file, jsonify
import qrcode
from PIL import Image
import os
import uuid
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Ensure data directory exists
DATA_DIR = './data'
os.makedirs(DATA_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.json.get('data')
    filename = request.json.get('filename', None)
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # If custom filename is provided, use it; otherwise generate unique filename
        if filename:
            # Validate filename (only alphanumeric, underscores, hyphens, and dots)
            allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.')
            if not all(c in allowed_chars for c in filename):
                return jsonify({'error': 'Invalid filename. Only alphanumeric, underscores, hyphens, and dots are allowed.'}), 400
            
            # Ensure it has .png extension
            if not filename.endswith('.png'):
                filename += '.png'
        else:
            # Generate unique filename
            filename = f"{uuid.uuid4().hex}.png"
        
        file_path = os.path.join(DATA_DIR, filename)
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(file_path)
        
        logger.info(f'QR code generated: {filename}')
        return jsonify({'filename': filename, 'url': f'/download/{filename}'})
    except Exception as e:
        logger.error(f'Error generating QR code: {str(e)}')
        return jsonify({'error': 'Failed to generate QR code'}), 500

@app.route('/download/<filename>')
def download_qr(filename):
    try:
        file_path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logger.error(f'Error downloading file {filename}: {str(e)}')
        return jsonify({'error': 'Failed to download file'}), 500

@app.route('/delete/<filename>')
def delete_qr(filename):
    try:
        file_path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        os.remove(file_path)
        logger.info(f'File deleted: {filename}')
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f'Error deleting file {filename}: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/list_qrs')
def list_qrs():
    try:
        files = os.listdir(DATA_DIR)
        qr_files = [f for f in files if f.endswith('.png')]
        return jsonify({'files': qr_files})
    except Exception as e:
        logger.error(f'Error listing files: {str(e)}')
        return jsonify({'error': 'Failed to list files'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)