import sys
import pygame
from pytmx.util_pygame import load_pygame

from settings import *
from tile import Tile, CollisionTile, MovingPlatform
from player import Player
from enemy import Enemy
from allsprites import AllSprites
from bullet import Bullet, FireAnimation
from overlay import Overlay


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Contra')
        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.vulnerable_sprites = pygame.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.player)

        # bullet images
        self.bullet_surf = pygame.image.load('../graphics/bullet.png').convert_alpha()
        self.fire_surfs = [
            pygame.image.load('../graphics/fire/0.png').convert_alpha(),
            pygame.image.load('../graphics/fire/1.png').convert_alpha()
        ]

        # music
        self.background_music = pygame.mixer.Sound('../audio/music.wav')
        self.background_music.set_volume(0.01)
        self.background_music.play(loops=-1)


    def setup(self):
        tmx_map = load_pygame('../data/map.tmx')

        # collision tiles
        for x, y, surf in tmx_map.get_layer_by_name('Level').tiles():
            CollisionTile(surf, (x * 64, y * 64), [self.all_sprites, self.collision_sprites])

        # tiles
        for layer in ['BG', 'BG Detail', 'FG Detail Top', 'FG Detail Bottom']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile(surf, (x * 64, y * 64), LAYERS[layer], self.all_sprites)

        # objects
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player': self.player = Player(
                pos=(obj.x, obj.y),
                path='../graphics/player',
                groups=[self.all_sprites, self.vulnerable_sprites],
                collision_sprites=self.collision_sprites,
                shoot=self.shoot
            )
            if obj.name == 'Enemy':
                Enemy(
                    pos=(obj.x, obj.y),
                    path='../graphics/enemy',
                    groups=[self.all_sprites, self.vulnerable_sprites],
                    shoot=self.shoot,
                    player=self.player,
                    collision_sprites=self.collision_sprites
                )

        self.platform_border_rects = []
        for obj in tmx_map.get_layer_by_name('Platforms'):
            if obj.name == 'Platform':
                MovingPlatform(obj.image, (obj.x,obj.y), [self.all_sprites, self.collision_sprites, self.platform_sprites])
            else: # border
                border_rect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
                self.platform_border_rects.append(border_rect)

    def platform_collisions(self):
        for platform in self.platform_sprites.sprites():
            for border in self.platform_border_rects:
                # bounce the platforms
                if platform.rect.colliderect(border):
                    if platform.direction.y < 0:
                        platform.rect.top = border.bottom
                        platform.pos.y = platform.rect.y
                        platform.direction.y = 1
                    else:
                        platform.rect.bottom = border.top
                        platform.pos.y = platform.rect.y
                        platform.direction.y = -1

            if platform.rect.colliderect(self.player.rect) and self.player.rect.centery > platform.rect.centery:
                platform.rect.bottom = self.player.rect.top
                platform.pos.y = platform.rect.y
                platform.direction.y = -1

    def bullet_collisions(self):
        # obstacles
        for obstacle in self.collision_sprites.sprites():
            pygame.sprite.spritecollide(obstacle, self.bullet_sprites, True)
        # entities
        for sprite in self.vulnerable_sprites.sprites():
            if pygame.sprite.spritecollide(sprite, self.bullet_sprites, True, pygame.sprite.collide_mask):
                sprite.damage()

    def shoot(self , pos, direction, entity):
        Bullet(self.bullet_surf,  pos, direction, [self.all_sprites, self.bullet_sprites])
        FireAnimation(entity, self.fire_surfs, direction, self.all_sprites)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.dt = self.clock.tick() / 1000
            self.display_surface.fill((249,131,103))

            self.platform_collisions()
            self.all_sprites.update(self.dt)
            self.bullet_collisions()

            self.all_sprites.custom_draw(self.player)
            self.overlay.display()

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()