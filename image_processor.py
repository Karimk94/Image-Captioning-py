from transformers import pipeline, BlipProcessor, BlipForConditionalGeneration, AutoImageProcessor, AutoModelForObjectDetection
from PIL import Image, ImageDraw, ImageFont
import requests
import io
import base64
import logging
import torch

class ImageProcessor:
    """
    A class that combines object detection and image captioning. It generates a natural
    caption and then appends any detected objects that were not mentioned.
    """

    def __init__(self, detector_path="./local-yolos-model", captioner_path="./local-blip-model"):
        """
        Initializes by loading both models from local paths in a strictly offline manner.
        """
        
        print(f"Initializing Object Detector from: {detector_path} (Strict Offline Mode)")
        self.detector_processor = AutoImageProcessor.from_pretrained(detector_path, local_files_only=True)
        self.detector_model = AutoModelForObjectDetection.from_pretrained(detector_path, local_files_only=True)
        print("Object Detector (YOLOS) initialized successfully.")

        print(f"Initializing Image Captioner from: {captioner_path} (Strict Offline Mode)")
        self.caption_processor = BlipProcessor.from_pretrained(
            captioner_path, 
            local_files_only=True
        )
        self.caption_model = BlipForConditionalGeneration.from_pretrained(
            captioner_path, 
            local_files_only=True
        )
        print("Image Captioner initialized.")

    def process_image(self, image_path_or_url):
        """
        Performs both object detection and captioning on an image.
        """
        try:
            if image_path_or_url.startswith(('http://', 'https://')):
                raw_image = Image.open(requests.get(image_path_or_url, stream=True).raw).convert('RGB')
            else:
                raw_image = Image.open(image_path_or_url).convert('RGB')

            # --- 1. Detect Objects and Collect Tags using YOLOS ---
            inputs = self.detector_processor(images=raw_image, return_tensors="pt")
            outputs = self.detector_model(**inputs)
            
            target_sizes = torch.tensor([raw_image.size[::-1]])
            results = self.detector_processor.post_process_object_detection(
                outputs, threshold=0.8, target_sizes=target_sizes
            )[0]

            draw = ImageDraw.Draw(raw_image)
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except IOError:
                font = ImageFont.load_default()

            detected_tags = set()

            for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
                label_name = self.detector_model.config.id2label[label.item()]
                detected_tags.add(label_name)
                
                if score > 0.9:
                    box = [round(i, 2) for i in box.tolist()]
                    xmin, ymin, xmax, ymax = box
                    
                    draw.rectangle(((xmin, ymin), (xmax, ymax)), outline="blue", width=3)
                    text_bbox = draw.textbbox((xmin, ymin), label_name, font=font)
                    draw.rectangle(text_bbox, fill="blue")
                    draw.text((xmin, ymin), label_name, fill="white", font=font)
            
            sorted_tags = sorted(list(detected_tags))

            # --- 2. Generate a Natural, Unconditional Caption ---
            logging.info("Generating a natural, unconditional caption...")
            caption_inputs = self.caption_processor(raw_image, return_tensors="pt")
            caption_out = self.caption_model.generate(**caption_inputs)
            base_caption = self.caption_processor.decode(caption_out[0], skip_special_tokens=True)

            # --- 3. Enrich the Caption with Missing Tags ---
            final_caption = base_caption
            missing_tags = []
            # Check which tags are not already mentioned in the base caption
            for tag in sorted_tags:
                # A simple check to see if the tag word is in the caption
                if tag not in final_caption.lower():
                    missing_tags.append(tag)
            
            # If there are missing tags, append them to the caption
            if missing_tags:
                tags_to_add_str = ", ".join(missing_tags)
                final_caption += f", and also {tags_to_add_str}."
                logging.info(f"Enriched caption with missing tags: {tags_to_add_str}")


            # --- 4. Prepare Response ---
            buffer = io.BytesIO()
            raw_image.save(buffer, format="JPEG")
            img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
            
            return {
                "image_data": img_str,
                "caption": final_caption,
                "tags": sorted_tags
            }

        except Exception as e:
            print(f"Error during image processing: {e}")
            return None

# Create a single instance to be used by the Flask app
processor_instance = ImageProcessor()
