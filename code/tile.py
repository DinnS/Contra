import pygame
from pygame.math import Vector2
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, surf, pos, z, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

class CollisionTile(Tile):
    def __init__(self, surf, pos, groups):
        super().__init__(surf, pos, LAYERS['Level'], groups)
        self.old_rect = self.rect.copy()

class MovingPlatform(CollisionTile):
    def __init__(self, surf, pos, groups):
        super().__init__(surf, pos, groups)

        # float based movement
        self.direction = Vector2(0,-1)
        self.speed = 200
        self.pos = Vector2(self.rect.topleft)

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

