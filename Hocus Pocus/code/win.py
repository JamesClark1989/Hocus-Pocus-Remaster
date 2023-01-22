import pygame
from settings import * 

class WinScreen:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.win_screen = pygame.image.load('graphics/Win_Screen.png').convert_alpha()
        

    def display(self):
        self.display_surface.blit(self.win_screen,(0,0))


