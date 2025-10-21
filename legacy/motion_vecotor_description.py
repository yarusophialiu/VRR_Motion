import numpy as np
import torch
import matplotlib.pyplot as plt
import cv2
from utils import *
# from compute_bmp import *
from generate_MP4 import make_video
from PIL import Image



# generate bmp for motino vector
# max_x, max_y are max abs value of motion vector x,y (per pixel) of a sequence
# def generate_bmp(w, h, max_x, max_y):
def generate_bmp(base_path, bitrate, refresh_rate, w, h, scene_name, scene, speed, max_x, max_y):
    output_dir = f'{base_path}/bmp'
    os.makedirs(output_dir, exist_ok=True)
    pixel_precision = max(int(max_x) + 1, int(max_y) + 1)

    frame_limit = frame_per_fps_video(refresh_rate)
    print(f'frame_limit {frame_limit}, {refresh_rate + frame_limit}') # 50， 80
    for i in range(refresh_rate, refresh_rate + frame_limit):
        filename = f'{base_path}/{refresh_rate}_{h}_{bitrate}/{i}_{refresh_rate}_{h}_{bitrate}_{speed}.dat'
        data = read_dat_file(filename)
        data_array = np.frombuffer(data, dtype=np.float32)
        # print(f'data_array from dat \n {data_array.shape}') # (460800,)
        # with open('data_dat_png.py', 'a') as f:
        #     f.write("data_array = " + repr(data_array.tolist()))

        even = data_array[0::2]
        odd = data_array[1::2]

        # # compute frame velocity
        # squared_sum = odd ** 2 + even ** 2
        # sqrt_result = np.sqrt(squared_sum)
        # average = sqrt_result.mean().item()
        # with open('writeout/frame_velocity_dat.txt', 'a') as f:
        #     f.write(f"frame {i} " + str(average) + "\n")

        even = np.reshape(even, [h, w]) * 0.5 * w
        odd = np.reshape(odd, [h, w]) * 0.5 * h

        even = (((even / pixel_precision) + 1) * 0.5) * 255 # even should be in range -1, 1, map to range 0-255
        odd = (((odd / pixel_precision) + 1) * 0.5) * 255
        blue = pixel_precision * np.ones([h, w])

        data = np.stack([blue, odd, even], axis=2).astype('int')
        # print(f'data {data}')
        print(f'i-refresh_rate {i-refresh_rate}')
        # print(f'even {even}')
        # print(f'odd {odd}')

        break

        # plt.imshow(data, cmap=plt.get_cmap('hot'), vmin=0, vmax=255)
        # plt.show()
        # cv2.imwrite(f'{i}.bmp', data)

        # data = np.stack([blue, odd, even], axis=2).astype(np.float32)  # Keep as float32
        # cv2.imwrite(f'{output_dir}/{i-refresh_rate}.bmp', data)



# # compute_frame_velocity.py
# def compute_velocity(patch, max_x, max_y):
#     # max_x, max_y = read_motion_vectors(motion_vector_path)
#     pixel_precision = max(int(max_x) + 1, int(max_y) + 1)

#     h, w = patch.shape[1], patch.shape[2]  # height and width
#     odd_channel_processed = patch[1, :, :].float()  # Convert to float for calculations
#     even_channel_processed = patch[2, :, :].float()
#     # print(odd_channel_processed)

#     even_channel = (((even_channel_processed / 255.0) * 2) - 1) * pixel_precision
#     even_channel = even_channel / (0.5 * w)  # Undo the scaling based on width
#     odd_channel = (((odd_channel_processed / 255.0) * 2) - 1) * pixel_precision
#     odd_channel = odd_channel / (0.5 * h)  # Undo the scaling based on height

#     combined_patch = torch.stack([odd_channel, even_channel], dim=0)
#     print(f'data covered from bmp \n {combined_patch}')
#     with open('data_covered.py', 'a') as f:
#         f.write("data_array = " + repr(combined_patch.tolist()))
#     # squared_sum = odd_channel ** 2 + even_channel ** 2
#     # sqrt_result = torch.sqrt(squared_sum)
#     # average = round(sqrt_result.mean().item(), 3)
#     # return average


def compute_velocity(patch, max_x, max_y):
    # print(f'max_x, max_y {max_x, max_y}')
    pixel_precision = max(int(max_x) + 1, int(max_y) + 1)
    h, w = patch.shape[1], patch.shape[2]  # height and width
    odd_channel_processed = patch[1, :, :].float()  # Convert to float for calculations
    even_channel_processed = patch[2, :, :].float()
    # print(odd_channel_processed)

    even_channel = (((even_channel_processed / 255.0) * 2) - 1) * pixel_precision
    even_channel = even_channel / (0.5 * w)  # Undo the scaling based on width
    odd_channel = (((odd_channel_processed / 255.0) * 2) - 1) * pixel_precision
    odd_channel = odd_channel / (0.5 * h)  # Undo the scaling based on height
    squared_sum = odd_channel ** 2 + even_channel ** 2
    sqrt_result = torch.sqrt(squared_sum)
    average = round(sqrt_result.mean().item(), 3)
    return average


def recover_dat_from_bmp(bmp_image, frame_number, max_x, max_y, h, w):
    pixel_precision = max(int(max_x) + 1, int(max_y) + 1)
    # Extract the three channels (blue, odd, even)
    blue_channel = bmp_image[:, :, 0]  # Blue channel
    odd_channel = bmp_image[:, :, 1]   # Odd channel
    even_channel = bmp_image[:, :, 2]  # Even channel

    # Reverse the operations
    # Undo the range normalization
    odd_channel = ((odd_channel / 255.0) * 2 - 1) * pixel_precision
    even_channel = ((even_channel / 255.0) * 2 - 1) * pixel_precision

    # Undo the scaling
    odd_channel = odd_channel / (0.5 * h)
    even_channel = even_channel / (0.5 * w)

    # Reshape the channels to their original shape
    even_channel = np.reshape(even_channel, [h, w])
    odd_channel = np.reshape(odd_channel, [h, w])

    squared_sum = odd_channel ** 2 + even_channel ** 2
    sqrt_result = np.sqrt(squared_sum)
    average = sqrt_result.mean().item()
    # print(f'average {average}')
    return average

def recover_dat_from_video(bmp_image, frame_number, max_x, max_y, h, w):
    pixel_precision = max(int(max_x) + 1, int(max_y) + 1)
    # Extract the three channels (blue, odd, even)
    even_channel = bmp_image[:, :, 0]  # Blue channel
    odd_channel = bmp_image[:, :, 1]   # Odd channel
    blue_channel = bmp_image[:, :, 2]  # Even channel

    print(f'odd_channel {odd_channel}')
    print(f'even_channel {even_channel}')

    # Reverse the operations
    # Undo the range normalization
    odd_channel = ((odd_channel / 255.0) * 2 - 1) * pixel_precision
    even_channel = ((even_channel / 255.0) * 2 - 1) * pixel_precision

    # Undo the scaling
    odd_channel = odd_channel / (0.5 * h)
    even_channel = even_channel / (0.5 * w)

    # Reshape the channels to their original shape
    even_channel = np.reshape(even_channel, [h, w])
    odd_channel = np.reshape(odd_channel, [h, w])

    squared_sum = odd_channel ** 2 + even_channel ** 2
    sqrt_result = np.sqrt(squared_sum)
    average = sqrt_result.mean().item()
    # print(f'average {average}')
    return average

    # # Stack the odd and even channels to get back the data_array
    # recovered_data_array = np.empty((h * w * 2,), dtype=np.float32)
    # recovered_data_array[0::2] = even_channel.flatten()
    # recovered_data_array[1::2] = odd_channel.flatten()

    # # Now `recovered_data_array` should contain the data as it was before saving to BMP
    # print(f"Recovered data_array shape: {recovered_data_array.shape}")
    # print(f'data_array from dat \n {recovered_data_array.shape}') # (460800,)
    # with open('data_covered_2_png.py', 'a') as f:
    #     f.write("data_array = " + repr(recovered_data_array.tolist()))

def compute_velocity_from_video(video_path, max_x, max_y):
    cap = cv2.VideoCapture(video_path)    
    if not cap.isOpened():
        print("Error opening video file")
        return
    frame_number = 0 # decoded video frame index that will be passed to find_motion_patch_h265
    while cap.isOpened():
        ret, frame = cap.read() # frame (360, 640, 3)
        if not ret: # If frame is read correctly ret is True
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        print(f'frame from video {frame.shape} {frame}') # (360, 640, 3)
        # [[[201 131   2]
        # [140 128   3]]
        # [[201 131   2]
        # [140 128   3]]
        # frame = torch.from_numpy(frame).permute(2, 0, 1) # 3, 360, 640  C,H,W
        # velocity = compute_velocity(frame, max_x, max_y)
        velocity = recover_dat_from_video(frame, frame_number, max_x, max_y, h, w)
        print(f'{frame_number} {velocity}')
        # velocity = recover_dat(frame, frame_number, max_x, max_y, h, w)
        # velocity = recover_dat(frame, frame_number, max_x, max_y, h, w)
        # with open('writeout/frame_velocity_video.txt', 'a') as f:
        #     f.write(f"frame {frame_number + refresh_rate} " + str(velocity) + "\n")

        # write to magnitude_motion_per_frame
        frame_number += 1
        break
        # if frame_number == 10:
        #     break
    # return max_velocity

if __name__ == "__main__":
    # compute bmp
    max_x = 4.620445251464844
    max_y = 0.3601822853088379
    base_path = r'C:\Users\15142\OneDrive - University of Cambridge\Desktop\dat\room_path1_seg1_1\8000kbps\fps30'
    # print(f'base_path {base_path}')
    bitrate = 8000
    h, w = 360, 640
    scene_name, scene, speed = '', '', 1
    refresh_rate = 30
    generate_bmp(base_path, bitrate, refresh_rate, w, h, scene_name, scene, speed, max_x, max_y)

    # # generate mp4
    # mp4_scene_dir = f'{base_path}'
    # os.makedirs(mp4_scene_dir, exist_ok=True)
    # refmp4File = make_video(f'{base_path}/bmp', "%d.bmp", f"refOutput_{refresh_rate}_{h}_{bitrate}.mp4", refresh_rate)
    # shutil.move(refmp4File, mp4_scene_dir)
    
    # video_path = f'{base_path}/refOutput_{refresh_rate}_{h}_{bitrate}.mp4'
    # compute_velocity_from_video(video_path, max_x, max_y)

    # # image = Image.open('3.bmp')
    # # image_array = np.array(image)

    # bmp_image = cv2.imread(f'{base_path}/bmp/0.bmp')
    # # bmp_image = cv2.imread('3.png', cv2.IMREAD_UNCHANGED)
    # # h, w = 360, 640
    # print(f'\nbmp {bmp_image.shape} {bmp_image}')
    # average = recover_dat_from_bmp(bmp_image, 3, max_x, max_y, h, w)
    # print(f'0 {average}')

# # frame = torch.from_numpy(image_array).permute(2, 0, 1) # 3, 360, 640  C,H,W
# # print(f'frame {frame.size()}')
# # # motion_video_path = f'{VRR_Motion}/reference/refMP4_reference/{scene}/{scene}_path{path}_seg{seg}_{speed}_refOutput_166_1080_8000.mp4'
# frame = torch.from_numpy(bmp_image).permute(2, 0, 1) # 3, 360, 640  C,H,W
# print(f'frame {frame.size()}')
# compute_velocity(frame, max_x, max_y)


# dat file 30.dat
# data [[[  5 139 269]
#   [  5 139 268]
#   [  5 139 268]
#   ...
#   [  5 131 156]
#   [  5 131 156]
#   [  5 131 156]]

#  [[  5 139 269]
#   [  5 139 268]
#   [  5 139 268]
#   ...
#   [  5 131 156]
#   [  5 131 156]
#   [  5 131 156]]

#  [[  5 139 269]
#   [  5 139 268]
#   [  5 139 268]

# bmp (360, 640, 3) 
# 0 0.006865139579197219
# [[[  5 139 255]
#   [  5 139 255]
#   [  5 139 255]
#   ...
#   [  5 131 156]
#   [  5 131 156]
#   [  5 131 156]]

#  [[  5 139 255]
#   [  5 139 255]
#   [  5 139 255]


# frame from video (360, 640, 3) 
# 0 0.006624972851036922
# [[[253 139   2]
#   [253 139   2]
#   [253 139   2]
#   ...
#   [153 130   1]
#   [153 130   1]
#   [153 130   1]]

#  [[253 139   2]
#   [253 139   2]
#   [253 139   2]
#   ...
#   [153 130   1]
#   [153 130   1]
#   [153 130   1]]

# even 200, odd 100, blue 5