from PIL import Image
from utils import *

# Load the BMP image
image_path_folder = 'bpms_reference'  # Replace with the path to your BMP file



# for i in range(30, 31):
#     image_path = f'{image_path_folder}/{i}.bmp'
#     image = Image.open(image_path)

#     # Ensure the image is in RGB mode
#     if image.mode != 'RGB':
#         image = image.convert('RGB')

#     # Get the size of the image
#     width, height = image.size
#     print(f'width, height {width, height}')

#     # Iterate through each pixel and print its RGB value
#     count = 0
#     for y in range(height):
#         for x in range(width):
#             r, g, b = image.getpixel((x, y))
#             print(f"Pixel at ({x}, {y}): R={r}, G={g}, B={b}")
#             count += 1
#             if count > 20:
#                 break


# empty_recycle_bin()

# frame_limit_per_fps()
frames = frame_per_fps_video(166)
print(f'166, {frames}, {166+frames}')

sqroot = sqrt(0.0002723 **2 + -2.4034351e-05 ** 2)
print(sqroot)

even = np.array([1, 2, 3])
odd = np.array([1, 2, 3])
# frame_velocity = np.sqrt(even**2 + odd**2)
# print(f'frame_velocity {frame_velocity}')
# print(np.average(even))
print(0.06840108335018158 + 0.06839551776647568 + 0.07101016491651535)