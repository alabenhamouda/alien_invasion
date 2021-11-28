import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """ Represents the bullet """

    def __init__(self, screen, settings, ship):
        """ Initialize the bullet """
        super().__init__()
        self.screen = screen
        self.settings = settings

        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)
        self.color = settings.bullet_color

    def __bool__(self):
        """ Return True if the bullet is on the screen """
        return self.rect.bottom > self.screen.get_rect().top

    def update(self):
        """ Move the bullet up """
        self.y -= self.settings.bullet_speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """ Draw the bullet """
        pygame.draw.rect(self.screen, self.color, self.rect)
