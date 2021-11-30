class Settings():
    """ A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 5

        # Alien settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Number of ships
        self.number_of_ships = 3

        # Text settings
        self.text_color = (30, 30, 30)
        self.text_font = 'arial'
        self.text_size = 20
        self.game_over_text_size = 50
        self.text_top_margin = 20
        self.text_right_margin = 20

        # Scoring options
        self.alien_points = 50
