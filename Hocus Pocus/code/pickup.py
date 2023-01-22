import pygame
from settings import *
from pygame.math import Vector2
import os
import math

class Pickup(pygame.sprite.Sprite):
    def __init__(self, pos, path, groups, points):
        super().__init__(groups)

        # Graphics setup
        self.import_assets(path)
        self.frame_index = 0

        # Image setup        
        self.image = self.animations[0]
        self.rect = self.image.get_rect(midbottom = pos)
        self.z = LAYERS['Level']   
        self.mask = pygame.mask.from_surface(self.image)

        self.points = points 
        
        # Sound
        # self.hit_sound = pygame.mixer.Sound('audio/hit.wav')
        # self.hit_sound.set_volume(.3)
        # self.bullet_sound = pygame.mixer.Sound('audio/bullet.wav')
        # self.bullet_sound.set_volume(.3)


    def animate(self,dt):
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.animations):
            self.frame_index = 0

        self.image = self.animations[math.floor(self.frame_index)]


    def import_assets(self, path):
        self.animations = []
        for image_name in os.listdir(path):
            surf = pygame.image.load(os.path.join(path, image_name)).convert_alpha()
            self.animations.append(surf)



    def update(self, dt):
        
        self.animate(dt)

