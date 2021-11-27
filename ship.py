import pygame


class Ship():
    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)

        self.step = 0
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """ Draw the ship on the screen """
        self.screen.blit(self.image, self.rect)

    def direct_right(self):
        """ Move the ship to the right """
        self.step = self.ai_settings.ship_speed_factor
        self.moving_right = True
        self.moving_left = False

    def direct_left(self):
        """ Move the ship to the left """
        self.step = -self.ai_settings.ship_speed_factor
        self.moving_left = True
        self.moving_right = False

    def stop(self):
        """ Stop the ship """
        self.step = 0
        self.moving_right = False
        self.moving_left = False

    def move(self):
        """ Move the ship to the right """
        self.center += self.step
        self.rect.centerx = self.center
        if self.rect.right > self.screen_rect.right:
            self.rect.right = self.screen_rect.right
            self.center = self.rect.centerx
        elif self.rect.left < self.screen_rect.left:
            self.rect.left = self.screen_rect.left
            self.center = self.rect.centerx
