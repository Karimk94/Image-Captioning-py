# app.py

from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from image_captioning import captioner_instance # Import the singleton instance

# Initialize the Flask application
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Checks if the file's extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/generate_caption', methods=['POST'])
def generate_caption_route():
    """Handles the caption generation request."""
    if 'image_file' not in request.files and 'image_url' not in request.form:
        return jsonify({'error': 'No image file or URL provided.'}), 400

    image_source = None
    
    # --- Handle File Upload ---
    if 'image_file' in request.files:
        file = request.files['image_file']
        if file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_source = filepath
    
    # --- Handle URL ---
    if 'image_url' in request.form and request.form['image_url']:
        image_source = request.form['image_url']

    if not image_source:
        return jsonify({'error': 'Invalid image source.'}), 400

    # --- Generate Caption ---
    try:
        # Use the pre-loaded captioner instance
        caption = captioner_instance.generate_caption(image_source)
        return jsonify({'caption': caption})
    except Exception as e:
        print(f"Error in Flask route: {e}")
        return jsonify({'error': 'Failed to generate caption.'}), 500
    finally:
        # --- Cleanup: Remove the uploaded file ---
        if image_source and os.path.exists(image_source) and not image_source.startswith('http'):
             os.remove(image_source)


if __name__ == '__main__':
    # Runs the Flask app
    # debug=True will auto-reload the server when you make changes
    app.run(debug=True)
