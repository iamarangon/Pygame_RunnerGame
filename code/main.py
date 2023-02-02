import pygame
from sys import exit
from random import randint, choice
from sprites import Player, Obstacle


def display_score():
    current_time = int(pygame.time.get_ticks()/1000)-start_time
    score_surface = core_font.render(
        f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()

# SECTION - GAME SETUP
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Pixel Runner - Pygame')
clock = pygame.time.Clock()
core_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops=-1)
bg_music.set_volume(0.1)

#SECTION - GROUPS
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()
#!SECTION - GROUPS END

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# SECTION - INTRO SCREEN
player_stand = pygame.image.load(
    'graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = core_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = core_font.render('Press SPACE to Run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))
#!SECTION - INTRO SCREEN END

obstacle_timer = pygame.USEREVENT+1
pygame.time.set_timer(obstacle_timer, 1000)

#!SECTION - GAME SETUP END

# SECTION - GAME LOOP
while True:
    # SECTION - GAME STATUS
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)
    #!SECTION - GAME STATUS END

    # SECTION - GAME RUNNING
    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = core_font.render(
            f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    #!SECTION - GAME RUNNING END

    pygame.display.update()
    clock.tick(60)

#!SECTION - GAME LOOP END
