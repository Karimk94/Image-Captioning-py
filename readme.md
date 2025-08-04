AI Image Captioning Web Application
This is a web-based application built with Flask that uses a powerful deep learning model to automatically generate descriptive captions for images. Users can either upload an image file directly or provide a URL to an image online.
Features
Generate Captions from Files: Upload JPG, PNG, or other common image formats.
Generate Captions from URLs: Simply paste a link to an image.
Modern UI: A clean, user-friendly interface for easy interaction.
RESTful Backend: Built with Flask, providing a simple and scalable foundation.
State-of-the-Art AI: Powered by the Hugging Face transformers library and the pre-trained Salesforce BLIP model for high-quality image understanding.
How It Works
The application uses a client-server architecture:
Frontend (HTML, CSS, JavaScript): The user interacts with a web page to upload an image or submit a URL. JavaScript handles the form submission asynchronously, providing a smooth user experience without page reloads.
Backend (Flask): The Python-based Flask server receives the image.
AI Model (Hugging Face Transformers): The backend uses the image_captioning.py module, which contains a pre-loaded instance of the BLIP (Bootstrapping Language-Image Pre-training) model. This model processes the image and generates a text caption.
Response: The generated caption is sent back to the frontend as a JSON response and displayed to the user.
Project Structure
The project is organized using a standard Flask application structure for clarity and maintainability.
/image-captioning-flask
|
|-- app.py                  # Main Flask application file (routing, app logic)
|-- image_captioning.py     # The ImageCaptioner class and its logic
|-- requirements.txt        # Lists all the Python dependencies for the project
|-- README.md               # This file
|
|-- templates/
|   |-- index.html          # The main HTML page for the user interface
|
|-- static/
|   |-- css/
|   |   |-- style.css       # Stylesheet for the application
|   |-- js/
|       |-- script.js       # JavaScript for handling form submission and UI updates
|
|-- uploads/                # A temporary folder for user-uploaded images


Setup and Installation
Follow these steps to run the application on your local machine.
Prerequisites
Python 3.7 or newer
pip (Python package installer)
Installation Steps
Clone the Repository
If you are using git, clone the repository to your local machine:
git clone <your-repository-url>
cd image-captioning-flask

If not using git, simply create the folder structure and files as described above.
Create a Virtual Environment (Recommended)
It's highly recommended to create a virtual environment to keep project dependencies isolated.
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate


Install Dependencies
Install all the required Python libraries from the requirements.txt file.
pip install -r requirements.txt

Note: The first time you run the app, the script will download the pre-trained model files, which may take a few minutes depending on your internet connection.
Run the Application
Start the Flask development server:
flask run

Alternatively, you can run python app.py.
Access the Application
Open your web browser and navigate to:
http://127.0.0.1:5000
Future Improvements
Fine-Tuning Interface: Build a section in the web app to allow users to upload a dataset of images and corresponding text files to fine-tune the model on custom data.
Model Selection: Allow users to choose from different pre-trained image captioning models available on Hugging Face.
Batch Processing: Implement a feature to upload multiple images at once and receive a list of captions.
Containerization: Add a Dockerfile to easily deploy the application using Docker.
