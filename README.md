# ImageFormatter

Python package to format high-throughput microscopy images (currently ScanR) into reconstructed multi-channel TIFF files.

## Installation

### 1. Install Conda (Miniconda or Conda-Forge)

Use one of the official installers:

- Miniconda: https://www.anaconda.com/docs/getting-started/miniconda/main
- Conda-Forge (Miniforge): https://conda-forge.org/download/

### 2. Create and activate a Conda environment

From a terminal in this project folder:

```bash
conda create -n imageformatter python=3.11 -y
conda activate imageformatter
```

### 3. Install dependencies

Option A: install from `requirements.txt`

```bash
pip install -r requirements.txt
```

Option B: install directly with pip

```bash
pip install numpy pandas tifffile tqdm
```

### Alternative: create environment from `environment.yml`

```bash
conda env create -f environment.yml
conda activate imageformatter
```

## Usage

### 1. Activate the environment

```bash
conda activate imageformatter
```

### 2. Run the ScanR formatter script

```bash
python main_scanr.py
```

The script will ask for the path to your ScanR acquisition directory and then export reconstructed TIFF images.

## Programmatic usage example

```python
from HtImageFormatter import HtImageFormatter

hif = HtImageFormatter()
hif.read_ScanR(r"C:\path\to\ScanR_experiment")
hif.export_images(channels=[2, 3])
```

