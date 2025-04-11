class GameStats():

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()

        self.start_menu = True
        self.game_active = False
        self.game_over = False

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit


