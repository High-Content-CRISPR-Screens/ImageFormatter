"""This script is used to merge individual images of a ScanR acquisition into single multichannel images.
Author: André Dias, 2026"""

import os
import tifffile as tiff
from HtImageFormatter import HtImageFormatter

def main():
    # --- Initialization ---
    image_formatter = HtImageFormatter()

    # --- User input for image directory ---
    img_dir = input("Enter the path to the image directory: ").strip('"')

    # --- Read and process images ---
    image_formatter.read_ScanR(img_dir)
    
    output_dir = os.path.join(img_dir, "tiff_images")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for i in range(image_formatter.nImages()):
        img = image_formatter.prepare_multichannel_image(i)
        tiff.imwrite(os.path.join(output_dir, f"image_{i}.tif"), img)

if __name__ == "__main__":
    main()