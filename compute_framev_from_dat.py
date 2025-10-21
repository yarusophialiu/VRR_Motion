import os
import math
import numpy as np
import matplotlib.pyplot as plt
import cv2
from utils import *
# from compute_bmp import *
# from generate_MP4 import *
import argparse
import time
from glob import glob



# compute magnitude motion velocity per frame 
# from dat file in falcor
if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('bitrate', type=int, help='The framerate of the video')
    # parser.add_argument('framerate', type=int, help='The framerate of the video')
    # parser.add_argument('width', type=int, help='The width of the video')
    # parser.add_argument('height', type=int, help='The height of the video')
    # parser.add_argument('scene', type=str, help='Scene name')
    # parser.add_argument('speed', type=str, help='Speed value')
    # parser.add_argument('sceneval', type=str, help='Speed value')
    # args = parser.parse_args()
    # bitrate = args.bitrate
    # refresh_rate = args.framerate
    # scene_seg_path = args.scene
    # speed = args.speed
    # w = args.width
    # h = args.height
    # scene_name = args.sceneval

    scene_name = 'room'
    scene_seg_path = 'room_path4_seg2_3' # {scene}_{speed}
    speed = 3
    bitrate = 8000
    refresh_rate = 166
    h = 1080
    # w, h = 1920, 1080

    FALCOR_MOTION_PATH = 'C:/Users/15142/new/Falcor/Source/Samples/EncodeDecode/motion'
    output_dir = f'{VRR_MOTION}/magnitude_motion_per_frame/{scene_name}'
    os.makedirs(output_dir, exist_ok=True)
    output_file = f'{output_dir}/{scene_seg_path}_velocity_per_frame.txt'# saved in magnitude_motion_per_frame
    print(f'output_file {output_file}')
    
    with open(output_file, 'w') as file:
        print(f'\n ===================== sequence {scene_seg_path} =====================')
        base_path = f'{FALCOR_MOTION_PATH}/{scene_name}/{scene_seg_path}/{bitrate}kbps/fps{refresh_rate}/{refresh_rate}_{h}_{bitrate}'
        dat_files = glob(os.path.join(base_path, '*.dat'))
        print(f'There are {len(dat_files)} in {scene_seg_path}')

        # for i in range(1, len(dat_files) + 1): # TODO replace 333
        count = 0
        for i in range(166, len(dat_files) + 1): # TODO replace 333
            # print(f'\n=== i {i} ===')
            filename = f'{base_path}/{i}_{refresh_rate}_{h}_{bitrate}_{speed}.dat'
            data = read_dat_file(filename)
            data_array = np.frombuffer(data, dtype=np.float32)
            print(f'Frame {i}, shape {data_array.shape}')
            print(data_array)
            count += 1

            if count >= 2:
                break