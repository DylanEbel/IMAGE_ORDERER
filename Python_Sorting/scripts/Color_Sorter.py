import numpy as np
from PIL import Image, ImageOps
from pathlib import Path
from .Greedy_Swap import Greedy_Swap

class ColorSorter:
    def __init__(self, target, width, height, input = None):
        self.target = target
        self.width = width
        self.height = height
        self.input = input

        if not input:
            self.GenInputArr()
        else:
            self.input_arr = self.GenArr(input)

        self.GenTargetArr()

        self.algorithm: Greedy_Swap = Greedy_Swap(self.input_arr, self.target_arr)

    def GenTargetArr(self):
        path = Path(__file__).resolve().parent.parent / "targets" / f"{self.target}.jpg"

        image = Image.open(path)
        self.target_arr = self.GenArr(image)

    def GenInputArr(self):
        self.input_arr = self.Random_Arr()

    def Reset(self):      
        if not self.input:
            self.GenInputArr()
        else:
            self.input_arr = self.GenArr(self, self.input)
    
        self.algorithm.input_arr = self.input_arr

    def Random_Arr(self):
        return np.random.randint(0, 256, (self.height, self.width, 3), dtype=np.uint8)

    def GenArr(self, image):
        image_arr = ImageOps.exif_transpose(image).convert("RGB")
        color_arr = np.asarray(image_arr, dtype=np.uint8)

        return color_arr

    def GenOutputArr(self):
        self.input_arr = self.GenArr(input)

    def Forward(self):
        return self.algorithm.Forward()

    def Sort(self):
        if (self.input_arr.shape != self.target_arr.shape):
            return ValueError
        
        self.algorithm.Solve()






