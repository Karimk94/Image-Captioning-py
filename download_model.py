import os
import certifi
from transformers import (
    AutoImageProcessor, 
    AutoModelForObjectDetection,
    BlipProcessor,
    BlipForConditionalGeneration
)

def download_all_models():
    """
    Downloads and saves all required AI models to local folders.
    """
    # Set SSL certificates to prevent connection errors during download
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    os.environ['SSL_CERT_FILE'] = certifi.where()

    # --- Model 1: Object Detection (YOLOS - a fully offline-compatible model) ---
    yolos_model_name = "hustvl/yolos-tiny"
    yolos_local_path = "./local-yolos-model"

    if not os.path.exists(yolos_local_path):
        print(f"\nDownloading Object Detection model: '{yolos_model_name}'...")
        try:
            image_processor = AutoImageProcessor.from_pretrained(yolos_model_name)
            model = AutoModelForObjectDetection.from_pretrained(yolos_model_name)
            
            os.makedirs(yolos_local_path, exist_ok=True)
            image_processor.save_pretrained(yolos_local_path)
            model.save_pretrained(yolos_local_path)
            print(f"Object Detection model saved to '{yolos_local_path}'")
        except Exception as e:
            print(f"FATAL: Error downloading YOLOS model: {e}")
            return
    else:
        print(f"Object Detection model already exists at '{yolos_local_path}'. Skipping.")

    # --- Model 2: Image Captioning (BLIP) ---
    blip_model_name = "Salesforce/blip-image-captioning-base"
    blip_local_path = "./local-blip-model"

    if not os.path.exists(blip_local_path):
        print(f"\nDownloading Image Captioning model: '{blip_model_name}'...")
        try:
            processor = BlipProcessor.from_pretrained(blip_model_name)
            model = BlipForConditionalGeneration.from_pretrained(blip_model_name)

            os.makedirs(blip_local_path, exist_ok=True)
            processor.save_pretrained(blip_local_path)
            model.save_pretrained(blip_local_path)
            print(f"Image Captioning model saved to '{blip_local_path}'")
        except Exception as e:
            print(f"FATAL: Error downloading BLIP model: {e}")
            return
    else:
        print(f"Image Captioning model already exists at '{blip_local_path}'. Skipping.")
    
    print("\nAll models are downloaded and ready for offline use.")


if __name__ == "__main__":
    download_all_models()
