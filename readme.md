AI Image Analyzer (with Ollama)

This is a self-contained web application built with Flask that performs image analysis using a local multimodal Large Language Model (LLM) running on Ollama. It replaces the need for multiple, specialized AI models with a single, powerful one.

The application takes an image upload and generates:

A natural, human-like sentence describing the entire scene.

A list of relevant tags for searching or filtering.

Features

Single Model, Multiple Tasks: Uses one multimodal LLM (e.g., Gemma, LLaVA) via Ollama to handle both captioning and tagging.

100% Local & Offline: After setting up Ollama, the entire application runs on your local machine with no need for an internet connection or external API keys.

Simple RESTful Backend: Built with Flask, providing a clean and simple foundation.

Modern UI: A clean, responsive user interface for uploading images and viewing results.

How It Works

Frontend (HTML, CSS, JS): A user uploads an image through the web interface.

Backend (Flask): The Python Flask server receives the image.

AI Processor (image_processor.py):

The image is encoded into a Base64 string.

A carefully crafted prompt is created, instructing the LLM to return a JSON object containing a caption and a list of tags.

A single API call is made to the local Ollama server (http://localhost:11434).

Response: The backend sends a single JSON response to the frontend containing:

The original uploaded image (as a Base64 string).

The generated caption.

A list of generated tags.

Display: The frontend JavaScript dynamically renders the image, caption, and tags for the user.

Setup and Installation

Follow these steps to run the application on your local machine.

Prerequisites

Python 3.7+ and pip.

Ollama: You must have Ollama installed and running. You can download it from ollama.com.

A Multimodal Model: You need to pull a multimodal model. We recommend gemma3:12b or llava. Open your terminal and run:

ollama pull gemma3:12b


(This step requires an internet connection.)

Installation Steps

Clone the Repository
Clone or download the project files to your local machine.

Create a Virtual Environment (Recommended)

# Navigate to the project directory
cd /path/to/image-captioning-py

# Create the environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate


Install Dependencies
Install the required Python libraries.

pip install -r requirements.txt


Configure Environment Variables
Create a file named .env in the root of the project directory. You can copy the example file:

# On Windows
copy .env.example .env
# On macOS/Linux
cp .env.example .env


Open the .env file and ensure the variables are correct for your setup. The defaults should work if Ollama is running on the standard port.

# .env
OLLAMA_API_URL="http://localhost:11434/api/generate"
OLLAMA_MODEL="gemma3:12b"


Run the Application
You can now start the Flask server.

python app.py


Access the Application
Open your web browser and navigate to:
http://127.0.0.1:5001

Project Structure

/image-captioning-py
|
|-- app.py                  # Main Flask application
|-- image_processor.py      # The core class that calls the Ollama API
|-- requirements.txt        # Python dependencies
|-- .env.example            # Example environment variables
|-- readme.md               # This file
|
|-- templates/
|   |-- index.html          # Main HTML user interface
|
|-- static/
|   |-- css/style.css
|   |-- js/script.js
|
|-- uploads/                # Temporary folder for uploaded images