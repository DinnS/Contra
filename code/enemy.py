import pygame
from pygame.math import Vector2
from settings import *
from entity import Entity

class Enemy(Entity):
    def __init__(self, pos, path, groups, shoot, player, collision_sprites):
        super().__init__(pos, path, groups, shoot)
        self.player = player
        for sprite in collision_sprites.sprites():
            if sprite.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = sprite.rect.top

        self.shoot_cooldown = 0.2

    def get_status(self):
        if self.rect.centerx < self.player.rect.centerx:
            self.status = 'right_' + self.status.split('_')[1]
        else:
            self.status = 'left_' + self.status.split('_')[1]

    def check_fire(self):
        enemy_pos = Vector2(self.rect.center)
        player_pos = Vector2(self.player.rect.center)

        distance = (player_pos - enemy_pos).magnitude()
        same_y = True if self.rect.top - 20 < player_pos.y < self.rect.bottom + 20 else False

        if distance < 600 and same_y and self.can_shoot:
            bullet_direction = Vector2(1,0) if self.status.split('_')[0] == 'right' else Vector2(-1,0)
            y_offset = Vector2(0,-16)
            pos = self.rect.center + bullet_direction * 80
            self.shoot(pos + y_offset, bullet_direction,self)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks() / 1000

            self.shoot_sound.play()

    def update(self, dt):
        self.get_status()
        self.animate(dt)
        self.blink()
        self.check_fire()

        # timer
        self.shoot_timer()
        self.invulnerability_timer()

        # death
        self.check_death()

