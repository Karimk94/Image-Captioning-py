import os
import uuid
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from image_processor import processor_instance
from waitress import serve

# Initialize the Flask application
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image_from_form():
    """Handles image upload from the web form."""
    if 'image_file' not in request.files:
        return jsonify({'error': 'No image file provided.'}), 400

    file = request.files['image_file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid or no selected file.'}), 400

    # Save the file temporarily
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # Use the processor that reads from a file path
        result = processor_instance.process_image_from_path(filepath)
        if result:
            return jsonify(result)
        else:
            return jsonify({'error': 'Failed to process image with Ollama model.'}), 500
    except Exception as e:
        print(f"Error in Flask route: {e}")
        return jsonify({'error': 'An internal error occurred.'}), 500
    finally:
        # Clean up the uploaded file
        if os.path.exists(filepath):
             os.remove(filepath)

@app.route('/process_image_stream', methods=['POST'])
def process_image_stream():
    """
    Handles processing a single image sent as a raw byte stream.
    This is ideal for service-to-service communication.
    """
    try:
        image_bytes = request.get_data()
        if not image_bytes:
            return jsonify({'error': 'No image data in request body'}), 400

        # Use the new processor method that accepts bytes directly
        result = processor_instance.process_image_from_bytes(image_bytes)

        if result:
            return jsonify(result)
        else:
            return jsonify({'error': 'Failed to process image stream with Ollama.'}), 500
            
    except Exception as e:
        print(f"Error in Flask stream route: {e}")
        return jsonify({'error': 'Failed to process image from stream.'}), 500

if __name__ == '__main__':
    print("Serving on http://0.0.0.0:5001")
    serve(app, host='0.0.0.0', port=5001, threads=100)