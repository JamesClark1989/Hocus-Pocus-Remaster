import pygame
from settings import *
from pygame.math import Vector2
from os import walk
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, path, groups, shoot):
        super().__init__(groups)

        # Graphics setup
        self.import_assets(path)
        self.frame_index = 0
        self.status = 'right'

        # Image setup        
        self.image = self.animations[self.status][self.frame_index]

        self.rect = self.image.get_rect(midbottom = pos)
        self.old_rect = self.rect.copy()
        
        self.z = LAYERS['Level']   
        self.mask = pygame.mask.from_surface(self.image)     

        # float based movement
        self.direction = Vector2()
        self.pos = Vector2(self.rect.midbottom)
        self.speed = 500        

        # Shooting setup
        self.shoot = shoot
        self.can_shoot = True
        self.shoot_time = None
        self.cooldown = 200
        self.shoot_up = False

        # Health
        self.health = 3
        self.is_vulnerable = True
        self.hit_time = None
        self.invul_duration = 300

        # Sound
        self.hit_sound = pygame.mixer.Sound('audio/hit.wav')
        self.hit_sound.set_volume(.3)

    def blink(self):
        if not self.is_vulnerable:
            if self.wave_value():
                mask = pygame.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0,0,0))
                self.image = white_surf

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: return True
        else: return False

    def damage(self):
        if self.is_vulnerable:
            self.hit_sound.play()
            self.health -= 1
            self.is_vulnerable = False
            self.hit_time = pygame.time.get_ticks()

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def animate(self,dt):
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)   

    def shoot_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > self.cooldown:
                self.can_shoot = True

    def invul_timer(self):
        if not self.is_vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > self.invul_duration:
                self.is_vulnerable = True

    def import_assets(self, path):
            self.animations = {}
            for index, folder in enumerate(walk(path)):
                if index == 0:
                    for name in folder[1]:
                        print(name)
                        self.animations[name] = []
                
                else:
                    for file_name in sorted(folder[2], key = lambda string: int(string.split(".")[0])):
                        path = folder[0].replace('\\', '/') + '/' + file_name
                        surf = pygame.image.load(path).convert_alpha()
                        key = folder[0].split('\\')[2]
                        #print(key)
                        
                        self.animations[key].append(surf)


            print(self.animations)
