import cv2
import mediapipe as mp
import numpy as np
import os
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision

# Use absolute path for safety
MODEL_PATH = r"c:\Users\SHASIHINI MALSHA\Development\lomiees\utils\pose_landmarker.task"
IMAGE_PATH = r"c:\Users\SHASIHINI MALSHA\Development\lomiees\static\uploads\test_person.jpg"

def test_segmentation():
    print("Initializing landmarker with segmentation...")
    base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
    options = mp_vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=mp_vision.RunningMode.IMAGE,
        output_segmentation_masks=True
    )
    landmarker = mp_vision.PoseLandmarker.create_from_options(options)
    
    print(f"Loading image: {IMAGE_PATH}")
    img_bgr = cv2.imread(IMAGE_PATH)
    if img_bgr is None:
        print("Failed to load image.")
        return
    
    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    
    print("Running detection...")
    result = landmarker.detect(mp_img)
    print("Detection finished.")
    
    if result.segmentation_masks:
        print(f"Successfully got {len(result.segmentation_masks)} segmentation masks.")
    else:
        print("No segmentation masks found.")
        
    landmarker.close()

if __name__ == "__main__":
    try:
        test_segmentation()
    except Exception as e:
        print(f"Error during test: {e}")
