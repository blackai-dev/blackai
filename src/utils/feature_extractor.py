import numpy as np
from PIL import Image

def extract_features(image_path):
    """Extract RGB, brightness, and contrast from an image."""
    image = Image.open(image_path)
    np_image = np.array(image)
    mean_rgb = np.mean(np_image, axis=(0, 1))  # RGB mean
    brightness = np.mean(np.max(np_image / 255.0, axis=2)) * 255
    contrast = np.std(np_image)
    return mean_rgb.tolist() + [brightness, contrast]

