# Imageformater

Python package to format high-throughput microscopy images (currently ScanR) into reconstructed multi-channel TIFF files.

## Installation

### 1. Install Conda

Use one of the official installers, e.g.:

- Miniconda: https://www.anaconda.com/docs/getting-started/miniconda/main
- Conda-Forge (Miniforge): https://conda-forge.org/download/

### 2. Create and activate a Conda environment

From a terminal in this project folder:

```bash
conda create -n imageformater python=3.11 -y
conda activate imageformater
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
```

## Usage

### 1. Activate the environment from the directory containing the code

```bash
conda activate imageformater
```

### 2. Run the relevant formater script

For ScanR images:

```bash
python main_scanr.py
```

The script will ask for the path to your ScanR acquisition directory and then export reconstructed TIFF images.

## Programmatic usage example

You may also use the module as part of a larger application.

```python
from HtImageformater import HtImageformater

hif = HtImageformater()
hif.read_ScanR(r"C:\path\to\ScanR_experiment")
hif.export_images(channels=[2, 3])
```

