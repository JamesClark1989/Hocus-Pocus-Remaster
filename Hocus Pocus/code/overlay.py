import pygame
from settings import * 

class Overlay:
    def __init__(self,player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.UI_surf = pygame.image.load('graphics/UI.png').convert_alpha()
        self.health_surf = pygame.image.load('graphics/health_potion_ui.png').convert_alpha()

        # Point font
        self.points = 0
        pygame.font.init()
        self.my_font = pygame.font.Font('font/PressStart2P-Regular.ttf', 22)
        self.set_score(self.points)

        # Key
        self.show_key = False
        self.key_surf = pygame.image.load('graphics/key.png').convert_alpha()

    def display(self):
        UI_offset_y = (WINDOW_HEIGHT - self.UI_surf.get_height())
        self.display_surface.blit(self.UI_surf,(160,UI_offset_y))

        # Blit the health surface as many times as the player has health
        x_offset = 5
        for h in range(self.player.health):
            x = 428 + h * (self.health_surf.get_width() + x_offset)
            y = 665
            self.display_surface.blit(self.health_surf,(x,y))

        # Points
        self.display_surface.blit(self.text_surface, (200,665))

        # Key
        if self.show_key == True:
            self.display_surface.blit(self.key_surf, (810,660))

    def set_score(self, points):
        self.points += points
        self.text_surface = self.my_font.render(str(self.points), False, (255,255,255))

    def got_key(self):
        self.show_key = True