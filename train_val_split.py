import os
import math
import glob
import random
import imageio
import shutil
import secrets
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torchvision.transforms as transforms

from PIL import Image
from utils import *
from collections import Counter
VRRML_DATA = r'C:\Users\15142\Projects\VRR\Data\VRRML\ML'

def create_train_validation_data(train_root):
    # Ensure the validation directory exists
    val_root = f"{VRRML_DATA}/validation-temp"   # Validation data root

    os.makedirs(val_root, exist_ok=True)
    total_files = 0
    total_validation_files = 0
    # Iterate over each subfolder (e.g., "360x30", "480x60", etc.)
    for subfolder in os.listdir(train_root):
        subfolder_path = os.path.join(train_root, subfolder)
        val_subfolder_path = os.path.join(val_root, subfolder)
        print(f'subfolder {subfolder}')
        
        if os.path.isdir(subfolder_path):  # Ensure it's a directory
            os.makedirs(val_subfolder_path, exist_ok=True)  # Create validation subfolder
            
            # Get all files in the subfolder
            files = [f for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))]
            
            # Select 10% of files randomly
            num_val_samples = max(1, int(len(files) * 0.10))  # Ensure at least 1 file is selected
            total_validation_files += num_val_samples
            total_files += len(files)
            val_files = random.sample(files, num_val_samples)
            
            # Move selected files to the validation folder
            for file in val_files:
                # print(f'file {file}')
                shutil.move(os.path.join(subfolder_path, file), os.path.join(val_subfolder_path, file))

    train_dir = os.path.join(train_root, "train")
    os.makedirs(train_dir, exist_ok=True)
    # Loop through all items in the parent directory
    for folder in os.listdir(train_root):
        folder_path = os.path.join(train_root, folder)
        
        # Check if it's a directory and not the "train" folder
        if os.path.isdir(folder_path) and folder != "train":
            # Move the directory into "train"
            shutil.move(folder_path, os.path.join(train_dir, folder))
    shutil.move(val_root, train_root)
    os.rename(f'{train_root}/validation-temp', f'{train_root}/validation')
    print(f'Total data {total_files}, training data {total_files - total_validation_files}, validation data {total_validation_files}')
    print(f"Saved successfully to {train_root}")

dest_path = r'C:\Users\15142\Projects\VRR\Data\VRR_Patches\2025-04-28_patch64x64_labeled_data_test'
# create_train_validation_data(dest_path)

count_data_labels(f'{dest_path}/validation', output_csv_path='', SAVE=False)
