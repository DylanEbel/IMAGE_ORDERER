import numpy as np
import pygame
from scripts.Pygame_Gui import Pygame_Gui
from scripts.Color_Sorter import ColorSorter

pygame.init()

TARGET = 1
INPUT = r"cropped_images\cropped_image.png"

colorSorter = ColorSorter(TARGET, 450, 600, INPUT)

pygame_Gui = Pygame_Gui(colorSorter)
# pygame_Gui = Pygame_Gui(colorSorter.input_arr, colorSorter.Forward())

pygame_Gui.Run()
