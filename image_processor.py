from transformers import pipeline, BlipProcessor, BlipForConditionalGeneration
from PIL import Image, ImageDraw, ImageFont
import requests
import io
import base64

class ImageProcessor:
    """
    A class that combines object detection and image captioning.
    """

    def __init__(self, detector_path="./local-detr-model", captioner_path="./local-blip-model"):
        """
        Initializes by loading both the object detector and the image captioner
        from local paths.
        """
        print(f"Initializing Object Detector from: {detector_path}")
        self.detector = pipeline("object-detection", model=detector_path)
        print("Object Detector initialized.")

        print(f"Initializing Image Captioner from: {captioner_path}")
        self.caption_processor = BlipProcessor.from_pretrained(captioner_path)
        self.caption_model = BlipForConditionalGeneration.from_pretrained(captioner_path)
        print("Image Captioner initialized.")

    def process_image(self, image_path_or_url):
        """
        Performs both object detection and captioning on an image.

        Returns:
            A dictionary containing the processed image (Base64) and the caption (text).
        """
        try:
            if image_path_or_url.startswith(('http://', 'https://')):
                raw_image = Image.open(requests.get(image_path_or_url, stream=True).raw).convert('RGB')
            else:
                raw_image = Image.open(image_path_or_url).convert('RGB')

            # --- 1. Generate Caption ---
            caption_inputs = self.caption_processor(raw_image, return_tensors="pt")
            caption_out = self.caption_model.generate(**caption_inputs)
            caption = self.caption_processor.decode(caption_out[0], skip_special_tokens=True)

            # --- 2. Detect Objects and Draw on the Image ---
            objects = self.detector(raw_image)
            draw = ImageDraw.Draw(raw_image)
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except IOError:
                font = ImageFont.load_default()

            for obj in objects:
                if obj['score'] > 0.9:
                    box = obj['box']
                    label = obj['label']
                    xmin, ymin, xmax, ymax = box['xmin'], box['ymin'], box['xmax'], box['ymax']
                    draw.rectangle(((xmin, ymin), (xmax, ymax)), outline="red", width=3)
                    text_bbox = draw.textbbox((xmin, ymin), label, font=font)
                    draw.rectangle(text_bbox, fill="red")
                    draw.text((xmin, ymin), label, fill="white", font=font)

            # --- 3. Prepare Response ---
            buffer = io.BytesIO()
            raw_image.save(buffer, format="JPEG")
            img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
            
            return {
                "image_data": img_str,
                "caption": caption
            }

        except Exception as e:
            print(f"Error during image processing: {e}")
            return None

# Create a single instance to be used by the Flask app
processor_instance = ImageProcessor()
