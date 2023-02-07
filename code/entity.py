from math import sin
import pygame
from pygame.math import Vector2
from settings import *
from os import walk



class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, path, groups, shoot):
        super().__init__(groups)
        # graphics import
        self.import_assets(path)
        self.frame_index = 0
        self.status = 'right_idle'

        # image setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = LAYERS['Level']
        self.mask = pygame.mask.from_surface(self.image)

        # float movement
        self.pos = Vector2(self.rect.center)
        self.direction = Vector2()
        self.speed = 400

        # shooting setup
        self.shoot = shoot
        self.can_shoot = True
        self.shoot_time = 0
        self.shoot_cooldown = 0.2
        self.duck = False

        # health
        self.health = 3

        # invulnerability timer
        self.is_vulnerable = True
        self.hit_time = 0
        self.invulnerability_cooldown = 0.5

        # sound
        self.hit_sound = pygame.mixer.Sound('../audio/hit.wav')
        self.hit_sound.set_volume(0.05)
        self.shoot_sound = pygame.mixer.Sound('../audio/bullet.wav')
        self.shoot_sound.set_volume(0.05)

    def blink(self):
        if not self.is_vulnerable:
            if self.wave_value():
                mask = pygame.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0,0,0))
                self.image = white_surf

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return True
        else:
            return False

    def import_assets(self, path):
        self.animations = {}
        for index , folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2], key = lambda string: int(string.split('.')[0])):
                    path = folder[0].replace('\\', '/') + '/' + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split('\\')[1]
                    self.animations[key].append(surf)

    def shoot_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks() / 1000
            if current_time - self.shoot_time > self.shoot_cooldown:
                self.can_shoot = True

    def invulnerability_timer(self):
        if not self.is_vulnerable:
            current_time = pygame.time.get_ticks() / 1000
            if current_time - self.hit_time > self.invulnerability_cooldown:
                self.is_vulnerable = True

    def animate(self, dt):
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def damage(self):
        if self.is_vulnerable:
            self.health -= 1
            self.is_vulnerable = False
            self.hit_time = pygame.time.get_ticks() / 1000
            self.hit_sound.play()


    def check_death(self):
        if self.health <= 0:
            self.kill()


