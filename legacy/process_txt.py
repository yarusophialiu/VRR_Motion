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





# SCENES = ['bedroom']
for scene in SCENES:
    with open(f'reference_velocity/{scene}.txt', 'r') as infile:
        with open(f'reference_velocity/{scene}_cleaned.txt', 'w') as outfile:
            # Iterate through each line in the input file
            for line in infile:
                first_value = line.split()[0]
                # Write the extracted value to the output file
                outfile.write(first_value + '\n')
