import pygame,sys
from settings import *
from pygame.math import Vector2
from entity import Entity

class Player(Entity):

    def __init__(self, pos, groups, path, collision_sprites, shoot, point):
        super().__init__(pos, path, groups, shoot)

        # collision
        self.collision_sprites = collision_sprites

        # Vertical movement
        self.gravity = 30
        self.jump_speed = 1000
        self.on_floor = False
        self.moving_floor = None

        self.point = point

        self.rect.width = 30

        self.health = 10

    def get_status(self):
        # Idle
        if self.direction.x == 0 and self.on_floor:
            self.status = self.status.split('_')[0] + '_idle'

        # Jump
        if self.direction.y != 0 and not self.on_floor:
            self.status = self.status.split('_')[0] + '_jump'

        # Shoot
        if self.can_shoot == False:
            self.status = self.status.split('_')[0] + '_shoot'

        # Duck
        if self.on_floor and self.duck:
            self.status = self.status.split('_')[0] + '_duck'

    def check_contact(self):
        bottom_rect = pygame.Rect(0,0,self.rect.width, 5)
        bottom_rect.midtop = self.rect.midbottom
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(bottom_rect):
                if self.direction.y > 0:
                    self.on_floor = True
                if hasattr(sprite, 'direction'):
                    self.moving_floor = sprite

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] and self.on_floor:
            self.direction.y = -self.jump_speed

        if keys[pygame.K_DOWN]:
            self.duck = True
        else:
            self.duck = False

        # Shoot
        if keys[pygame.K_SPACE] and self.can_shoot:
            direction = Vector2(1,0) if self.status.split('_')[0] == 'right' else Vector2(-1,0)
            pos = self.rect.center + direction * 40
            y_offset = Vector2(0,-5) if not self.duck else Vector2(0,10)
            self.shoot(pos + y_offset, direction, self)

            # self.bullet_sound.play()

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

        # Trigger if player is jumping
        if self.on_floor and self.direction.y != 0:
            self.on_floor = False

    def move(self, dt):
        if self.duck and self.on_floor:
            self.direction.x  = 0

        # Horizontal Movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')

        # Vertical Movement
        # Gravity
        self.direction.y += self.gravity
        self.pos.y += self.direction.y * dt

        # Glue the player to the platform
        if self.moving_floor and self.moving_floor.direction.y > 0 and self.direction.y > 0:
            self.direction.y = 0
            self.rect.bottom = self.moving_floor.rect.top
            self.pos.y = self.rect.y
            self.on_floor = True

        self.rect.y = round(self.pos.y)
        self.collision('vertical')
        self.moving_floor = None

    def check_death(self):
        if self.health <= 0:
            pygame.quit()
            sys.exit()

    def pickup(self, points):
        direction = Vector2(0,-1)
        pos = self.rect.topright
        self.point(pos, direction,points)

    def finish_game(self):
        pygame.quit()
        sys.exit()

    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.get_status()
        self.move(dt)
        self.check_contact()

        self.animate(dt)
        self.blink()

        # Timer
        self.shoot_timer()
        self.invul_timer()

        # Death
        self.check_death()
