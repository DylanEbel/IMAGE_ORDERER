import numpy as np
import random

class Greedy_Swap:
    def __init__(self, iter):
        self.iter = iter

    def Solve(self, input_arr, target_arr):
        self.input_arr = input_arr
        self.target_arr = target_arr

        self.width = len(input_arr[0])
        self.height = len(input_arr)

    def Err(self, input, output):
        return np.sum(np.abs(input - output)) / (255 * 3)

    def SortInput(self):
        for _ in range(self.iter):
            randX_1 = random.randrange(self.width)
            randY_1 = random.randrange(self.height)

            randX_2 = random.randrange(self.width)
            randY_2 = random.randrange(self.height)

            input_pixel_1 = self.input_arr[randY_1, randX_1]
            input_pixel_2 = self.input_arr[randY_2, randX_2]

            target_pixel_1 = self.target_arr[randY_1, randX_1]
            target_pixel_2 = self.target_arr[randY_2, randX_2]

            inital_error = self.Err(input_pixel_1, target_pixel_1) + self.Error(input_pixel_2, target_pixel_2)
            swap_error = self.Err(input_pixel_1, target_pixel_2) + self.Error(input_pixel_2, target_pixel_1)

            if swap_error < inital_error:
                self.input_arr[randY_1, randX_1], self.input_arr[randY_2, randX_2] = input_pixel_2, input_pixel_1