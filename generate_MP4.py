import os
import glob
import shutil
import argparse
import subprocess
import numpy as np
from datetime import datetime


def delete_files(directory_path, files_to_delete):
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        # List all files in the directory
        files = os.listdir(directory_path)

        for file_to_delete in files_to_delete:
            file_path = os.path.join(directory_path, file_to_delete)

            # Check if the file exists before attempting to delete
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            else:
                print(f"File not found: {file_path}")
    else:
        print(f"Directory not found: {directory_path}")

def delete_files_range(directory_path, num_to_delete):
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        for i in range(num_to_delete):
            # file_path = os.path.join(directory_path, file_to_delete)
            file_path = str(i) + '.bmp'
            file_to_delete = os.path.join(directory_path, file_path)

            print(f'file path {file_to_delete}')

            # Check if the file exists before attempting to delete
            if os.path.exists(file_to_delete):
                os.remove(file_to_delete)
                print(f"Deleted: {file_to_delete}")
            else:
                print(f"File not found: {file_to_delete}")

        rename_files(directory_path)
    else:
        print(f"Directory not found: {directory_path}")


def rename_files(directory_path):
     # rename files to 1.bmp, 2.bmp...
    file_names = os.listdir(directory_path)
    file_names.sort()  # Sort the file names

    for i, file_name in enumerate(file_names, start=1):
        old_path = os.path.join(directory_path, file_name)
        new_path = os.path.join(directory_path, f"{i}.bmp")
        os.rename(old_path, new_path)
        print(f"Renamed: {old_path} -> {new_path}")


def make_video(directory, input_pattern, output_filename, framerate):
    os.chdir(directory)
    print(f'directory {directory}')
    # ffmpeg -framerate 160 -i %d.bmp -c:v libx264 -crf 5 -r 160 -pix_fmt yuv420p ref_crf5_160_1080.mp4
    # ffmpeg_command = ["ffmpeg", "-framerate", str(framerate), "-i", input_pattern, "-c:v", "libx264", \
    #                   "-crf" "-r", str(framerate), "-pix_fmt", "yuv420p", output_filename]

    ffmpeg_command = [
        "ffmpeg", 
        "-framerate", str(framerate), 
        "-i", input_pattern, 
        "-c:v", "libx265", # "libx264"
        "-crf", "0", 
        "-r", str(framerate), 
        "-pix_fmt", "yuv420p", 
        output_filename
    ]
#  ['ffmpeg', '-framerate', '120', '-i', '%d.bmp', '-c:v', 'libx264', '-r', '120', '-pix_fmt', 'yuv420p', 'decOutput_120_1080_4000.mp4']
    #  use below if bmp files are not 1.bmp, 2.bmp, etc., 
    # ffmpeg_command = ['ffmpeg', -framerate 30 -pattern_type glob -i '*.bmp' -c:v libx264 -r 30 -pix_fmt yuv420p refOutput.mp4]
    # ffmpeg -framerate 120 -i %d.bmp -c:v libx264 -r 120 -pix_fmt yuv420p dec_120_1080.mp4
    # print(f'\n\n\nffmpeg \n {ffmpeg_command}')
    try:
        subprocess.run(ffmpeg_command, check=True)
        print("FFmpeg command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running FFmpeg command: {e}")

    mp4File = os.path.join(directory, output_filename)
    return mp4File



def move_video(parent_dir, file1, file2):
    # create folder based on timestamp
    current_time = datetime.now().strftime("%m%d_%H%M%S")
    folder_name = f"{current_time}"
    new_folder_path = os.path.join(parent_dir, folder_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f"Folder '{folder_name}' created successfully in '{parent_dir}'.")
    else:
        print(f"Folder '{folder_name}' already exists in '{parent_dir}'. Choose a different time format.")
    
    file_name = "details.txt"
    file_path = os.path.join(new_folder_path, file_name)
    with open(file_path, 'w') as file:
        file.write("Frames: Width: Height: bitrate: JOD:")

    try:
        shutil.move(file1, new_folder_path)
        newFile1 = os.path.join(new_folder_path, f"refOutput{bitrate}.mp4")
        shutil.move(file2, new_folder_path)
        newFile2 = os.path.join(new_folder_path, f"decOutput{bitrate}.mp4")
        print(f"Files moved to '{new_folder_path}'.")
        return newFile1, newFile2
    except Exception as e:
        print(f"Error moving file: {e}")


def emptyFolder(folder_path, deleteBMP=False):
    if deleteBMP:
        # Use glob to get a list of all files in the folder
        files_to_delete = glob.glob(os.path.join(folder_path, '*'))

        # Delete each file in the list
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                # print(f"File '{file_path}' deleted successfully.")
            except Exception as e:
                print(f"Error deleting file '{file_path}': {e}")

def runCVVDP(newRefPath, newDecPath):
        print(f'\nnewRefPath {newRefPath}')
        print(f'newDecPath {newDecPath}\n')

        command = f"cvvdp --test {newDecPath} --ref {newRefPath} --display standard_fhd --full-screen-resize bilinear"
        # command = cvvdp --test 'C:/Users/15142/Desktop/test_data/decOutputBMP/2.bmp' --ref 'C:/Users/15142/Desktop/test_data/refbmp/*' --display standard_fhd

# cvvdp --test ref_crf5_30_720.mp4 --ref refOutput_30_720_8000.mp4 --display standard_fhd --full-screen-resize bilinear --temp-resample 
# cvvdp --test ref_crf5_160_1080.mp4 --ref ref_crf1_160_1080.mp4 --display standard_fhd --full-screen-resize bilinear --temp-resample 
# -m dm-preview-exr -o dm-preview

        activate_command = f'conda init && conda activate cvvdp && cd "{CVVDPDIR}" && {command}'

        try:
            subprocess.run(activate_command, check=True, shell=True)
            print("Command executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running the command: {e}")



# if __name__ == "__main__":
#     refOutputDir = 'refBMP'
#     # refOutputDir = f'D:/VRR-frame/{SCENE_NAME}/refOutputBMP'

#     # SCENE_NAME = 'bistropath_one1'
#     current_date = datetime.now().date()
#     print(f'current_date {current_date}')

#     CVVDPDIR = 'C:/Users/15142/Projects/ColorVideoVDP/ColorVideoVDP'
#     input_pattern = "%d.bmp"

#     size = 1080
#     bitrate = 8000
#     framerate = 166
#     scene = "bistro_path1_seg2"
#     speed = 1

#     print(f'scene {scene}, speed {speed}')
#     VRRMP4DIR = f'C:/Users/15142/Projects/VRR/VRRMP4/{current_date}/{scene}_{speed}'
#     os.makedirs(VRRMP4DIR, exist_ok=True)
#     print(f"Processing video with bitrate: {bitrate}, resolution: {size} and framerate {framerate}.\n")


#     # generate reference video
#     GETREFANDDEC = True # True False
#     DARKSETTING = False
#     if GETREFANDDEC:
#         # TODO: change bitrate
#         # crf 5
#         refmp4File = make_video(refOutputDir, input_pattern, f"refOutput_{framerate}_{size}_{bitrate}.mp4", framerate)
#         # shutil.move(refmp4File, 'mp4')
    
#     DELETEBMP = False # True False
#     if DELETEBMP:
#         emptyFolder(refOutputDir, deleteBMP=DELETEBMP)
#         # emptyFolder(decOutputDir, deleteBMP=DELETEBMP)

#     RUNCVVDPBATCH = False # True False
#     if RUNCVVDPBATCH:
#         newRefPath = 'C:/Users/15142/Desktop/VRRMP4/ref1080/refOutput.mp4' # 1080
#         newDecPath = f'C:/Users/15142/Desktop/VRRMP4/dec{size}/decOutput*.mp4' # 

#         runCVVDP(newRefPath, newDecPath)

# # C:/Users/15142/source/repos/Falcor/Falcor/build/Source/PerceptualRendering/EncodeDecode

