import sys
import pygame
from settings import Settings
from pygame.sprite import Group, groupcollide, spritecollideany
from ship import Ship
from alien import Alien
from time import sleep


class Game():
    """ Holds all information about the game """

    def __init__(self):
        """ Initialize the game and create the screen """
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion")

        # initialize the settings
        self.settings = Settings()

        # initialize the game elements
        self.bullets = Group()
        self.ship = Ship(self.settings, self.screen, self.bullets)
        self.aliens = Group()
        self.remaining_ships = self.settings.number_of_ships

        self.score = 0

        # flag to indicate if the game is active
        self.running = True

        # create the fleet of aliens
        self.create_fleet()

    def run(self):
        """ Start the main loop for the game. """
        while True:
            self.clear_screen()
            self.check_events()
            self.display_score()
            self.display_remaining_ships()
            if self.running:
                self.handle_shot_aliens()
                self.ship.move()
                self.bullets.update()
                self.update_aliens()
                self.update_screen()
            else:
                self.print_game_over()
            pygame.display.flip()

    def check_keydown_events(self, event):
        """ Reponse to keydown events"""
        if event.key == pygame.K_RIGHT:
            self.ship.direct_right()
        elif event.key == pygame.K_LEFT:
            self.ship.direct_left()
        elif event.key == pygame.K_SPACE:
            self.ship.fire()

    def check_keyup_events(self, event):
        """ Reponse to keyup events"""
        if event.key == pygame.K_RIGHT and self.ship.moving_right:
            self.ship.stop()
        elif event.key == pygame.K_LEFT and self.ship.moving_left:
            self.ship.stop()

    def check_events(self):
        """ Respond to keypresses and mouse events. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)

    def get_number_aliens_x(self, alien_width):
        """ Determine the number of aliens that fit in a row. """
        available_space_x = self.settings.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x

    def get_number_aliens_y(self, alien_height):
        """ Determine the number of aliens that fit in a row. """
        available_space_y = self.settings.screen_height - \
            3 * alien_height - self.ship.rect.height
        number_aliens_y = int(available_space_y / (2 * alien_height))
        return number_aliens_y

    def create_fleet(self):
        """ Create a full fleet of aliens"""
        alien = Alien(self.settings, self.screen)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        number_aliens_x = self.get_number_aliens_x(alien_width)
        number_aliens_y = self.get_number_aliens_y(alien_height)
        for row_number in range(number_aliens_y):
            for alien_number in range(number_aliens_x):
                alien = Alien(self.settings, self.screen,
                              alien_number, row_number)
                self.aliens.add(alien)

    def check_fleet_edges(self):
        """ Respond appropriately if any aliens have reached an edge. """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def check_fleet_hit_bottom_edge(self):
        """ Check if any aliens have reached the bottom of the screen """
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen.get_rect().bottom:
                self.restart(True)
                break

    def check_fleet_hit_ship(self):
        """ Check if any aliens have hit the ship """
        if spritecollideany(self.ship, self.aliens):
            self.restart(True)

    def change_fleet_direction(self):
        """ Drop the fleet and change the direction """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    def update_aliens(self):
        """ Update the postions of all aliens in the fleet. """
        self.check_fleet_edges()
        self.check_fleet_hit_bottom_edge()
        self.check_fleet_hit_ship()
        self.aliens.update()

    def print_game_over(self):
        """ Show Game Over message """
        # display game over message
        font = pygame.font.SysFont(
            self.settings.text_font, self.settings.game_over_text_size)
        text = font.render("Game Over", True, self.settings.text_color)
        textRect = text.get_rect()
        textRect.centerx = self.screen.get_rect().centerx
        textRect.centery = self.screen.get_rect().centery
        self.screen.blit(text, textRect)

    def game_over(self):
        """ Display game over message and exit game """
        self.running = False

    def restart(self, remove_ship=False):
        """ Recenter ship and aliens, and create a new fleet """
        if remove_ship:
            self.remaining_ships -= 1
        # if no ships are left, end the game
        if self.remaining_ships == 0:
            self.game_over()
        else:
            self.settings.speedup_settings()
            self.ship.center_ship()
            self.bullets.empty()
            self.aliens.empty()
            self.create_fleet()
            sleep(0.3)

    def handle_shot_aliens(self):
        """ Check if any aliens have been shot and repopulate the fleet"""
        collisions = groupcollide(self.bullets, self.aliens, True, True)
        aliens_shot = sum(len(l) for l in collisions.values())
        self.score += aliens_shot * self.settings.alien_points
        if(len(self.aliens) == 0):
            self.restart()

    def display_score(self):
        """ Display the score at the top of the screen """
        font = pygame.font.SysFont(
            self.settings.text_font, self.settings.text_size)
        score_str = "{:,}".format(self.score)
        text = font.render("Score: " + score_str, True,
                           self.settings.text_color)
        text_rect = text.get_rect()
        text_rect.centerx = self.screen.get_rect().centerx
        text_rect.centery = self.settings.text_top_margin
        self.screen.blit(text, text_rect)

    def display_remaining_ships(self):
        """ Display the number of remaining ships """
        font = pygame.font.SysFont(
            self.settings.text_font, self.settings.text_size)
        text = font.render("Ships Remaining: " + str(self.remaining_ships),
                           True, self.settings.text_color)
        text_rect = text.get_rect()
        text_rect.right = self.screen.get_rect().right - self.settings.text_right_margin
        text_rect.centery = self.settings.text_top_margin
        self.screen.blit(text, text_rect)

    def update_screen(self):
        """ Update images on the screen and flip to the new screen. """
        self.ship.blitme()
        self.aliens.draw(self.screen)
        for bullet in self.bullets.sprites():
            if bullet:
                bullet.draw_bullet()
            else:
                self.bullets.remove(bullet)

    def clear_screen(self):
        """ Clear the screen to the background color """
        self.screen.fill(self.settings.bg_color)
