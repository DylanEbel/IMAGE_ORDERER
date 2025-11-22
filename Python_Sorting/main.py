import numpy as np
import pygame
from scripts.Pygame_Gui import Pygame_Gui
from scripts.Color_Sorter import ColorSorter

pygame.init()

TARGET = 1
ITERATIONS = 10000

pygame_Gui = Pygame_Gui(None)
colorSorter = ColorSorter(TARGET, None, ITERATIONS)

pygame_Gui.Run()
