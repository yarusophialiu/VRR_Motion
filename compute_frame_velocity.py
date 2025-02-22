import cv2
import torch
from utils import *
from extract_patch_h264_scene_8000 import compute_velocity



def find_motion_h265(video_path, motion_vector_path, output_file, max_velocity):
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
        # print(f'frame {frame.shape} {frame}')
        # [[[201 131   2]
        # [140 128   3]]
        # [[201 131   2]
        # [140 128   3]]
        # print(f'frame {frame.shape} {frame}')
        # frame (1080, 1920, 3) [[[201 131   2]
        # [201 131   2]
        # [201 131   2]
        # ...
        # [140 128   3]
        # [140 128   3]
        # [140 128   3]]

        frame = torch.from_numpy(frame).permute(2, 0, 1) # 3, 360, 640  C,H,W
        velocity = compute_velocity(frame, motion_vector_path)
        # print(f'max_velocity {max_velocity}')
        max_velocity = max(max_velocity, velocity)
        # print(f'velocity {velocity}') # 0.005
        if WRITE:
            with open(output_file, 'a') as f:
                f.write(f'{frame_number} {velocity}\n')

        # write to magnitude_motion_per_frame
        frame_number += 1
        if frame_number == 1:
            break
    return max_velocity

# compute frame velocity: magnitude velocity per pixel, average across the frame
# magnitude velocity per pixel = sqrt(v1**2 + v2**2)
if __name__ == "__main__":
    scenes = [
            # 'bedroom', 'bistro', 
            #  'gallery', 
            #  'living_room', 
            #  'lost_empire', 
            'room', 
            #  'suntemple', 'suntemple_statue'
             ]
    # scenes = ['bedroom', 'bistro', 'crytek_sponza', 'gallery', 'living_room', 'lost_empire', 'room', 'sibenik', 'suntemple', 'suntemple_statue']
    WRITE = False
    max_velocity = -np.inf
    fps = 166
    resolution = 1080
    for scene in scenes:
        print(f'============ scene {scene} ============')
        output_folder = f'reference/magnitude_motion_per_frame/{scene}'
        os.makedirs(output_folder, exist_ok=True)
        for id in range(1, 2): # 46
            id -= 1
            path, seg, speed = mapIdToPath(id)
            print(f'path, seg, speed {path, seg, speed}')

            # save max vector[0], vecotor[1] across frame
            motion_vector_path = f'{VRR_Motion}/reference/motion_vector_reference/{scene}/{scene}_path{path}_seg{seg}_{speed}_velocity_cleaned.txt'
            motion_video_path = f'{VRR_Motion}/reference/refMP4_reference/{scene}/{scene}_path{path}_seg{seg}_{speed}_refOutput_166_1080_8000.mp4'

            output_file = f'{output_folder}/{scene}_path{path}_seg{seg}_{speed}_velocity_per_frame.txt'
            max_velocity = find_motion_h265(motion_video_path, motion_vector_path, output_file, max_velocity)


    print(f'max_velocity {max_velocity}') # max_velocity 1730880.5






