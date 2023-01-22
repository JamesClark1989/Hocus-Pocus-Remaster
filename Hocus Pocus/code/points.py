import pygame
from settings import *
from pygame.math import Vector2

class Points(pygame.sprite.Sprite):
    def __init__(self,pos,surf,direction, groups):
        super().__init__(groups)

        self.image = surf
        # Flip image if direction x is negative
        self.rect = self.image.get_rect(center = pos)

        self.z = LAYERS['Level']

        # float based movement
        self.direction = direction
        self.speed = 100
        self.pos = Vector2(self.rect.center)

        self.start_time = pygame.time.get_ticks()  


    def update(self,dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        # 1000 is in milliseconds
        if pygame.time.get_ticks() - self.start_time > 2000:
            self.kill()
