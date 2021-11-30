import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ Represents and alien"""

    def __init__(self, ai_settings, screen, col=0, row=0):
        """ Initialize the alien """
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width + 2 * self.rect.width * col
        self.rect.y = self.rect.height + 2 * self.rect.height * row

        self.x = float(self.rect.x)

    def blitme(self):
        """ Draw the alien """
        self.screen.blit(self.image, self.rect)

    def update(self):
        """ Move the alien right or left """
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """ Return True if alien is at the edge of the screen """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
