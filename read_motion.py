import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


image_path = 'refBMP/0.bmp'
image = Image.open(image_path)

image_array = np.array(image)

print(f'image_array {image_array.shape} \n {image_array}')
# plt.imshow(image_array)
# plt.axis('off')  # Turn off axis labels
# plt.show()

# grayscale_image = image.convert('L')  # 'L' mode is for grayscale

# # Convert the grayscale image to a NumPy array
# grayscale_array = np.array(grayscale_image)

# plt.imshow(grayscale_array, cmap='gray')
# plt.axis('off')
# plt.show()