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

        self.GenInputArr()
        self.GenTargetArr()

        self.output_arr.setflags(write=True)
        self.algorithm: Greedy_Swap = Greedy_Swap(self.output_arr, self.target_arr)

    def GenTargetArr(self):
        path = Path(__file__).resolve().parent.parent / "targets" / f"{self.target}.jpg"

        image = Image.open(path)
        self.target_arr = self.GenArr(image)

    def GenInputArr(self):
        if self.input:
            path = Path(__file__).resolve().parent.parent.parent / self.input

            print(path)

            image = Image.open(path)
            self.input_arr = self.GenArr(image)
            self.output_arr = np.array(self.input_arr, copy=True)
        else:
            self.input_arr = self.RandomArr()
            self.output_arr = np.array(self.input_arr, copy=True)

    def Reset(self):      
        self.output_arr = np.array(self.input_arr, copy=True)
        self.algorithm.input_arr = np.array(self.input_arr, dtype=np.uint8, copy=True, order="C")

    def RandomArr(self):
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






