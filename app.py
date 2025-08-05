from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from image_processor import processor_instance # Import the new processor

# Initialize the Flask application
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image_route():
    if 'image_file' not in request.files:
        return jsonify({'error': 'No image file provided.'}), 400

    file = request.files['image_file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid or no selected file.'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # Use the pre-loaded processor instance to get both results
        result = processor_instance.process_image(filepath)
        if result:
            # Return the dictionary with image data and caption
            return jsonify(result)
        else:
            return jsonify({'error': 'Failed to process image.'}), 500
    except Exception as e:
        print(f"Error in Flask route: {e}")
        return jsonify({'error': 'Failed to process image.'}), 500
    finally:
        if os.path.exists(filepath):
             os.remove(filepath)

if __name__ == '__main__':
    # Run on port 5001 to avoid conflict
    app.run(port=5001, debug=False)
