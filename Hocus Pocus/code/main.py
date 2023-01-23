import pygame, sys
from settings import *
from pytmx.util_pygame import load_pygame
from tile import Tile, CollisionTile, AnimatedTile
from player import Player
from pygame.math import Vector2
from bullet import Bullet
from enemy import Dracodile,ThunderDevil
from pickup import Pickup
from overlay import Overlay
from points import Points
from win import WinScreen

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
            self.display_surface.blit(self.bg_sky,(x_pos - self.offset.x / 2.5, 0))

        # blit all sprites
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Hocus Pocus")
        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.player_bullet_sprites = pygame.sprite.Group()
        self.enemy_bullet_sprites = pygame.sprite.Group()
        self.walking_enemy_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.environment_hazard_sprites = pygame.sprite.Group()
        self.vulnerable_enemy_sprites = pygame.sprite.Group()
        self.vulnerable_player_sprite = pygame.sprite.Group()
        self.gem_sprites = pygame.sprite.Group()
        self.chalice_sprites = pygame.sprite.Group()
        self.crown_sprites = pygame.sprite.Group()
        self.end_of_level_sprites = pygame.sprite.Group()
        self.health_pickups = pygame.sprite.Group()
        self.key_wall_sprites = pygame.sprite.Group()
        self.key_sprites = pygame.sprite.Group()

        self.won_game = False
        self.has_key = False

        self.setup()
        self.overlay = Overlay(self.player)
        self.win_screen = WinScreen()

        # Bullet images
        self.bullet_surf = pygame.image.load('graphics/fire/bullet.png').convert_alpha()
        self.bullet_up_surf = pygame.image.load('graphics/fire_up/fire_up.png').convert_alpha()
        self.enemy_bullet_surf = pygame.image.load('graphics/enemy_fire/enemy_fire.png').convert_alpha()

        # Points images
        self.five_hundred_points = pygame.image.load('graphics/points/500.png').convert_alpha()
        self.one_thousand_points = pygame.image.load('graphics/points/1000.png').convert_alpha()
        self.five_thousand_points = pygame.image.load('graphics/points/5000.png').convert_alpha()

        # Music
        self.music = pygame.mixer.Sound('audio/music.ogg')
        self.music.play(loops = -1)
        self.music.set_volume(.4)

        self.win_music = pygame.mixer.Sound('audio/win_music.ogg')
        self.win_music.set_volume(.4)
        

        # Misc
        self.player_start_pos = None


    def setup(self):
        # Setup level with the map.tmx
        tmx_map = load_pygame('data\map.tmx')
        tile_size = 48
        
        self.platform_border_rects = []
        for obj in tmx_map.get_layer_by_name("Enemy Blockers"):
            if obj.name == "Blocker":
                border_rect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
                self.platform_border_rects.append(border_rect)

        # Tiles with collision
        for x,y,surf in tmx_map.get_layer_by_name('Level').tiles():
            CollisionTile((x * tile_size,y * tile_size),surf,[self.all_sprites, self.collision_sprites])

        for x,y,surf in tmx_map.get_layer_by_name('Lava').tiles():
            AnimatedTile((x * tile_size,y * tile_size),surf,[self.all_sprites,self.environment_hazard_sprites])

        # Key walls
        for x,y,surf in tmx_map.get_layer_by_name('Key Wall').tiles():
            CollisionTile((x * tile_size,y * tile_size),surf,[self.all_sprites, self.collision_sprites, self.key_wall_sprites])

        # Tiles without collision. LAYERS is in settings.py with z depth
        for layer in ['BG Detail']:
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile((x * tile_size,y * tile_size),surf,self.all_sprites, LAYERS[layer])

        # Setup player
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == "Player":
                self.player_start_pos = (obj.x,obj.y)
                # Setup Player
                self.player = Player(
                    pos = self.player_start_pos, 
                    groups = [self.all_sprites, self.vulnerable_player_sprite],
                    path = 'graphics\player', 
                    collision_sprites = self.collision_sprites, 
                    shoot = self.player_shoot,
                    point = self.get_points)
            if obj.name == "Dracodile":                
                Dracodile(
                    pos = (obj.x,obj.y), 
                    groups = [self.all_sprites, self.vulnerable_enemy_sprites, self.walking_enemy_sprites], 
                    path = 'graphics\dracodile', 
                    collision_sprites = self.collision_sprites, 
                    shoot = self.enemy_shoot, 
                    player = self.player)
            if obj.name == "Thunder_Devil":
                ThunderDevil(
                    pos = (obj.x,obj.y), 
                    groups = [self.all_sprites, self.vulnerable_enemy_sprites], 
                    path = 'graphics\devil', 
                    collision_sprites = self.collision_sprites, 
                    shoot = self.enemy_shoot, 
                    player = self.player)

            if obj.name == "Red_Gem":
                Pickup(
                    pos = (obj.x,obj.y), 
                    groups = [self.all_sprites, self.gem_sprites], 
                    path = 'graphics\pickups\\red_gem',
                    points = 500)
            
            if obj.name == "Chalice":
                Pickup(
                    pos = (obj.x,obj.y), 
                    groups = [self.all_sprites, self.chalice_sprites], 
                    path = 'graphics\pickups\chalice',
                    points = 1000)

            if obj.name == "Crown":
                Pickup(
                    pos = (obj.x,obj.y), 
                    groups = [self.all_sprites, self.crown_sprites], 
                    path = 'graphics\pickups\crown',
                    points = 5000)

            if obj.name == "Key":
                Pickup(
                    pos = (obj.x,obj.y), 
                    groups = [self.all_sprites, self.key_sprites], 
                    path = 'graphics\pickups\key',
                    points = 5000)

            if obj.name == "Finish_Gem":
                Pickup(
                    pos = (obj.x,obj.y), 
                    groups = [self.all_sprites, self.end_of_level_sprites], 
                    path = 'graphics\pickups\\finish_gem',
                    points = 5000)

            if obj.name == "Health_Potion":
                Pickup(
                    pos = (obj.x,obj.y), 
                    groups = [self.all_sprites, self.health_pickups], 
                    path = 'graphics\pickups\health_potion',
                    points = 0)



    def platform_collisions(self):
        for walking_enemy in self.walking_enemy_sprites.sprites():
            for border in self.platform_border_rects:
                # Bounce the Enemies
                if walking_enemy.rect.colliderect(border):
                    walking_enemy.change_direction(-1)
                    if walking_enemy.direction.x == 1: # up
                        walking_enemy.direction.x == -1
                    else: # down
                        walking_enemy.direction.x == 1

    def bullet_collisions(self):
        # obstacle collisions
        for obstacle in self.collision_sprites.sprites():
            pygame.sprite.spritecollide(obstacle, self.bullet_sprites, True)

        # Player collision handler
        for sprite in self.vulnerable_player_sprite.sprites():
            if pygame.sprite.spritecollide(sprite, self.enemy_bullet_sprites, True, pygame.sprite.collide_mask):
                sprite.damage()

            if pygame.sprite.spritecollide(sprite, self.environment_hazard_sprites, False, pygame.sprite.collide_mask):
                sprite.damage()

            if pygame.sprite.spritecollide(sprite, self.vulnerable_enemy_sprites, False, pygame.sprite.collide_mask):
                sprite.damage()

            if pygame.sprite.spritecollide(sprite, self.gem_sprites, True, pygame.sprite.collide_mask):
                sprite.pickup(500)
                self.overlay.set_score(500)

            if pygame.sprite.spritecollide(sprite, self.chalice_sprites, True, pygame.sprite.collide_mask):
                sprite.pickup(1000)
                self.overlay.set_score(1000)

            if pygame.sprite.spritecollide(sprite, self.crown_sprites, True, pygame.sprite.collide_mask):
                sprite.pickup(5000)
                self.overlay.set_score(5000)   

            if pygame.sprite.spritecollide(sprite, self.key_sprites, True, pygame.sprite.collide_mask):
                sprite.pickup(5000)
                self.overlay.set_score(5000)  
                self.overlay.got_key()
                self.has_key = True 

            if pygame.sprite.spritecollide(sprite, self.key_wall_sprites, False, pygame.sprite.collide_mask):
                if self.has_key:
                    for wall in self.key_wall_sprites:
                        wall.kill()
            
            if pygame.sprite.spritecollide(sprite, self.health_pickups, False, pygame.sprite.collide_mask):
                if sprite.health_pickup() == True:
                    pygame.sprite.spritecollide(sprite, self.health_pickups, True, pygame.sprite.collide_mask)

            if pygame.sprite.spritecollide(sprite, self.end_of_level_sprites, True, pygame.sprite.collide_mask):

                self.music.stop()
                self.win_music.play()
                self.won_game = True

        # Enemy collisions
        for sprite in self.vulnerable_enemy_sprites.sprites():
            if pygame.sprite.spritecollide(sprite, self.player_bullet_sprites, True, pygame.sprite.collide_mask):
                sprite.damage()

        
    def player_shoot(self, pos, direction, shooting_up):
        
        if not shooting_up:
            Bullet(pos,self.bullet_surf,direction,[self.all_sprites, self.bullet_sprites, self.player_bullet_sprites], 1200)
        else:
            Bullet(pos,self.bullet_up_surf,direction,[self.all_sprites, self.bullet_sprites, self.player_bullet_sprites], 1200)

    def enemy_shoot(self, pos, direction):
        Bullet(pos,self.enemy_bullet_surf,direction,[self.all_sprites, self.bullet_sprites, self.enemy_bullet_sprites], 800)

    def get_points(self, pos,direction, points):
        if points == 500:
            Points(pos,self.five_hundred_points,direction,[self.all_sprites])
        elif points == 1000:
            Points(pos,self.one_thousand_points,direction,[self.all_sprites])
        elif points == 5000:
            Points(pos,self.five_thousand_points,direction,[self.all_sprites])

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.won_game:
                        pygame.quit()
                        sys.exit()

            dt = self.clock.tick() / 1000
            self.display_surface.fill((0, 0, 0))

            
            if self.won_game:
                self.win_screen.display()
            else:
                self.platform_collisions()
                self.all_sprites.update(dt)
                self.bullet_collisions()
                self.all_sprites.custom_draw(self.player)
                self.overlay.display()


            pygame.display.update()

if __name__ == '__main__':
    main = Main()
    main.run()