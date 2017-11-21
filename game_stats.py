class GameStats(object):
    """docstring for GameStats"""
    def __init__(self, ai_settings):
        super(GameStats, self).__init__()
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = True
        
    def reset_stats(self):
        """Inintialize statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit

        