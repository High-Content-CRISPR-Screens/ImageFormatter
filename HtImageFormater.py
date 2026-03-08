"""Image formatter for high-throughput imaging.
This module contains the HtImageFormatter class, which is designed to help read and process images from high-throughput microscopy.  
Author: André Dias, 2026"""

import os
import pandas as pd
import numpy as np
import tifffile as tiff
from tqdm.auto import tqdm
from itertools import product


class HtImageFormater:
    def __init__(self):
        """Initialize the HtImageFormatter class."""
        self._image_data = None
        self._data_path = None
        self._experiment_name = None
        self._source_microscope = None
    
    # --- Loading functions ---
    def read_ScanR(self, image_dir: str):
        """Read and process images from a ScanR acquisition.
        Args:
            image_dir (str): Path to the directory containing the ScanR images.
        """
        self._source_microscope = "ScanR"
        self._experiment_name = image_dir.split("\\")[-1]
        self._data_path = os.path.join(image_dir, "data")
        self._image_data = pd.DataFrame()
        file_list = os.listdir(self._data_path)
        self._image_data['image_names'] = file_list
        self._image_data['image_paths'] = [os.path.join(self._data_path, name) for name in file_list] 
        image_info = [name.split("--") for name in file_list]
        self._image_data['well_names'] = [elem[0] for elem in image_info]
        self._image_data['well_numbers'] = [int(elem[1].strip('W')) for elem in image_info]
        self._image_data['site']= [int(elem[2].strip('P')) for elem in image_info]
        self._image_data['z-index'] = [int(elem[3].strip('Z')) for elem in image_info]
        self._image_data['time'] = [int(elem[4].strip('T')) for elem in image_info]
        self._image_data['channel_name'] = [elem[5].strip('.tif') for elem in image_info]
        self._image_data.sort_values(by=['well_numbers', 'site', 'z-index', 'time', 'channel_name'], inplace=True)
        self._image_data['channel_number'],_ = pd.factorize(self._image_data['channel_name'])
        self._image_data['channel_number'] += 1
        self._image_data["image_id"] = self._image_data.groupby(["well_names", "site"], sort=False).ngroup() + 1
        self._image_data = self._image_data.reset_index(drop=True)
        
    def validate_image_data(self):
        """Validate that the image data has been loaded."""
        if self._image_data is None:
            raise ValueError("Image data not loaded. Please load the data first.")
    
    def nImages(self):
        """Return the number of unique images in the dataset."""
        self.validate_image_data()
        return len(self._image_data['image_id'].unique())
    
    def get_well_name(self, image_id: int):
        """Get the well name for a given image ID.
        Args:
            image_id (int): The ID of the image."""
        self.validate_image_data()
        return self._image_data[self._image_data["image_id"] == image_id]["well_names"].iloc[0]

    def get_site(self, image_id: int):
        """Get the site number for a given image ID.
        Args:
            image_id (int): The ID of the image."""
        self.validate_image_data()
        return self._image_data[self._image_data["image_id"] == image_id]["site"].iloc[0]
    
    def get_image_id(self, well_name: str, site: int):
        """Get the image ID for a given well name and site number
        Args:
            well_name (str): The name of the well.
            site (int): The site number."""
        self.validate_image_data()
        row = self._image_data[
            (self._image_data["well_names"] == well_name) &
            (self._image_data["site"] == site)
        ]
        if row.empty:
            raise ValueError(f"No image found for well name '{well_name}' and site '{site}'.")
        return row["image_id"].iloc[0]
    
    def prepare_multichannel_image(self, image_id: int = 1, channels: list = None, z_indices: list = None, times: list = None, show_progress: bool = True):
        """Prepare a multichannel image for a given image ID.
        Args:
            image_id (int): The ID of the image to prepare.
            channels (list): List of channel numbers to include in the final image. If None, all channels will be included.If 0 is included, it will place an empty image.
            z_indices (list): List of z-index values to include in the final image. If None, all z-index values will be included.
            times (list): List of time points to include in the final image. If None, all time points will be included.
            show_progress (bool): If True, display a progress bar while building the image."""
        self.validate_image_data()

        grp = self._image_data[self._image_data["image_id"] == image_id].copy()

        if channels is None:
            channels = grp["channel_number"].unique()
        if z_indices is None:
            z_indices = grp["z-index"].unique()
        if times is None:
            times = grp["time"].unique()

        c_to_idx = {c: idx for idx, c in enumerate(channels)}
        z_to_idx = {z: idx for idx, z in enumerate(z_indices)}
        t_to_idx = {t: idx for idx, t in enumerate(times)}

        first_img = tiff.imread(grp.iloc[0]["image_paths"])
        y, x = first_img.shape  # image is (Y, X)

        final_img = np.zeros((y, x, len(channels), len(z_indices), len(times)), dtype=first_img.dtype)

        channels_nz = [c for c in channels if c != 0] # Exclude the empty channel (0) from the loop.
        total_iters = len(channels_nz) * len(z_indices) * len(times)

        with tqdm(total=total_iters, desc="Building image...", unit="img", disable=not show_progress) as pbar:
            for channel, zstep, time in product(channels_nz, z_indices, times):
                row = grp[
                    (grp["channel_number"] == channel) &
                    (grp["z-index"] == zstep) &
                    (grp["time"] == time)
                ]
                img = tiff.imread(row["image_paths"].values[0])  # (Y, X)

                final_img[:, :,
                        c_to_idx[row["channel_number"].values[0]],
                        z_to_idx[row["z-index"].values[0]],
                        t_to_idx[row["time"].values[0]]] = img

                pbar.update(1)

        final_img = np.squeeze(final_img)  # Remove singleton dimensions if any
        
        return final_img
    
    def export_images(self, output_dir: str = None, channels: list = None, z_indices: list = None, times: list = None, output_type: str = "tiff"):
        """Reconstruct and export all images as TIFF files in the specified output directory.
        Args:
            output_dir (str): Path to the directory where the TIFF files will be saved. By default, a "tiff_images" directory will be created in the data path.
            channels (list): List of channel numbers to include in the final images. By default, all channels will be included.If 0 is included, it will place an empty image.
            z_indices (list): List of z-index values to include in the final images. By default, all z-index values will be included.
            times (list): List of time points to include in the final images. By default, all time points will be included."""
        self.validate_image_data()
        
        if output_dir is None:
            output_dir = os.path.join(self._data_path, "tiff_images")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if output_type == "tiff":
            photometric = 'minisblack'
        elif output_type == "rgb":
            photometric = 'rgb'
        
        for image_id in tqdm(self._image_data["image_id"].unique(), desc="Exporting images", unit="img"):
            output_name= f"image_{image_id}_{self.get_well_name(image_id)}_s{self.get_site(image_id)}.tif"
            img = self.prepare_multichannel_image(
                image_id,
                channels=channels,
                z_indices=z_indices,
                times=times,
                show_progress=False
            )
            tiff.imwrite(
                os.path.join(output_dir, output_name),
                img,
                compression="lzw",
                photometric=photometric,
                planarconfig="contig"
            )