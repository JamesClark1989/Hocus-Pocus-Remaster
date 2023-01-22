import pygame
from settings import *
from pygame.math import Vector2

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos,surf,direction, groups):
        super().__init__(groups)

        
        self.image = surf
        # Flip image if direction x is negative
        if direction.x < 0:
            self.image = pygame.transform.flip(self.image,True,False)
        self.rect = self.image.get_rect(center = pos)

        self.z = LAYERS['Level']

        # float based movement
        self.direction = direction
        self.speed = 1200
        self.pos = Vector2(self.rect.center)

        self.start_time = pygame.time.get_ticks()
        self.mask = pygame.mask.from_surface(self.image)   

    def update(self,dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        # 1000 is in milliseconds
        if pygame.time.get_ticks() - self.start_time > 1000:
            self.kill()

class FireAnimation(pygame.sprite.Sprite):
    def __init__(self,entity, surf_list, direction, groups):
        super().__init__(groups)

        # Setup
        self.entity = entity
        self.frames = surf_list
        if direction.x < 0:
            # List comprehension to flip all the frames
            self.frames = [pygame.transform.flip(frame,True,False) for frame in self.frames]

        # Image
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # Offset
        x_offset = 60 if direction.x > 0 else -60
        y_offset = 10 if entity.duck else -16
        self.offset = Vector2(x_offset, y_offset)

        # Postion
        self.rect = self.image.get_rect(center = self.entity.rect.center + self.offset)
        self.z = LAYERS['Level']

    def animate(self, dt):
        self.frame_index += 15 * dt
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def move(self):
        self.rect.center = self.entity.rect.center + self.offset

    def update(self,dt):
        
        self.move()
        self.animate(dt)