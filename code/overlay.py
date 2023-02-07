import pygame

class Overlay:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.health_surface = pygame.image.load('../graphics/health.png').convert_alpha()

    def display(self):
        # blit the health surf
        for x in range(self.player.health):
            x_pos = 50 + x * (self.health_surface.get_width() + 5)
            y_pos = 20
            self.display_surface.blit(self.health_surface,(x_pos,y_pos))

