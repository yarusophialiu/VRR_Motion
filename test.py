import math
from utils import *
from math import *
import matplotlib.pyplot as plt

# from compute_bmp import compute_velocity


def compute_velocity(data, frame_rate):
    # optimize using python
    velocities = []
    for i in range(0, len(data) - 1, 2):
        t1 = data[i]
        t2 = data[i + 1]
        hypotenuse = math.sqrt(t1 * t1 + t2 * t2)
        velocity = hypotenuse
        # print(f't1, t2, hypotenuse, velocity {t1, t2, hypotenuse, velocity}')

        velocities.append(velocity)
    return np.array(velocities)

def mapPathToId(path, seg, speed):
    """
    NOTE: output id starts from 0 not 1, HPC job id starts from 1

    mapPathToId(1, 1, 1) -> 0, id is 0, need to add 1 to become jobid
    """
    id = (path-1) * 9 + (seg-1) * 3 + speed - 1
    print(f'id {id}')
    return id



def mapIdToPath(id):
    """
    NOTE: input id starts from 0 not 1, HPC job id starts from 1
    so should be mapIdToPath(JOBID-1)

    we run 45 jobs/tasks (allocate 13 gpus) at one time as each scene has 45 clips
    so we run 10 times as there are in total 10 scenes
    for each task id, we run videos for 1 scene, 1 seg, 1 speed, i.e. for loop 5 * 10 = 50 videos
    e.g. sbatch --array=1-10:1 -A STARS-SL3-GPU submission_script

    id is from 0-44, map id -> path, seg, speed

    e.g. id 0 -> paths[0], segs[0], speeds[0]
         id 1 -> paths[0], segs[0], speeds[1]
    Note that id in HPC starts from 1, so delete id by 1 when call the function
    mapIdToPath(0) -> (1, 1, 1) path1 seg1 speed1
    mapIdToPath(16) -> (2, 3, 2) path2 seg3 speed2
    """
    pathIdx = int(floor(id/9))
    segIdx = int(floor((id - pathIdx * 9) / 3))
    speedIdx = (id - pathIdx * 9) % 3
    paths = [1, 2, 3, 4, 5]
    segs = [1, 2, 3,]
    speeds = [1, 2, 3,]
#    print(f'pathIdx {pathIdx}, segIdx {segIdx} speedIdx {speedIdx}')
    return paths[pathIdx], segs[segIdx], speeds[speedIdx]


if __name__ == "__main__":
    motion_dir = r"C:\Users\15142\new\Falcor\Source\Samples\EncodeDecode\motion\room\room_path4_seg2_3\8000kbps\fps166\166_1080_8000"
    velocities = []
    frame_indices = []
    for i in range(166, 300):
        filename = f'{motion_dir}/{i}_166_1080_8000_3.dat'
        data = read_dat_file(filename)
        data_array = np.frombuffer(data, dtype=np.float32)
        # print(f'data_array {len(data_array)} {1920*1080 * 2}')
        motion = data_array.reshape((1080, 1920, 2))

        speed = np.sqrt(motion[..., 0]**2 + motion[..., 1]**2)

        # Compute average (mean) velocity magnitude across the frame
        frame_v = np.mean(speed)
    #     frame_v = compute_velocity(data_array, 166)
    #     # print(f'frame_v {len(frame_v)}')
    #     frame_v = np.mean(frame_v)
    #     print(f'frame_v {frame_v}')
        velocities.append(frame_v)
        frame_indices.append(i)
    
    frame_indices = np.array(frame_indices)
    plt.figure(figsize=(8, 5))
    plt.plot(frame_indices, velocities, marker='o', linestyle='-', linewidth=1, markersize=3)
    plt.xlabel("Frame Index")
    plt.ylabel("Motion Velocity")
    plt.title(f"Frame velocity using dat file")
    plt.grid(True)
    plt.show()
