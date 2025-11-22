import numpy as np
from PIL import Image, ImageOps
from pathlib import Path
from .Greedy_Swap import Greedy_Swap

class ColorSorter:
    def __init__(self, target, input, iter):
        self.target = target
        self.input = input 
        self.iter = iter
        self.algorithm = Greedy_Swap(iter)

        self.GenTargetArr()

    def GenTargetArr(self):
        path = Path(__file__).resolve().parent.parent / "targets" / f"{self.target}.jpg"

        image = Image.open(path)
        self.target_arr = self.GenArr(image)

    def GenArr(self, image):
        image_arr = ImageOps.exif_transpose(image).convert("RGB")
        color_arr = np.asarray(image_arr)

        return color_arr

    def GenOutputArr(self):
        self.input_arr = self.GenArr(input)
        self.SortInput() 

    def Sort(self):
        if (self.input_arr.shape != self.target_arr.shape):
            return ValueError
        
        self.algorithm.Solve(self.input_arr, self.target_arr)






