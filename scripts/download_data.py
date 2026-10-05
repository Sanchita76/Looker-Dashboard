"""Download the Kaggle 'E-Commerce Data' (Online Retail) dataset into data/raw.
Kaggle page: https://www.kaggle.com/datasets/carrie1/ecommerce-data  (file: data.csv, ~540k rows)
Needs a Kaggle API token (see README step 2) - or download the ZIP manually and unzip into data/raw.
"""
import os, subprocess, sys

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw")
os.makedirs(RAW, exist_ok=True)
try:
    subprocess.run([sys.executable, "-m", "kaggle", "datasets", "download", "-d", "carrie1/ecommerce-data",
                    "-p", RAW, "--unzip"], check=True)
    print("Downloaded to", os.path.abspath(RAW))
except Exception as e:
    sys.exit(f"\nKaggle download failed ({e}).\nDownload manually from the Kaggle page, unzip data.csv into data/raw, "
             "or run: python scripts/make_demo_data.py")
