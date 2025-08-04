from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import requests

class ImageCaptioner:
    """
    A class to generate captions for images using a pre-trained model.
    """

    def __init__(self, model_name="Salesforce/blip-image-captioning-base"):
        """
        Initializes the ImageCaptioner by loading the pre-trained model and processor.
        This is done once when the Flask app starts.

        Args:
            model_name (str): The name of the pre-trained model from Hugging Face.
        """
        print("Initializing model... This may take a moment.")
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)
        print("Model initialized successfully.")

    def generate_caption(self, image_path_or_url):
        """
        Generates a caption for a given image from a local path or a URL.

        Args:
            image_path_or_url (str): The local path or URL of the image.

        Returns:
            str: The generated caption for the image.
        """
        try:
            if image_path_or_url.startswith(('http://', 'https://')):
                # Handle image from URL
                raw_image = Image.open(requests.get(image_path_or_url, stream=True).raw).convert('RGB')
            else:
                # Handle image from local file path
                raw_image = Image.open(image_path_or_url).convert('RGB')

            # --- Conditional vs. Unconditional Captioning ---
            # For unconditional captioning (just describing the image):
            inputs = self.processor(raw_image, return_tensors="pt")
            
            # For conditional captioning (e.g., asking a question about the image):
            # text = "a photography of"
            # inputs = self.processor(raw_image, text, return_tensors="pt")

            # Generate the caption
            out = self.model.generate(**inputs)

            # Decode the caption
            caption = self.processor.decode(out[0], skip_special_tokens=True)
            return caption

        except Exception as e:
            print(f"Error during caption generation: {e}")
            return "Sorry, I couldn't generate a caption for that image."

# Create a single instance of the captioner to be used by the Flask app.
# This avoids reloading the model on every request.
captioner_instance = ImageCaptioner()
