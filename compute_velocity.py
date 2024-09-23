import numpy as np
import math
import matplotlib.pyplot as plt
import cv2
from utils import *
from compute_bmp import *
from generate_MP4 import *
import argparse
import time
import numpy as np
import math
import cv2
from utils import *


def show_motion(frame_start, frame_end, bitrate, refresh_rate, resolution):
    for i in range(frame_start, frame_end):
        filename = f'{base_path}/{i}_{refresh_rate}_{resolution}_{bitrate}_{speed}.dat'
        data = read_dat_file(filename)
        data_array = np.frombuffer(data, dtype=np.float32)
        print(f'Frame {i}, shape {data_array.shape}')
        print(data_array[:10])


def compute_velocity(data, frame_rate):
    # optimize using python
    velocities = []
    for i in range(0, len(data) - 1, 2):
        t1 = data[i]
        t2 = data[i + 1]
        hypotenuse = math.sqrt(t1 * t1 + t2 * t2)
        velocity = frame_rate * hypotenuse
        # print(f't1, t2, hypotenuse, velocity {t1, t2, hypotenuse, velocity}')

        velocities.append(velocity)
    return velocities


# compute velocity for the whole sequence
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('bitrate', type=int, help='The framerate of the video')
    parser.add_argument('framerate', type=int, help='The framerate of the video')
    parser.add_argument('width', type=int, help='The width of the video')
    parser.add_argument('height', type=int, help='The height of the video')
    parser.add_argument('scene', type=str, help='Scene name')
    parser.add_argument('path', type=str, help='path')
    parser.add_argument('seg', type=str, help='seg')
    parser.add_argument('speed', type=str, help='Speed value')
    args = parser.parse_args()
    bitrate = args.bitrate
    refresh_rate = args.framerate
    scene = args.scene
    path = args.path
    seg = args.seg
    speed = args.speed
    w = args.width
    h = args.height
    
    # scene = 'crytek_sponza'
    # path, seg = 1, 1
    # speed = 2
    # bitrate = 8000
    # refresh_rate = 166
    # w, h = 1920, 1080

    print(f'\n\n\nscene {scene}, path {path}, seg {seg}, speed {speed}')
    print(f'bitrate {bitrate}, refresh_rate {refresh_rate}, w, h {w, h}')

    velocity = 0
    base_path = f'{FALCOR_MOTION_PATH}/{scene}_path{path}_seg{seg}_{speed}/{bitrate}kbps/fps{refresh_rate}/{refresh_rate}_{h}_{bitrate}'

    # loop through every dat file, compute velocity per pixel, sumup and take average
    frame_limit = frame_per_fps_video(refresh_rate)
    count = 0
    for i in range(refresh_rate, refresh_rate + frame_limit + 1): # refresh_rate + frame_limit
    # for i in range(166, 443): # TODO 166, 443
        filename = f'{base_path}/{i}_{refresh_rate}_{h}_{bitrate}_{speed}.dat'
        data = read_dat_file(filename)

        data_array = np.frombuffer(data, dtype=np.float32)
        # print(f'data_array shape {data_array.shape} \n {data_array}\n')

        even = data_array[0::2]
        odd = data_array[1::2]
        frame_velocity = np.sqrt(even**2 + odd**2)
        # print(f'frame_velocity {frame_velocity}')
        frame_velocity = frame_velocity * refresh_rate
        avg_velocity = np.average(frame_velocity)
        velocity += avg_velocity
        # print(f'i {i} avg_velocity {avg_velocity}, velocity {velocity}')
        count += 1

    # print(f'count {count}')
    print(f'frame_limit {frame_limit}, {count} frames processed')
    # velocity /= count
    print(f'velocity {round(velocity, 4)}')
    velocity_output_path = f'{VRR_MOTION}/reference_velocity/{scene}.txt'
    with open(velocity_output_path, "a") as file:
        # TODO: this velocity is sumed up across all frames, NOT average
        file.write(f"{round(velocity, 4)} {scene}_path{path}_seg{seg}_{speed} {refresh_rate}_{h}_{bitrate}\n")

    # remove motion folder
    remove_dir(f'{FALCOR_MOTION_PATH}/{scene}_path{path}_seg{seg}_{speed}')
    empty_recycle_bin()
    