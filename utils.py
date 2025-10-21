import os
import numpy as np
import pandas as pd
from collections import Counter

VRR_MOTION = r'C:\Users\15142\Projects\VRR\VRR_Motion'



def read_dat_file(filename):
    with open(filename, 'rb') as file:
        data = file.read()
        return data


def find_all_frame_velocities(input_root, output_root=None):
    os.makedirs(output_root, exist_ok=True) if output_root else None
    # Store all velocity values for computing mean and std
    all_velocities = []
    # print(f'os.listdir(input_root) {os.listdir(input_root)}')
    for scene_folder in os.listdir(input_root):
        subfolder_path = os.path.join(input_root, scene_folder)
        print(f'=================== {subfolder_path} ===================')
        if os.path.isdir(subfolder_path):  # Ensure it's a folder
            # Process each txt file in the subfolder
            # First pass: Collect all velocity values
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".txt"):
                    input_file = os.path.join(subfolder_path, filename)
                    with open(input_file, 'r') as infile:
                # print(f'file_path {file_path}')
                        for line in infile:
                            parts = line.strip().split()
                            velocity = float(parts[1])
                            all_velocities.append(velocity)
                    # print(f'all_velocities {len(all_velocities)} \n {all_velocities}')
        #         break
        # break
    return all_velocities



def count_data_labels(training_folder, output_csv_path='', SAVE=False):
    """Usage:
    training_data_name = 'train_single_64x64'
    data_type = 'drop-jod'
    train_or_val = 'train'
    training_folder = f'{VRRML}/ML/frame-velocity/{data_type}-nooutliers/{training_data_name}/{train_or_val}'
    output_csv_path = f'data-label-csv/{data_type}-{training_data_name}_{train_or_val}.csv'
    print(f'output_csv_path {output_csv_path}')
    count_data_labels(training_folder, output_csv_path)
    """
    # Dictionary to store counts
    subfolder_counts = Counter()

    # Loop through each subfolder in the training folder
    for subfolder in os.listdir(training_folder):
        # print(f'subfolder {subfolder}')
        subfolder_path = os.path.join(training_folder, subfolder)
        if os.path.isdir(subfolder_path):  # Ensure it's a directory
            # Count number of images in the subfolder (assuming images are files)
            image_count = len([f for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))])
            subfolder_counts[subfolder] = image_count

    # Convert to DataFrame and sort by count (descending)
    df_subfolder_counts = pd.DataFrame(subfolder_counts.items(), columns=["Subfolder", "Image Count"])
    df_subfolder_counts = df_subfolder_counts.sort_values(by="Image Count", ascending=False)

    total_images = df_subfolder_counts["Image Count"].sum()
    print("Total number of images:", total_images) # 351748
    num_rows = len(df_subfolder_counts)
    num_data_each_label =  int(total_images/num_rows)
    print(f'Number of rows: {num_rows}, num_data_each_label {num_data_each_label}')
    print(f'df_subfolder_counts {df_subfolder_counts}')
    if SAVE:
        df_subfolder_counts.to_csv(output_csv_path, index=False)
    return df_subfolder_counts



