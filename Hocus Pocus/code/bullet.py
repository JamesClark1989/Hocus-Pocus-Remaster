import pygame
from settings import *
from pygame.math import Vector2

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos,surf,direction, groups, speed):
        super().__init__(groups)

        self.image = surf
        # Flip image if direction x is negative
        if direction.x < 0:
            self.image = pygame.transform.flip(self.image,True,False)
        self.rect = self.image.get_rect(center = pos)

        self.z = LAYERS['Level']

        # float based movement
        self.direction = direction
        self.speed = speed
        self.pos = Vector2(self.rect.center)

        self.start_time = pygame.time.get_ticks()
        self.mask = pygame.mask.from_surface(self.image)   

    def update(self,dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        # 1000 is in milliseconds
        if pygame.time.get_ticks() - self.start_time > 1000:
            self.kill()
