import pygame
from settings import Settings
from ship import Ship
import game_function as gf
from pygame.sprite import Group
from ai import AI
from game_stats import GameStats
from over import Over
from time import sleep
def rungame():
    #Inittialize game,settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien make by Raven");

    #Set the background color
    #backgroundcolor = (200,128,230)

    #Create an instance to store game statistics.
    stats = GameStats(ai_settings)

    #Make a ship
    ship = Ship(ai_settings,screen);
    over = Over(screen)
    #Make a ai
    #ai = AI(ai_settings,screen)

    #Make a group to store bullets in.
    bullets = Group();
    #Make a group of aliens
    ais = Group()

    #Create the main loop for the game.
    gf.create_fleet(ai_settings,screen,ship,ais)
    
    #Start the main loop for the game.
    while True:
        gf.check_events(ai_settings,screen,ship,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,ship,ais,bullets)
            gf.update_aliens(ai_settings,stats,screen,ship,ais,bullets)
            gf.update_screen(ai_settings,screen,ship,ais,bullets)
        else:
            screen.fill((0,0,0))
            over.end()
            pygame.display.flip()


rungame();
input()