import pygame
import sys

class Pygame_Gui:
    def __init__(self, image):
        self.Width = 800
        self.Height = 1000

        self.BLACK = (0, 0, 0)

        self.screen = pygame.display.set_mode((self.Width, self.Height))
        pygame.display.set_caption("Image Orderer")
        self.font = pygame.font.Font(None, 20)

        # reset_button_rect = pygame.Rect()
        # start_button_rect = pygame.Rect()

        self.clock = pygame.time.Clock()
        
    def DisplayInput(self):
        pass

    def Run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(self.BLACK)

            print("Hello")

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


