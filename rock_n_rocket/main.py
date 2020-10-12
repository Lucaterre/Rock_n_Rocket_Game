##################################
# Rock 'n' Rocket
#
# Spatial Shoot'em up alike 1980's game
#
# -- ABSTRACT --
# A painter draws an abstract sky, when suddenly spots of paint,
# in the shape of rocks, come strewn over his work in progress.
# The painter decides to draw a spaceship to clean everything ...
#
# @ Luca Terre - 2020
##################################
import random
import time
import pygame
pygame.init()
from game import Game


##################################
# OPEN MAIN SCREEN (canva) #
##################################
pygame.display.set_caption("Rock 'n' Rocket")
screen = pygame.display.set_mode((1180, 850))

##################################
# LOAD GAME CLASSES #
##################################

game = Game()

##################################
# GAME USER MAINLOOP #
##################################
def mainloop(running: bool) -> None:
    """
    - Initial screen
    - Manage Players' keyboard & events during play

    :param running: bool if game is activate or not
    :return:
    """
    while running:
        # verifier si jeu a commencé ou non
        if game.is_playing:
            # déclencher instructions de partie
            game.update(screen)
        else:
            # ecran d'acceuil
            bg = pygame.image.load('assets/Home_game/home_bg.jpg')
            home_ship = [pygame.image.load('assets/Home_game/sprite_welcome0.png'),
                     pygame.image.load('assets/Home_game/sprite_welcome1.png'),
                     pygame.image.load('assets/Home_game/sprite_welcome2.png')]
            image_bg_home = pygame.transform.scale(bg, (1180, 850))
            screen.blit(image_bg_home, (0, 0))
            number = random.randint(0, 2)
            image_ship_home = pygame.transform.scale(home_ship[number], (650, 500))
            rect = image_ship_home.get_rect()
            rect.x = 255
            rect.y = 80
            screen.blit(image_ship_home, rect)
            time.sleep(1)
            play_button = pygame.image.load('assets/Home_game/button.png')
            play_button = pygame.transform.scale(play_button, (400, 300))
            play_button_rect = play_button.get_rect()
            play_button_rect.x = 300
            play_button_rect.y = 500
            screen.blit(play_button, (380, 660))



        # screen update
        pygame.display.flip()

        # if player close the window
        for event in pygame.event.get():
            # *close event
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            # *command user event
            elif event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True

                if event.key == pygame.K_SPACE:
                    if game.player.laser_ammo > 0:
                        game.player.launch_weapon()
                        game.player.laser_ammo = game.player.laser_ammo - 1


            elif event.type == pygame.KEYUP:
                game.pressed[event.key] = False
                game.player.right = False
                game.player.left = False
                game.player.up = False
                game.player.down = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # vérification de la collision avec le boutton start
                if play_button_rect.collidepoint(event.pos):
                    # mettre le jeu en mode lancer
                    game.start()

##################################
# START GAME #
##################################
running = True
mainloop(running)