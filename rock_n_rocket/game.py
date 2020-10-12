import pygame
import random

##################################
# TIME #
##################################

time = pygame.time.Clock()

##################################
# GAME SOUNDS #
##################################

laser_sound = pygame.mixer.Sound('sounds/laser.wav')
reload_sound = pygame.mixer.Sound('sounds/reload.wav')
gameover_sound = pygame.mixer.Sound('sounds/explosion.wav')

##################################
# GAME LOGIC #
##################################

class Game:
    def __init__(self):
        # définir si le jeu a commencé
        self.is_playing = False
        self.screen = pygame.display.set_mode((1180, 850))
        # génère un joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        self.all_monsters = pygame.sprite.Group()
        self.pressed = {}

    def start(self):
        self.is_playing = True
        self.spawn_monster()

    def game_over(self):
        # remettre le jeu à zero
        bg = pygame.image.load('assets/bg.jpg')
        self.screen.blit(bg, (-40, -100))
        self.screen.blit(self.player.image_player_kill, self.player.rect)
        game_over_banner = pygame.image.load('assets/game_over/game_over_3.png')
        image_game_over = pygame.transform.scale(game_over_banner, (600, 400))
        image_game_over_rect = image_game_over.get_rect()
        image_game_over_rect.x = 450
        image_game_over_rect.y = 200
        self.screen.blit(image_game_over, image_game_over_rect)
        self.all_monsters = pygame.sprite.Group()
        self.player.pv = self.player.max_health
        self.is_playing = False

    def update(self, screen):
        # background import
        bg = pygame.image.load('assets/bg.jpg')
        screen.blit(bg, (-40, -100))
        # player image apply

        #screen.blit(self.player.image, self.player.rect)

        # actualiser la barre de vie du joueur
        self.player.update_health_bar(screen)

        # actualiser le score
        font = pygame.font.SysFont("comicsans", 30, True)
        score = self.player.score_player
        text = font.render(f"Score: {str(score)}", 1, (0, 0, 0))
        screen.blit(text, (0, 0))

        # actualiser le nombre de munitions
        laser_ammo = self.player.laser_ammo
        text_ammo = font.render(f"Laser : {str(laser_ammo)}", 1, (0, 0, 0))
        screen.blit(text_ammo, (0, 50))
        self.player.all_weapon.draw(screen)
        if self.player.laser_ammo == 0:
            print('plus de munition')
            self.player.reload_laser()


        #recuperer les projectiles du joueur
        for shoot in self.player.all_weapon:
            shoot.move()

        # recupères les monstres
        for monster in self.all_monsters:
            monster.forward()

        # apply projectiles image
        #self.player.all_weapon.draw(screen)

        # apply monsters image
        self.all_monsters.draw(screen)

        # verify kind of key

        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
            self.player.redraw_window(screen)
            #print(self.pressed)
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()
            self.player.redraw_window(screen)
            #print(self.pressed)
        elif self.pressed.get(pygame.K_UP) and self.player.rect.y > 0:
            self.player.move_up()
            self.player.redraw_window(screen)
            #print(self.pressed)
        elif self.pressed.get(pygame.K_DOWN) and self.player.rect.y + self.player.rect.height < screen.get_height() :
            self.player.move_down()
            self.player.redraw_window(screen)
            #print(self.pressed)
        elif not self.pressed.get(pygame.K_LEFT) and not self.pressed.get(pygame.K_RIGHT):
             self.player.redraw_window(screen)
             #print(self.pressed)

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self):
        monster_rock = monsterRock(self)
        self.all_monsters.add(monster_rock)

# class user

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.pv = 100
        self.max_health = 100
        self.attack = 1
        self.velocity = 40
        self.score_player = 0
        self.all_weapon = pygame.sprite.Group()
        self.image = pygame.image.load('assets/player.png')
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 675
        self.image_right = pygame.image.load('assets/player_right.png')
        self.image_right = pygame.transform.scale(self.image_right, (150, 150))
        self.image_left = pygame.image.load('assets/player_left.png')
        self.image_left = pygame.transform.scale(self.image_left, (150, 150))
        self.image_up = pygame.image.load('assets/player_up.png')
        self.image_up = pygame.transform.scale(self.image_up, (150, 150))
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.image_player_kill = pygame.image.load('assets/game_over/player_kill.png')
        self.image_player_kill = pygame.transform.scale(self.image_player_kill, (150, 150))
        self.laser_ammo = 10
        self.last = pygame.time.get_ticks()

        self.cooldown = 10000

    def redraw_window(self, surface):
        if self.right and not self.left and not self.up and not self.down:
            surface.blit(self.image_right, self.rect)
            #print('ok right')
        elif self.left and not self.right and not self.up and not self.down:
            surface.blit(self.image_left, self.rect)
            #print('ok left')
        elif not self.left and not self.right and self.up and not self.down:
            surface.blit(self.image_up, self.rect)
            #print('ok up')
        elif not self.left and not self.right and not self.up and self.down:
            surface.blit(self.image, self.rect)
            #print('ok down')
        elif not self.left and not self.right:
            self.right = False
            self.left = False
            self.up = False
            self.down = False
            surface.blit(self.image, self.rect)
            #print('ok normal')


    def damage(self, amount):
        if self.pv - amount > amount:
            self.pv -= amount
        elif self.pv == 0:
            gameover_sound.play()
            self.game.game_over()
        else:
            self.pv = 0


    def launch_weapon(self):
        laser_sound.play()
        self.all_weapon.add(laserShoot(self))


    # temporiser les tirs
    def reload_laser(self):
        now = pygame.time.get_ticks()
        print(f'now vaut : {now}')
        print(f'last vaut : {self.last}')
        print(f'cooldown vaut : {self.cooldown}')
        print(f'now - self.last vaut : {self.cooldown - (now - self.last)}')
        if now - self.last >= self.cooldown:
            print('recharge')
            self.laser_ammo = 10
            reload_sound.play()
            self.last = now



    def move_right(self):
        self.right = True
        self.left = False
        self.up = False
        self.down = False
        self.rect.x += self.velocity

    def move_left(self):
        self.left = True
        self.right = False
        self.up = False
        self.down = False
        self.rect.x -= self.velocity

    def move_up(self):
        self.up = True
        self.down = False
        self.left = False
        self.right = False
        self.rect.y -= self.velocity

    def move_down(self):
        self.up = False
        self.down = True
        self.left = False
        self.right = False
        self.rect.y += self.velocity

    def update_health_bar(self, surface):
        # dessiner la barre
        pygame.draw.rect(surface, (218, 218, 218), [self.rect.x + 27, self.rect.y + 145, self.pv, 5])
        pygame.draw.rect(surface, (73, 184, 28), [self.rect.x + 27, self.rect.y + 145, self.pv, 5])



# class projectiles

class laserShoot(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.velocity = 40
        self.player = player
        self.image = pygame.image.load('assets/laser_shoot.png')
        self.image = pygame.transform.scale(self.image, (160, 150))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.laser_attack_amount = 1


    def remove(self):
        self.player.all_weapon.remove(self)


    def move(self):
            self.rect.y -= self.velocity
            # vérifier si le projectile rentre en collision
            for monster in self.player.game.check_collision(self, self.player.game.all_monsters):
                # suppresion projectile
                self.remove()
                # infliger dégât
                monster.damage(self.player.attack)
                # update score
                self.player.score_player += 1

            # vérifier si projectile n'est plus présent
            if self.rect.y < -850:
                self.remove()



# monsters :
#  * rock : 1 PV; 10 attack

class monsterRock(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.pv = 1
        self.max_pv = 1
        self.attack = 0.5
        self.image = pygame.image.load('assets/monster_rock.png')
        self.image = pygame.transform.scale(self.image, (180, 250))
        self.image_rock_kill = pygame.image.load('assets/monster_rock_kill.png')
        self.image_rock_kill = pygame.transform.scale(self.image_rock_kill , (180, 250))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1055)
        self.velocity = random.randint(5, 60)
        self.origin_image = self.image
        self.angle = 0

    def remove(self):
        self.game.all_monsters.remove(self)

    def damage(self, amount):
        # Infliger dégâts
        self.pv -= amount
        # vérifier si son nombre de points de vie et inférieur ou égal à 0
        if self.pv <= 0:
            self.game.screen.blit(self.image_rock_kill, self.rect)
            self.rect.x = random.randint(0, 1055)
            self.rect.y = -20
            self.velocity = random.randint(5, 60)
            self.pv = self.max_pv


    def rotate(self):
        self.angle += 5
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def forward(self):
        self.rect.y += self.velocity
        self.rotate()
        if self.rect.y > 800:
            self.rect.x = random.randint(0, 1055)
            self.rect.y = -30
            self.velocity = random.randint(5, 60)
            self.pv = self.max_pv
        if self.game.check_collision(self, self.game.all_players):
            self.game.player.damage(self.attack)

