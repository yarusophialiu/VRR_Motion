Falcor motion velocity is normalized device coordinates
obtain mv from falcor, compute frame velocity, set max = 0.4, min = 0 for training
want diagonal size of display in pixels: 

convert the motion velocity to degrees per second:
m1 = frame velocity * sqrt(1080^2 + 1920^2) / 2
m1 is velocity: pixel per frame
convert to degrees per frame:
m2 = m1 / pixels per degrees of the monitor (standard_fhd 37.8)
m3 = m2 * 166
degrees per second m3

If you use NDC (Normalized Device Coordinates), you need to rescale them to account for the aspect ratio.
NDC is -1, 1, both horizontal and vertical, but display is rectangle
i.e. y' = 9/16 * y





in legacy code, VRR_Motion compute frame velocity using reference video
compute magnitude motion velocity per frame from dat file
magnitude motion velocity: compute sqrt(v1**2 + v2**2) per pixel, average across frame

previous frame velocity saved in folders like refrence/magnitude_motion_per_frame/bedroom/bedroom_path1_seg1_1_velocity_per_frame.txt

data in magnitude_motion_per_frame
start from frame1, frame 0 is not saved in reference videos
reference videos are in C:\Users\15142\Projects\VRR\Data\VRRMP4_Reference\reference_videos

h256_to_mp4 are saved in harddisk D drive