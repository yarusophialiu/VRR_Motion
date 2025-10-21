import cv2
import numpy as np
import os
import imageio
from utils import *
from PIL import Image
import matplotlib.pyplot as plt
from utils import *
import datetime
import random
import torch
import torchvision.transforms as transforms


def get_patch(width, height, patch_size, interpolated_img):
    max_x = width - patch_size[1]
    max_y = height - patch_size[0]
    x = np.random.randint(0, max_x + 1)
    y = np.random.randint(0, max_y + 1)
    print(f'x, y {x, y}')

    interpolated_patch = interpolated_img[:, y:y+patch_size[0], x:x+patch_size[1]]
    return interpolated_patch




def find_velocity_h265(base_dir, bitrate, dec_fps, count, dec_frame_number, px, py, patch_size=(64, 64), output_dir="output", scene=None):
    """
    """
    # specs = f'{fps}_{resolution}_{bitrate}'
    # fps_dir = os.path.join(base_dir, f'{bitrate}kbps', f'fps{fps}', specs) # h264 inside the dir
    # files = os.listdir(fps_dir)
    # video_path = os.path.join(fps_dir, files[0])
    # print(f'files {files}')
    video_path = f'refBMP/refOutput_166_1080_8000.mp4'
    # video_path = f'refMP4/refOutput_166_1080_8000_bistro_121_0902.mp4'
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video file")
        return
    
    
    # number = int(filename.split('.')[0])

    frame_ind = int(safe_floor((dec_frame_number-4)/dec_fps * fps) + 2)
    print(f'dec_fps {dec_fps}, fps {fps}')

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_ind)
    ret, frame = cap.read() # frame (360, 640, 3)
    
    # while cap.isOpened(): # Read until video is completed
    # if count + frame_generated >= NUM_PATCH_REQUIRED:
    #     break

    if not ret: # If frame is read correctly ret is True
        print(f"Error: Could not read frame {frame_ind}")
        return None

    frame = torch.from_numpy(frame).permute(2, 0, 1) # 3, 360, 640
    # show_patch(frame.permute(1,2,0)) # after permute 360, 640, 3
    print(f'frame {frame.permute(1,2,0).size()} \n {frame.permute(1,2,0)}')
    # patch = get_patch(width, height, patch_size, frame)
    patch = frame[:, py:py+patch_size[0], px:px+patch_size[1]]
    print(f'patch {patch.size()} \n {patch.permute(1,2,0)}')
    # show_patch(patch.permute(1,2,0))

        #     # hex_unique_id = secrets.token_hex(4)
        #     # # path = f'{output_folder}/{hex_unique_id}_{frame_index}_{fps}_{resolution}_{bitrate}.png'
        #     # # path = f'{output_dir}/{hex_unique_id}_{fps}_{resolution}_{bitrate}.png'
        #     # # if scene:
        #     # #     path = f'{output_png_dir}/{hex_unique_id}_{fps}_{resolution}_{bitrate}_x{scene}.png'
        #     # # else:


        #     # path = f'{output_png_dir}/{hex_unique_id}_{fps}_{resolution}_{bitrate}.png'
        #     if False: # SAVE
        #         to_pil = transforms.ToPILImage()
        #         interpolated_patch = to_pil(interpolated_patch)
        #         interpolated_patch.save(path, "png")
        #     # count += 1
        #     frame_generated += 1


if __name__ == "__main__":
    base_path = f'C:/Users/15142/new/Falcor/Source/Samples/EncodeDecode/encodedH264/data'
    # scene_arr = ['bistro_glasses2', 'bistropath_one1', ]
    scene_arr = ['bistropath_one1', 'bistropath_one2', 'bistropath_three1', 'bistropath_three2', 'bistro_glasses2', \
                 'breakfast_room_two1', 'lost_empire_three1',  'sponza_three1', \
                  'paint2', 'room1', 'room2', \
                  'suntemple1', 'suntemple2', 
                #   'suntemple_statue2'
                  ]
    scene_arr = ["bistro"]
    bitrate = 8000
    fps_arr = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120,]
    fps = 166
    SAVE = True

    for scene in scene_arr:
        print(f'====================== scene {scene} ======================')

        base_directory = f'{base_path}/{scene}'
        current_date = datetime.date.today()
        output_folder = f'C:/Users/15142/Desktop/VRR/VRR_Patches/{current_date}/{scene}'
        # os.makedirs(output_folder, exist_ok=True)

        total = 0
        # # NUM_PATCH_REQUIRED = 120 * len(fps_arr) * len(bitrates) # 665
        # # for each fps, 120 * len(resolution_arr) patches 
        # NUM_PATCH_REQUIRED = 120 * len(resolution_arr) 

        # print(f'NUM_PATCH_REQUIRED {NUM_PATCH_REQUIRED}')


        print(f'====================== bitrate {bitrate} ======================')
        print(f'====================== fps {fps} ======================')

        rounds = int(120/fps) # make sure different fps has same number of patches
        # print(f'rounds {rounds}')
        count = 0 # count total number of patches generated for the fps
        find_velocity_h265(base_directory, bitrate, fps, \
                                                count, 0, 0, 0, output_dir=output_folder, scene=scene)
                        



        #                 # total += count
        #         # print(f'for loop {count} for {len(resolution_arr)} resolution')
        #         # for resolution in [360, 480, 720, 864, 1080]:
        #         # print(f'=================== while loop ===================')
        #         while True:
        #             if count >= NUM_PATCH_REQUIRED:
        #                     break
                    
        #             random_resolution = random.choice(resolution_arr)
        #             # print(f'random resolution {random_resolution}')
        #             # for resolution in resolution_arr:
        #             count += find_velocity_h265(base_directory, bitrate, fps, random_resolution, \
        #                                             count, output_dir=output_folder)
        #             # print(f'after resolution {resolution}, count {count}')
        #         total += count
        #         # print(f'{count} data generated for fps {fps}')
        # print(f'{total} data generated for {len(bitrates)} bitrates, {len(fps_arr)} fps and {len(resolution_arr)} resolutions.')



        # # generate_patches(video_path, output_folder)
