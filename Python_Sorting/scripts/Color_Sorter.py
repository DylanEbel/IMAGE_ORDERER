import numpy as np
from PIL import Image, ImageOps

class ColorSorter:
    def __init__(self, height, width, target):
        self.height = height
        self.width = width
        self.target_image = ".scripts." + target
        self.target_arr = self.GenColorArray(self.target_image)

    def GenColorArray()


