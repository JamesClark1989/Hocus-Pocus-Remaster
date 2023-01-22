import pygame, sys
from settings import *
from pytmx.util_pygame import load_pygame
from tile import Tile, CollisionTile, MovingPlatform, AnimatedTile
from player import Player
from pygame.math import Vector2
from bullet import Bullet, FireAnimation
from enemy import Enemy,Dracodile
from overlay import Overlay

class AllSprites(pygame.sprite.Group):
    # This class is basically a custom camera
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = Vector2()

        # Sky
        # Import
        
        self.bg_sky = pygame.image.load('graphics/sky/BG_Level_1.png').convert_alpha()
        tmx_map = load_pygame('data/map.tmx')        

        # Dimensions
        self.padding = WINDOW_WIDTH / 2        
        self.sky_width = self.bg_sky.get_width()
        map_width = tmx_map.tilewidth * tmx_map.width + (2 * self.padding)
        self.sky_num = int(map_width // self.sky_width)

    def custom_draw(self,player):

        # Change the offset vector
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        # Blit the bg image and offset
        for x in range(self.sky_num):
            x_pos = -self.padding + (x * self.sky_width)
            self.display_surface.blit(self.bg_sky,(x_pos - self.offset.x / 2.5, 120))

        # blit all sprites
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Contra")
        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.environment_hazard_sprites = pygame.sprite.Group()
        self.vulnerable_sprites = pygame.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.player)

        # Bullet iamges
        self.bullet_surf = pygame.image.load('graphics/bullet.png').convert_alpha()

        # Music
        self.music = pygame.mixer.Sound('audio/music.ogg')
        self.music.play(loops = -1)
        self.music.set_volume(.3)


    def setup(self):
        # Setup level with the map.tmx
        tmx_map = load_pygame('data\map.tmx')
        tile_size = 48

        # Tiles with collision
        for x,y,surf in tmx_map.get_layer_by_name('Level').tiles():
            CollisionTile((x * tile_size,y * tile_size),surf,[self.all_sprites, self.collision_sprites])


        for x,y,surf in tmx_map.get_layer_by_name('Lava').tiles():
            AnimatedTile((x * tile_size,y * tile_size),surf,[self.all_sprites,self.environment_hazard_sprites])

        # Tiles without collision. LAYERS is in settings.py with z depth
        for layer in ['BG Detail']:
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile((x * tile_size,y * tile_size),surf,self.all_sprites, LAYERS[layer])

        # Setup player
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == "Player":
                # Setup Player
                self.player = Player(
                    pos = (obj.x,obj.y), 
                    groups = [self.all_sprites, self.vulnerable_sprites],
                    path = 'graphics\player', 
                    collision_sprites = self.collision_sprites, 
                    shoot = self.shoot)
            if obj.name == "Dracodile":                
                Dracodile(
                    pos = (obj.x,obj.y), 
                    groups = [self.all_sprites, self.vulnerable_sprites], 
                    path = 'graphics\dracodile', 
                    collision_sprites = self.collision_sprites, 
                    shoot = self.shoot, 
                    player = self.player)
        # self.platform_border_rects = []
        # for obj in tmx_map.get_layer_by_name("Platforms"):
        #     if obj.name == "Platform":
        #         MovingPlatform((obj.x,obj.y),obj.image,[self.all_sprites, self.collision_sprites, self.platform_sprites])
        #     else:
        #         border_rect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
        #         self.platform_border_rects.append(border_rect)

    def platform_collisions(self):
        for platform in self.platform_sprites.sprites():
            for border in self.platform_border_rects:
                # Bounce the platforms
                if platform.rect.colliderect(border):
                    if platform.direction.y < 0: # up
                        platform.rect.top = border.bottom
                        platform.pos.y = platform.rect.y
                        platform.direction.y = 1
                    else: # down
                        platform.rect.bottom = border.top
                        platform.pos.y = platform.rect.y
                        platform.direction.y = -1

            if platform.rect.colliderect(self.player.rect) and self.player.rect.centery > platform.rect.centery:
                platform.rect.bottom = self.player.rect.top
                platform.pos.y = platform.rect.y
                platform.direction.y = -1

    def bullet_collisions(self):
        # obstacle collisions
        for obstacle in self.collision_sprites.sprites():
            pygame.sprite.spritecollide(obstacle, self.bullet_sprites, True)

        # Entities
        for sprite in self.vulnerable_sprites.sprites():
            if pygame.sprite.spritecollide(sprite, self.bullet_sprites, True, pygame.sprite.collide_mask):
                sprite.damage()
            if pygame.sprite.spritecollide(sprite, self.environment_hazard_sprites, False, pygame.sprite.collide_mask):
                sprite.damage()
        
    def shoot(self, pos, direction, entity):
        Bullet(pos,self.bullet_surf,direction,[self.all_sprites, self.bullet_sprites])

        FireAnimation(entity, self.fire_surfs, direction, self.all_sprites)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.display_surface.fill((249, 131, 103))

            self.platform_collisions()
            self.all_sprites.update(dt)
            self.bullet_collisions()
            self.all_sprites.custom_draw(self.player)
            self.overlay.display()

            pygame.display.update()

if __name__ == '__main__':
    main = Main()
    main.run()