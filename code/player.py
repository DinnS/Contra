import sys
from pytmx.util_pygame import load_pygame
import pygame
from pygame.math import Vector2
from settings import *
from entity import Entity

class Player(Entity):
    def __init__(self, pos, path, groups, collision_sprites, shoot):
        super().__init__(pos, path, groups, shoot)

        # collision
        self.collision_sprites = collision_sprites

        # vertical movement
        self.gravity = 15
        self.jump_speed = 2000
        self.on_floor = False
        self.moving_floor = None

        self.health = 10

        tmx_map = load_pygame('../data/map.tmx')
        self.map_height = tmx_map.tileheight * tmx_map.height

    def get_status(self):
        side = self.status.split('_')[0] + '_'

        # idle
        if self.direction.x == 0 and self.on_floor:
            self.status = side + 'idle'

        # jump
        if self.direction.y != 0 and not self.on_floor:
            self.status = side + 'jump'

        # duck
        if self.on_floor and self.duck:
            self.status = side + 'duck'


    def check_contact(self):
        bottom_rect = pygame.Rect(0,0,self.rect.width,5)
        bottom_rect.midtop = self.rect.midbottom
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(bottom_rect):
                if self.direction.y > 0:
                    self.on_floor = True
                if hasattr(sprite,'direction'):
                    self.moving_floor = sprite

    def check_death(self):
        if self.health <= 0 or self.map_height < self.rect.bottom:
            pygame.quit()
            sys.exit()

    def input(self):
        keys = pygame.key.get_pressed()
        # horizontal movement
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right_walk'
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left_walk'
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.can_shoot:
            direction = Vector2(1, 0) if self.status.split('_')[0] == 'right' else Vector2(-1, 0)
            pos = self.rect.center + direction * 60
            y_offset = Vector2(0, -16) if not self.duck else Vector2(0, 8)
            self.shoot(pos + y_offset, direction, self)

            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks() / 1000

            self.shoot_sound.play()


        if keys[pygame.K_w] and self.on_floor:
            self.direction.y = -self.jump_speed

        if keys[pygame.K_s]:
            self.duck = True
        else:
            self.duck = False

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):

                if direction == 'horizontal':
                    # left collision
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    # right collision
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                    self.pos.x = self.rect.x
                else:
                    # top collision
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    # bottom collision
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.on_floor = True
                    self.pos.y = self.rect.y
                    self.direction.y = 0
        if self.on_floor and self.direction.y != 0:
            self.on_floor = False

    def movement(self, dt):
        if self.duck and self.on_floor:
            self.direction.x = 0
        # horizontal movement
        self.pos.x += self.speed * self.direction.x * dt
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')

        # vertical movement
        self.direction.y += self.gravity
        self.pos.y += self.direction.y * dt

        # glue the player to platform
        if self.moving_floor and self.moving_floor.direction.y > 0 and self.direction.y > 0:
            self.direction.y = 0
            self.rect.bottom = self.moving_floor.rect.top
            self.pos.y = self.rect.y
            self.on_floor = True

        self.rect.y = round(self.pos.y)
        self.collision('vertical')
        self.moving_floor = None

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.get_status()
        self.movement(dt)
        self.check_contact()

        self.animate(dt)
        self.blink()

        # timer
        self.shoot_timer()
        self.invulnerability_timer()

        # death
        self.check_death()




