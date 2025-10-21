import os
import matplotlib.pyplot as plt
from utils import find_all_frame_velocities



def find_max_min_from_all_scenes(input_root):
    max_velocity = float('-inf')
    min_velocity = float('inf')
    all_velocties = []
    for scene_folder in os.listdir(input_root):
        subfolder_path = os.path.join(input_root, scene_folder)
        print(f'\n=================== {subfolder_path} ===================')
        if os.path.isdir(subfolder_path):  # Ensure it's a folder
            # Process each txt file in the subfolder
            for filename in os.listdir(subfolder_path):
                print(f'filename {filename}')
                file_path = os.path.join(subfolder_path, filename)
                # print(f'file_path {file_path}')
                with open(file_path, 'r') as file:
                    for line in file:
                        parts = line.strip().split()
                        velocity = float(parts[1])
                        max_velocity = max(max_velocity, velocity)
                        min_velocity = min(min_velocity, velocity)
                print(f'max_velocity, min_velocity {max_velocity, min_velocity}')
    return max_velocity, min_velocity


# Assuming velocities is a list of numerical values
def plot_velocity_distribution(velocities, data_type='Train', SHOW=False, SAVE=False):
    plt.figure(figsize=(8, 5))
    plt.scatter(range(len(velocities)), velocities, alpha=0.6)
    plt.xlabel("Frame Index")
    plt.ylabel("Velocity")
    plt.title(f"{data_type} Data Velocity Distribution Across Frames")
    plt.grid(True)

    if SAVE:
        plt.savefig(f'{data_type}_distribution.png')

    if SHOW:
        plt.show()


# find all velocites, and scatter plot
if __name__ == "__main__":
    train_data_root = "magnitude_motion_per_frame"
    # test_data_root = "reference/test_data/magnitude_motion_per_frame"
    velocities = find_all_frame_velocities(train_data_root) # len(velocities)  149400
    print(f'velocities {len(velocities)}')
    SAVE = False # True
    # x axis are velocity indices, with len 149400
    # plot_velocity_distribution(velocities, data_type='Train', SAVE=SAVE)
    max_velocity, min_velocity = find_max_min_from_all_scenes(train_data_root)
    # max_velocity, min_velocity (0.361342, 0.0)
    print(f'max_velocity, min_velocity {max_velocity, min_velocity}')