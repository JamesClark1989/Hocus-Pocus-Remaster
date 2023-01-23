import pygame
from settings import *
from pygame.math import Vector2
from entity import Entity
import random

class Dracodile(Entity):
    def __init__(self, pos, groups, path, collision_sprites, shoot, player):
        super().__init__(pos, path, groups, shoot)
        self.player = player
        self.collision_sprites = collision_sprites
        self.gravity = 30
        self.direction.x = 1
        self.speed = 100

        self.rect.width = 30
        self.cooldown = 1000

        self.invul_duration = 200

        # Sound
        self.shoot_sound = pygame.mixer.Sound('audio/shoot_low.mp3')
        self.shoot_sound.set_volume(.3)

    def get_status(self):
        if self.direction.x == -1:
            self.status = 'left'
        else:
            self.status = 'right'

    def check_fire(self):
        enemy_pos = Vector2(self.rect.center)
        player_pos = Vector2(self.player.rect.center)

        distance = (player_pos - enemy_pos).magnitude()
        same_y = True if self.rect.top - 20 < player_pos.y < self.rect.bottom + 20 else False

        if distance < 300 and same_y and self.can_shoot:

            bullet_direction = Vector2(1,0) if self.status == 'right' else Vector2(-1,0)
            y_offset = Vector2(0,-6)
            pos = self.rect.center + bullet_direction * 30
            self.shoot(pos + y_offset, bullet_direction)

            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

            self.shoot_sound.play()

    def collision(self,direction):
        # This literally detects if it's colliding with every sprite in the level
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                
                if direction == "horizontal":
                    # left collision
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction.x = 1

                    # right collision
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction.x = -1

                    self.pos.x = self.rect.x
                else:
                    # down collision
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.on_floor = True

                    # top collision
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    self.pos.y = self.rect.y
                    self.direction.y = 0

    def change_direction(self, direction):
        self.direction.x = self.direction.x * -1

    def move(self, dt):

        # Horizontal Movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')

        # Vertical Movement
        # Gravity
        self.direction.y += self.gravity
        self.pos.y += self.direction.y * dt

        self.rect.y = round(self.pos.y)
        self.collision('vertical')

    def update(self, dt):
        self.get_status()

        self.move(dt)
        
        self.animate(dt)
        self.blink()
        self.invul_timer()
        self.check_death()

        self.shoot_timer()
        self.check_fire()

class ThunderDevil(Entity):
    def __init__(self, pos, groups, path, collision_sprites, shoot, player):
        super().__init__(pos, path, groups, shoot)

        self.player = player
        self.collision_sprites = collision_sprites
        self.direction.x = random.choice([-1,1])
        self.direction.y = random.choice([-1,1])
        self.speed = 100

        self.rect.width = 30
        self.rect.height = 30
        
        
        self.cooldown = 1000

    def get_status(self):
        self.status = 'right'

    def check_fire(self):
        enemy_pos = Vector2(self.rect.center)
        player_pos = Vector2(self.player.rect.center)

        distance = (player_pos - enemy_pos).magnitude()
        same_y = True if self.rect.top - 20 < player_pos.y < self.rect.bottom + 20 else False

        if distance < 600 and same_y and self.can_shoot:

            bullet_direction = Vector2(1,0) if self.status == 'right' else Vector2(-1,0)
            y_offset = Vector2(0,-16)
            pos = self.rect.center + bullet_direction * 70
            self.shoot(pos + y_offset, bullet_direction)

            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def collision(self,direction):
        # This literally detects if it's colliding with every sprite in the level
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                
                if direction == "horizontal":
                    # left collision
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right

                    # right collision
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left

                    self.pos.x = self.rect.x

                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.direction.x = 1

                    # right collision
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.direction.x = -1
                else:
                    # down collision
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top

                    # top collision
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom

                    self.pos.y = self.rect.y

                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.direction.y = -1

                    # top collision
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.direction.y = 1


    def move(self, dt):

        # Horizontal Movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')

        # Vertical Movement
        # Gravity
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)

        self.collision('vertical')

    def update(self, dt):
        self.get_status()

        self.move(dt)
        
        self.animate(dt)
        self.blink()
        
        self.invul_timer()
        self.check_death()

