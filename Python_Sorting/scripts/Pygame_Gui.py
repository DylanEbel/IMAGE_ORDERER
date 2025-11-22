import pygame
import sys
import numpy as np
from .Color_Sorter import ColorSorter

class Pygame_Gui:
    def __init__(self, colorSorter: ColorSorter):
        self.Forward = colorSorter.Forward()
        self.colorSorter = colorSorter

        self.Width = 600
        self.Height = 800

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        self.button_color = (180, 180, 180)
        self.hover_color = (120, 120, 120)

        self.screen = pygame.display.set_mode((self.Width, self.Height))
        pygame.display.set_caption("Image Orderer")
        self.font = pygame.font.Font(None, 20)

        self.reset_button_rect = pygame.Rect(150, 700, 100, 30)
        self.start_button_rect = pygame.Rect(350, 700, 100, 30)

        self.clock = pygame.time.Clock()
        
    def DisplayOutput(self):
        arr = np.ascontiguousarray(self.colorSorter.input_arr)
        h, w = arr.shape[:2]
        return pygame.image.frombuffer(arr.tobytes(), (w,h), "RGB")
    
    def Run(self):
        running = True
        solving = False

        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            is_hovered_start = self.start_button_rect.collidepoint(mouse_pos)
            is_hovered_reset = self.reset_button_rect.collidepoint(mouse_pos)

            self.screen.fill(self.BLACK)
            
            pygame.draw.rect(self.screen, self.hover_color if is_hovered_reset else self.button_color, self.reset_button_rect, border_radius=8)
            pygame.draw.rect(self.screen, self.hover_color if is_hovered_start else self.button_color, self.start_button_rect, border_radius=8)

            reset_text = self.font.render("Reset", True, (255, 255, 255))
            reset_surface = reset_text.get_rect(center=self.reset_button_rect.center)
            self.screen.blit(reset_text, reset_surface)

            start_text = self.font.render("Pause" if solving else "Start", True, (255, 255, 255))
            start_surface = reset_text.get_rect(center=self.start_button_rect.center)
            self.screen.blit(start_text, start_surface)

            if is_hovered_reset and mouse_pressed[0]:
                solving = False
                self.colorSorter.Reset()

            if is_hovered_start and mouse_pressed[0]:
                solving = not solving
            
            if solving:
                flips = self.colorSorter.Forward()
                print(flips)

            img_surf = self.DisplayOutput()

            self.screen.blit(img_surf, (75, 50))
            

            pygame.display.flip()

            self.clock.tick(10)

        pygame.quit()
        sys.exit()



