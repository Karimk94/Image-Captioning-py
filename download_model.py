from transformers import (
    AutoImageProcessor, 
    AutoModelForObjectDetection,
    BlipProcessor,
    BlipForConditionalGeneration
)
import os

def download_models():
    """
    Downloads and saves all required AI models to local folders.
    """
    # --- Model 1: Object Detection (DETR) ---
    detr_model_name = "facebook/detr-resnet-50"
    detr_local_path = "./local-detr-model"

    if not os.path.exists(detr_local_path):
        print(f"Downloading Object Detection model: '{detr_model_name}'...")
        try:
            image_processor = AutoImageProcessor.from_pretrained(detr_model_name)
            model = AutoModelForObjectDetection.from_pretrained(detr_model_name)
            
            os.makedirs(detr_local_path, exist_ok=True)
            image_processor.save_pretrained(detr_local_path)
            model.save_pretrained(detr_local_path)
            print(f"Object Detection model saved to '{detr_local_path}'")
        except Exception as e:
            print(f"Error downloading DETR model: {e}")
    else:
        print(f"Object Detection model already exists at '{detr_local_path}'. Skipping.")

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
            print(f"Error downloading BLIP model: {e}")
    else:
        print(f"Image Captioning model already exists at '{blip_local_path}'. Skipping.")


if __name__ == "__main__":
    download_models()
