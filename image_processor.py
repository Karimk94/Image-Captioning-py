import requests
import base64
import os
import json
from PIL import Image
import io
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get Ollama configuration from environment variables with defaults
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:12b") 

class OllamaVisionProcessor:
    """
    A processor that uses a local Ollama multimodal model to analyze an image.
    It generates a caption and a list of descriptive tags.
    """

    def _analyze_with_ollama(self, image_bytes):
        """
        Private helper method to encode an image and call the Ollama API.
        
        Args:
            image_bytes (bytes): The raw bytes of the image in JPEG format.

        Returns:
            dict: The parsed JSON response from the Ollama model or None on failure.
        """
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')

        prompt = """
        Analyze the image and respond with a single JSON object.
        The JSON object must contain two keys:
        1. "caption": A brief description of the main social interaction and location. Focus on the general activity (e.g., "people discussing in a meeting room"). Do NOT describe clothing, colors, or specific details like eating or drinking.
        2. "tags": A JSON array of 5-10 key concepts related to the setting and activity.
        """

        print(f"Sending request to Ollama model: {OLLAMA_MODEL}...")
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "images": [encoded_image],
            "format": "json",
            "stream": False
        }

        response = requests.post(OLLAMA_API_URL, json=payload, timeout=300)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        
        response_data = response.json()
        json_string = response_data.get("response", "{}")
        
        try:
            analysis_result = json.loads(json_string)
            print("Successfully received and parsed response from Ollama.")
            # Add the original image data to the result for display purposes
            analysis_result["image_data"] = encoded_image
            return analysis_result
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from model response: {json_string}")
            return None


    def process_image_from_bytes(self, image_bytes):
        """
        Processes an image directly from a byte stream.

        Args:
            image_bytes (bytes): The raw bytes of the image.

        Returns:
            dict: A dictionary with the analysis results, or None on failure.
        """
        try:
            with Image.open(io.BytesIO(image_bytes)) as img:
                rgb_image = img.convert('RGB')
                buffered = io.BytesIO()
                rgb_image.save(buffered, format="JPEG")
                jpeg_bytes = buffered.getvalue()
                
            return self._analyze_with_ollama(jpeg_bytes)

        except Exception as e:
            print(f"An unexpected error occurred during byte processing: {e}")
            return None


    def process_image_from_path(self, image_path):
        """
        Processes an image from a local file path. This is used by the web UI.

        Args:
            image_path (str): The file path to the image.

        Returns:
            dict: A dictionary with the analysis results, or None on failure.
        """
        try:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            return self.process_image_from_bytes(image_bytes)

        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during path processing: {e}")
            return None

# Create a single instance to be used by the Flask app
processor_instance = OllamaVisionProcessor()