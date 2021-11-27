import pygame
import sys


def check_keydown_events(event, ship):
    """ Reponse to keydown events"""
    if event.key == pygame.K_RIGHT:
        ship.direct_right()
    elif event.key == pygame.K_LEFT:
        ship.direct_left()


def check_keyup_events(event, ship):
    """ Reponse to keyup events"""
    if event.key == pygame.K_RIGHT and ship.moving_right:
        ship.stop()
    elif event.key == pygame.K_LEFT and ship.moving_left:
        ship.stop()


def check_events(ship):
    """ Respond to keypresses and mouse events. """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(ai_settings, screen, ship):
    """ Update images on the screen and flip to the new screen. """
    screen.fill(ai_settings.bg_color)
    ship.blitme()

    pygame.display.flip()
