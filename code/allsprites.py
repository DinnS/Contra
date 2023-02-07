import pygame
from pygame.math import Vector2
from pytmx.util_pygame import load_pygame
from settings import *


# camera class
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = Vector2()

        # import
        self.fg_sky = pygame.image.load('../graphics/sky/fg_sky.png').convert_alpha()
        self.bg_sky = pygame.image.load('../graphics/sky/bg_sky.png').convert_alpha()
        tmx_map = load_pygame('../data/map.tmx')

        # dimension
        self.padding = WINDOW_WIDTH / 2
        self.sky_width = self.bg_sky.get_width()
        map_width = tmx_map.tilewidth * tmx_map.width + (2 * self.padding)
        self.sky_number = int(map_width // self.sky_width)

    def custom_draw(self, player):
        # change the offset
        self.offset.x = player.rect.centerx - (WINDOW_WIDTH / 2)
        self.offset.y = player.rect.centery - (WINDOW_HEIGHT / 2)

        # draw background sky
        for x in range(self.sky_number):
            x_pos = -self.padding + (x * self.sky_width)
            self.display_surface.blit(self.bg_sky, (x_pos - (self.offset.x / 2.5),850 - (self.offset.y / 2.5)))
            self.display_surface.blit(self.fg_sky, (x_pos - (self.offset.x / 2), 850 - (self.offset.y / 2)))

        # blit all sprite
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset

            self.display_surface.blit(sprite.image,offset_rect)