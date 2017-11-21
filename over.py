import pygame
class Over(object):
    """docstring for Over"""
    def __init__(self, screen):
        super(Over, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.center = self.screen_rect.center

    def end(self):
        self.screen.blit(self.image,self.rect)
        