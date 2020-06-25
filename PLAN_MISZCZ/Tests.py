import pygame
from Game import Keyborder
def image_shower(screen, image_name):
    image = pygame.image.load(image_name)
    imagerect = image.get_rect()
    image_loc = [0, 0]
    screen.blit(image, [*image_loc, *imagerect[2:4]])
    pygame.display.flip()

def main_choise_function(screen, image_names,Kb):
    image_shower(screen, image_names['main'])
    Kb.pg_str_input()
    while True:
        Kb.current_input = Kb.current_input[-1] if len(Kb.current_input) > 10 else Kb.current_input
        if Kb.finish is True:
            if Kb.current_input[-1] == ('s' or 'S'):
                main_choise = 's'
                break
            if Kb.current_input[-1] == ('g' or 'G'):
                main_choise = 'g'
                break
            if Kb.current_input[-1] == ('l' or 'L'):
                main_choise = 'l'
                break
    return main_choise

def statistisc_choise_function(screen, image_names,Kb):
    image_shower(screen, image_names['stat'])
    Kb.current_input = Kb.current_input
    Kb.pg_str_input()
    while True:
        Kb.current_input = Kb.current_input[-1] if len(Kb.current_input) > 10 else Kb.current_input
        if Kb.finish is True:
            if Kb.current_input[-1] == ('t' or 'T'):
                stat_choise = 1
                break
            if Kb.current_input[-1] == ('w' or 'W'):
                stat_choise = 2
                break
            if Kb.current_input[-1] == ('m' or 'M'):
                stat_choise = 3
                break
            if Kb.current_input[-1] == ('e' or 'E'):
                stat_choise = 4
                break
    return ['sta',stat_choise]  # TODO trzaba jakoś uwzględnić pobór niku w show_statistisc()

def gamemode_choise_function(screen, image_names,Kb):
    Kb.pg_str_input()
    Kb.current_input = Kb.current_input
    image_shower(screen, image_names['mode'])
    while True:
        Kb.current_input = Kb.current_input[-1] if len(Kb.current_input) > 10 else Kb.current_input
        if Kb.finish is True:
            if Kb.current_input[-1] == ('c' or 'C'):
                break
            if Kb.current_input[-1] == ('l' or 'L'):
                return 'ler'

    image_shower(screen, image_names['level'])

    Kb.pg_str_input()
    while True:
        Kb.current_input = Kb.current_input[-1] if len(Kb.current_input) > 10 else Kb.current_input
        if Kb.finish is True:
            if Kb.current_input[-1] == ('h' or 'H'):
                lvl_choise = 'h'
                break
            if Kb.current_input[-1] == ('m' or 'M'):
                lvl_choise = 'm'
                break
            if Kb.current_input[-1] == ('l' or 'L'):
                lvl_choise = 'l'
                break
    return ['cha', lvl_choise]


def main_window(screen):
    screen.fill((255, 255, 255))
    Kb = Keyborder()
    image_names = {'main': "main_main.png",
                   'stat': 'main_statistics.png',
                   'level': 'main_challenge_level.png',
                   'mode': 'main_gamemode.png'}
    #pierwszy wybór "main"
    main_choise = main_choise_function(screen, image_names,Kb)
    # wybor 2 po main
    if main_choise == 'l':  # logoff
        return 'log'

    if main_choise == 's':  # statistics
        return statistisc_choise_function(screen, image_names, Kb)

    if main_choise == 'g':  # game_mode
        return gamemode_choise_function(screen, image_names, Kb)


pygame.init()
screen = pygame.display.set_mode((1200, 650))
screen.fill((255, 255, 255))
main_window(screen)