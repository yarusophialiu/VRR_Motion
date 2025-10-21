import numpy as np
import math
import matplotlib.pyplot as plt
import cv2
from utils import *
from compute_bmp import *
from generate_MP4 import *
import argparse
import time



# compute velocity for the whole sequence
# find the max across all frames
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
    # scene = args.scene
    # speed = args.speed
    # w = args.width
    # h = args.height
    # scene_name = args.sceneval
    
    scene_name = 'room'
    scene = 'room_path4_seg2'
    speed = 3
    refresh_rate = 166
    w, h = 1920, 1080
    bitrate = 8000

    print(f'scene {scene}, scene_name {scene_name}, speed {speed}')
    print(f'bitrate {bitrate}, refresh_rate {refresh_rate}, w, h {w, h}')


    # scene = 'bistro_path1_seg2_1' # {scene}_{speed}
    # refresh_rate = 166
    # resolution = 1080
    # w, h = 1920, 1080
    # TODO: change path of dat files
    FALCOR_MOTION_PATH = 'C:/Users/15142/new/Falcor/Source/Samples/EncodeDecode/motion'
    output_dir = f'{VRR_MOTION}/motion_vector/{scene_name}'
    os.makedirs(output_dir, exist_ok=True)

    output_file = f'{output_dir}/{scene}_{speed}_velocity_cleaned.txt'
    print(f'output_file \n {output_file}')


    with open(output_file, 'w') as file:
        print(f'\n ===================== sequence {scene}_{speed} =====================')
        # file.write(f'===================== sequence {scene}_{speed} =====================\n')
        max_x_all = -np.inf
        max_y_all = -np.inf
        base_path = f'{FALCOR_MOTION_PATH}/{scene}_{speed}/{bitrate}kbps/fps{refresh_rate}/{refresh_rate}_{h}_{bitrate}'
        # frame_per_fps_video
        frame_limit = frame_per_fps_video(refresh_rate)
        print(f'frame_limit {frame_limit}, {refresh_rate + frame_limit}')

        for i in range(refresh_rate, refresh_rate + frame_limit):
        # for i in range(refresh_rate, refresh_rate + 1):
            # print(f'\n=== i {i} ===')
            filename = f'{base_path}/{i}_{refresh_rate}_{h}_{bitrate}_{speed}.dat'
            data = read_dat_file(filename)
            data_array = np.frombuffer(data, dtype=np.float32)
            # print(f'Frame {i}, shape {data_array.shape} {w * h}')
            print(data_array[:10])
            even = data_array[0::2]
            odd = data_array[1::2]
            even = np.reshape(even, [h, w]) * 0.5 * w
            odd = np.reshape(odd, [h, w]) * 0.5 * h

            max_x = np.abs(even).max()
            max_y = np.abs(odd).max()
            max_x_all = max(max_x_all, max_x)
            max_y_all = max(max_y_all, max_y)
            # print(f'max_x {max_x}, max_x_all {max_x_all}')
            # print(f'max_y {max_y}, max_y_all {max_y_all}')
        # print(f'max_x_all {max_x_all}, max_y_all {max_y_all}')
    #     file.write(f'{max_x_all}\n{max_y_all}\n')
    
    # compute bmp
    max_x, max_y = read_motion_vectors(output_file)
    print(f'max_x, max_y {max_x, max_y}')
    base_path = f'{FALCOR_MOTION_PATH}/{scene}_{speed}/{bitrate}kbps/fps{refresh_rate}/{refresh_rate}_{h}_{bitrate}'
    # print(f'base_path {base_path}')
    generate_bmp(base_path, bitrate, refresh_rate, w, h, scene_name, scene, speed, max_x, max_y)

    # generate mp4
    # mp4_scene_dir = f'{VRR_MOTION}/refMP4/{scene_name}' # for reference
    mp4_scene_dir = f'{VRR_MOTION}/refMP4/{scene_name}/{scene}_{speed}/'
    os.makedirs(mp4_scene_dir, exist_ok=True)

    # for reference
    # refmp4File = make_video(f'{VRR_MOTION}/refBMP/{scene_name}/{scene}_{speed}', "%d.bmp", f"{scene}_{speed}_refOutput_{refresh_rate}_{h}_{bitrate}.mp4", refresh_rate)
    refmp4File = make_video(f'{VRR_MOTION}/refBMP/{scene_name}/{scene}_{speed}', "%d.bmp", f"refOutput_{refresh_rate}_{h}_{bitrate}.mp4", refresh_rate)
    shutil.move(refmp4File, mp4_scene_dir)
    
    # remove dat and bmp file
    remove_dir(f'{FALCOR_MOTION_PATH}/{scene}_{speed}')
    remove_dir(f'{VRR_MOTION}/refBMP/{scene_name}/{scene}_{speed}')

    empty_recycle_bin()
    