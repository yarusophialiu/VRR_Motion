import numpy as np
import math
# import matplotlib.pyplot as plt
import cv2
from utils import *


def show_motion(frame_start, frame_end, refresh_rate, resolution):
    for i in range(frame_start, frame_end):
        filename = f'{base_path}/{i}_{refresh_rate}_{resolution}_8000_{speed}.dat'
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



def generate_bmp(base_path, bitrate, refresh_rate, w, h, scene_name, scene, speed, max_x, max_y):
    output_dir = f'{VRR_MOTION}/refBMP/{scene_name}/{scene}_{speed}'
    os.makedirs(output_dir, exist_ok=True)
    
    pixel_precision = max(int(max_x) + 1, int(max_y) + 1)
    print(f'pixel_precision {pixel_precision}')

    frame_limit = frame_per_fps_video(refresh_rate)
    # print(f'frame_limit {frame_limit}, {refresh_rate + frame_limit}')
    for i in range(refresh_rate, refresh_rate + frame_limit):
    # for i in range(refresh_rate+ frame_limit-2, refresh_rate + frame_limit):
    # for i in range(166, 167): # TODO 166, 443
        filename = f'{base_path}/{i}_{refresh_rate}_{h}_{bitrate}_{speed}.dat'
        data = read_dat_file(filename)
        data_array = np.frombuffer(data, dtype=np.float32)

        even = data_array[0::2]
        odd = data_array[1::2]

        even = np.reshape(even, [h, w]) * 0.5 * w
        odd = np.reshape(odd, [h, w]) * 0.5 * h

        even = (((even / pixel_precision) + 1) * 0.5) * 255
        odd = (((odd / pixel_precision) + 1) * 0.5) * 255
        blue = pixel_precision * np.ones([h, w])

        # print(f'\neven {even}')
        # print(f'odd {odd}')
        # print(f'blue {blue}')

        data = np.stack([blue, odd, even], axis=2).astype('int')
        # print(f'data {data.shape} \n {data}')

        # # plt.imshow(data, cmap=plt.get_cmap('hot'), vmin=0, vmax=255)
        # # plt.show()
        cv2.imwrite(f'{output_dir}/{i-refresh_rate}.bmp', data)



# # compute velocity for the whole sequence
# if __name__ == "__main__":
#     # Example usage
#     scene = 'bistro'
#     refresh_rate = 166
#     resolution = 1080
#     w, h = 1920, 1080
#     # TODO: change path of dat files
#     FALCOR_MOTION_PATH = 'C:/Users/15142/new/Falcor/Source/Samples/EncodeDecode/motion'
#     # output_file = f'velocity_sequence/{scene}_velocity_cleaned.txt'
#     # with open(output_file, 'w') as file:
#     # for path in range(1, 2):
#     #     for seg in range(1, 3):
#     #         for speed in range(2, 2):
#     path, seg, speed = 1, 1, 1
#     print(f'path {path}')

#     print(f'\n ===================== sequence {scene}_path{path}_seg{seg}_{speed} =====================')
#     # file.write(f'===================== sequence {scene}_path{path}_seg{seg}_{speed} =====================\n')

#     base_path = f'{FALCOR_MOTION_PATH}/{scene}_path{path}_seg{seg}_{speed}/8000kbps/fps{refresh_rate}/{refresh_rate}_{resolution}_8000'
#     # base_path = r'C:\Users\15142\new\Falcor\Source\Samples\EncodeDecode\motion\suntemple_path4_seg1_1\8000kbps\fps{refresh_rate}\{refresh_rate}_{resolution}_8000'
#     # show motion vector of first 4 frames
#     # 4147200 = 1920 x 1080 x 2, each pixel has 2 floats
#     # 460800 = 640 x 360 x 2
#     # data logged from falcor: count fCount 79, t1 0.0507232, t2 0.0462358
#     # show_motion(78, 81, refresh_rate, resolution)
#     sequence_velocity = 0 
#     count = 0
#     # max_x = round(12.71778678894043, 5) # TODO 2.5466396808624268, 2.2427003383636475
#     # max_y = round(5.837514400482178, 5)
#     max_x, max_y = read_motion_vectors(f'{VRR_MOTION}/motion_vector/{scene}/{scene}_path{path}_seg{seg}_{speed}_velocity_cleaned.txt')
#     print(f'max_x, max_y {max_x, max_y}')
#     pixel_precision = max(int(max_x) + 1, int(max_y) + 1)
#     print(f'pixel_precision {pixel_precision}')
#     for i in range(166, 167): # TODO 166, 443
#         filename = f'{base_path}/{i}_{refresh_rate}_{resolution}_8000_{speed}.dat'
#         data = read_dat_file(filename)
#         data_array = np.frombuffer(data, dtype=np.float32)
#         # print(f'Frame {i}, shape {data_array.shape} {360 * 640}')
#         print(data_array[:10])
#         even = data_array[0::2]
#         odd = data_array[1::2]

#         even = np.reshape(even, [h, w])
#         odd = np.reshape(odd, [h, w])
#         blue = pixel_precision * np.ones([h, w])
#         data_original = np.stack([blue, odd, even], axis=2).astype('int')
#         print(f'data_original {data_original.shape} \n {data_original}')


#         even = np.reshape(even, [h, w]) * 0.5 * w
#         odd = np.reshape(odd, [h, w]) * 0.5 * h
        
#         pixel_precision = max(int(max_x) + 1, int(max_y) + 1)
#         # print(f'pixel_precision {pixel_precision}')


#         even = (((even / pixel_precision) + 1) * 0.5) * 255
#         odd = (((odd / pixel_precision) + 1) * 0.5) * 255
#         blue = pixel_precision * np.ones([h, w])

#         # print(pixel_precision)
#         print(f'even \n {even}')
#         print(f'odd \n {odd}')
#         data = np.stack([blue, odd, even], axis=2).astype('int')
#         print(f'data {data.shape} \n {data}')

#         # plt.imshow(data, cmap=plt.get_cmap('hot'), vmin=0, vmax=255)
#         # plt.show()
#         # cv2.imwrite(f'refBMP/{i-166}.bmp', data)
        

#         # velocities = compute_velocity(data_array, refresh_rate)
#         # print(velocities)
#         # # total_sum = round(sum(velocities), 4)
#         # total_sum = sum(velocities)
#         # avg = total_sum / (360 * 640)
#         # sequence_velocity += avg
#         # print(f'i {i}, total_sum {total_sum}, avg {avg}')
#     # print(f'sequence_velocity {round(sequence_velocity, 4)}')
#     # # print(f'{round(sequence_velocity, 4)}')
#     # file.write(f'{round(sequence_velocity, 4)}\n')



