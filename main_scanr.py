"""This script is used to merge individual images of a ScanR acquisition into single multichannel images.
Author: André Dias, 2026

"""
channels = None # List of channel numbers to include in the output images or leave as None to include all channels. 
# channels = [1,2,3] # Example of how to specify channels to include in the output images. This will include channels 1, 2, and 3 in the output images. You can set a channel to 0 to include it as an empty frame.
# Note: The channel numbers correspond to the acquisition channels sorted alphabetically by their names. For example, if the channel names are "DAPI", "GFP", and "Cy5", then channel 1 corresponds to "Cy5",
# channel 2 corresponds to "DAPI", and channel 3 corresponds to "GFP". If you want to include all channels, simply set channels = None.


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
    image_formater.export_images(output_dir=output_dir, channels=channels)

if __name__ == "__main__":
    main()