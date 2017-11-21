import sys
import pygame
from bullet import Bullet
from ai import AI
from time import sleep

def check_events(ai_settings,screen,ship,bullets):
    """Respond to keypress and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit();

        elif event.type ==pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)


def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        #Move the ship to the right
        ship.moving_right =True;
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        #Move the ship to the left
        ship.moving_left = True;
    elif event.key == pygame.K_UP or event.key == pygame.K_w: 
        ship.moving_up = True;
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        #Create a new bullet and add it to the bullets group.
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_l:
        if ai_settings.bullet_width <= 500:
            ai_settings.bullet_width +=100


def fire_bullet(ai_settings,screen,ship,bullets):
    """Fire a bullet if limit not reached yet."""
    if len(bullets)< ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)


def check_keyup_events(event,ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = False

    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = False

    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        ship.moving_up = False

    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.moving_down = False

def update_screen(ai_settings,screen,ship,ais,bullets):
    """Update images on the screen and flip to the new screen."""
    #Redraw the screen during each pass through the loop
    screen.fill(ai_settings.backgroundcolor)
        #Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()


    ship.blitme();
    ais.draw(screen);

    #Make the most recently drawn screen visible.
    pygame.display.flip()

def update_bullets(ai_settings,screen,ship,ais,bullets):
    """Update position of bullets and get rid of old bullets."""

    #Update bullet positions.
    bullets.update()

    #Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,ship,ais,bullets)

def check_bullet_alien_collisions(ai_settings,screen,ship,ais,bullets):
    """Respond to bullet_alien collisions."""
    #Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets,ais,True,True)

    if len(ais) == 0:
        #Destroy existing bullets and create new fleet.
        bullets.empty()
        create_fleet(ai_settings,screen,ship,ais)


def create_fleet(ai_settings,screen,ship,ais):
    """Create a full of aliens"""
    #Create an alien and find the number of aliens in a row.
    #Spacing between each alien is equal to one alien width.
    ai = AI(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,ai.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,ai.rect.height)

    #Create the fleet of aliens.
    for row_number in range(number_rows):
        #Create the first row of aliens.
        for alien_number in range(number_aliens_x):
            #Create an alien and place it in the row.
            create_alien(ai_settings,screen,ais,alien_number,row_number)


def get_number_aliens_x(ai_settings,alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x/(2*alien_width))
    return number_aliens_x

def create_alien(ai_settings,screen,ais,alien_number,row_number):
    """Create an alien and place it in the row."""
    ai = AI(ai_settings,screen)
    alien_width = ai.rect.width;
    ai.x = alien_width+2*alien_width*alien_number
    ai.rect.x = ai.x
    ai.rect.y = ai.rect.height + 2*ai.rect.height*row_number
    ais.add(ai)

def get_number_rows(ai_settings,ship_height,alien_height):
    """Deterime the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height-(3*alien_height)-ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows

def update_aliens(ai_settings,stats,screen,ship,ais,bullets):
    """Update the position of all aliens in the fleet."""
    check_fleet_edges(ai_settings,ais)
    ais.update()
    check_aliens_bottom(ai_settings,stats,screen,ship,ais,bullets)
    #Look for alien_ship collisions.
    if pygame.sprite.spritecollideany(ship,ais):
        print("ship hit!!!Fuck,SB.")
        ship_hit(ai_settings,stats,screen,ship,ais,bullets)

def check_fleet_edges(ai_settings,ais):
    """Respond appropriately if any aliens have reached an edge."""
    for ai in ais.sprites():
        if ai.check_edges():
            change_fleet_direction(ai_settings,ais)
            break

def change_fleet_direction(ai_settings,ais):
    """Drop the entire fleet and change the fleet's direction."""
    for ai in ais.sprites():
        ai.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,stats,screen,ship,ais,bullets):
    """Respond to ship being hit by alien."""
    #Decrement ships_left.
    if stats.ships_left > 0:
        stats.ships_left -= 1
        #Empty the list of aliens and bullets.
        ais.empty()
        bullets.empty()

        #Create a new fleet anf center the ship.
        create_fleet(ai_settings,screen,ship,ais)
        ship.center_ship()

        #Pause.
        sleep(0.5)
    else:
        stats.game_active = False

def check_aliens_bottom(ai_settings,stats,screen,ship,ais,bullets):
    """check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for ai in ais.sprites():
        if ai.rect.bottom >= screen_rect.bottom:
            #Treat this the same as if the ship got hit.
            ship_hit(ai_settings,stats,screen,ship,ais,bullets)
            break