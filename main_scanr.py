"""This script is used to merge individual images of a ScanR acquisition into single multichannel images.
Author: André Dias, 2026"""

import os
import tifffile as tiff
from HtImageFormater import HtImageFormater

def main():
    # --- Initialization ---
    image_formater = HtImageFormater()

    # --- User input for image directory ---
    img_dir = input("Enter the path to the image directory: ").strip('"')
    output_dir = input("Enter the path to the output directory: ").strip('"')

    # --- Read and process images ---
    image_formater.read_ScanR(img_dir)
    image_formater.export_images(output_dir=output_dir, channels=[2,3])

if __name__ == "__main__":
    main()