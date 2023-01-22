import pygame
from settings import *
from pygame.math import Vector2
import os
import math

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

class CollisionTile(Tile):
    def __init__(self, pos, surf, groups):
        super().__init__(pos,surf,groups,LAYERS['Level'])
        self.old_rect = self.rect.copy()

class AnimatedTile(Tile):
    def __init__(self,pos,surf,groups):
        super().__init__(pos,surf,groups,LAYERS['Lava'])

        self.frames = []
        for frame in os.listdir('graphics/lava'):
            image = pygame.image.load(os.path.join('graphics/lava', frame)).convert_alpha()
            self.frames.append(image)

        self.frame_index = 0

        self.old_rect = self.rect.copy()
    
    def animate(self,dt):
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[math.floor(self.frame_index)]

    def update(self,dt):
        self.animate(dt)

class MovingPlatform(CollisionTile):
    def __init__(self, pos, surf, groups):
        super().__init__(pos,surf,groups)
        
        # Float based movement
        self.direction = Vector2(0,-1)
        self.speed = 200
        self.pos = Vector2(self.rect.topleft)

    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))