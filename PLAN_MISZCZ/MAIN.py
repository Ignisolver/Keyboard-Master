# IMPORT PLIKÓW
# IMPORT PAKIETÓW  - potem można przerobić tak żeby się pobierały tylko używane funkcje
import sqlite3
from threading import Thread
from time import sleep

import pygame
from Game import Keyborder
# GLOBAL VARIABLES:
from Game import game_loop_learn, game_loop_chalange
from Login import choose_player
from Statistics import show_statistics
from elevate import elevate
from waiting import wait

player = ''  # nazwa gracza
screen = None  # okno gry tworzone w window_maker
database = r"..\db\mistrz_klawiatury.db"
cx = sqlite3.connect(database)
cu = cx.cursor()


# FUNKCJE INICJALIZACYJNE
def do_order_in_database():
    """
    Gustaw
    robi porządek w bazie danych
    wykonuje się tuż po uruchomieniu
    jak nie ma plików, to je tworzy,
    np. przepisuje wyniki z poprzedniego dnia do tygodnia itp
    tutaj Gustaw może to rozplanować #order in data_base
    :return:
    """
    cu.execute("SELECT nick FROM players")
    nicks = []
    nicks_from_db = cu.fetchall()
    for el in nicks_from_db:
        nicks.append(el[0])

    for playerdb in nicks:
        cu.execute(
            "SELECT SUM(\"score\"), \"date\" FROM " + playerdb + "_stat_today GROUP BY \"date\"")
        stats_from_today = cu.fetchall()
        for el in stats_from_today:
            cu.execute(
                "INSERT INTO " + playerdb + "_stat_week (\"score\", \"date\") VALUES (" + str(el[0]) + ", \"" + str(
                    el[1]) + "\")")
            cx.commit()

        cu.execute(
            "select strftime(\'%m\',\"date\") as \"miesiac\", sum(\"score\") as \"wynik\" from " + playerdb + "_stat_week group by strftime(\'%m\',\"date\")")
        stats_from_week = cu.fetchall()
        # print(stats_from_week)
        for el in stats_from_week:
            cu.execute(
                "INSERT INTO " + playerdb + "_stat_month (\"score\", \"date\") VALUES (" + str(el[1]) + ", \"" + str(
                    el[0]) + "\")")
            cx.commit()
        cu.execute("DELETE FROM " + playerdb + "_stat_today")
        cx.commit()

# do_order_in_database()

def main_window(screen=None):
    """
    #Ignacy
    funkcja wyswietlająca ekran wyboru: trybu gry, poziomu, przejscia do statystyk, wylogowania.
    Pobiera z klawiatury literke i przechodzi do odpowiedniej funkcji
    :return chose_option: tablica [kod operacji, *args]
    kody operacji:
    'sta' - pokaż statystyki *arg: wybrany okres (day,week,month,begin - int 1,2,3,4)
    'ler' - tryb nauki *arg: -
    'cha' - tryb challange *arg: poziom trudnośi (easy/medium/hard - int 1,2,3)
    'log' - log off *arg: -
    'qui' - zamknij grę *arg: -
    """
    screen.fill((255, 255, 255))
    Kb = Keyborder()
    image_names = {'main': "../Others/main_window_images/main_main.png",
                   'stat': '../Others/main_window_images/main_statistics.png',
                   'level': '../Others/main_window_images/main_challenge_level.png',
                   'mode': '../Others/main_window_images/main_gamemode.png'}
    # pierwszy wybór "main"
    main_choise = main_choise_function(screen, image_names, Kb)
    # wybor 2 po main
    if main_choise == 'l':  # logoff
        return ['log']

    if main_choise == 's':  # statistics
        return statistisc_choise_function(screen, image_names, Kb)

    if main_choise == 'g':  # game_mode
        return gamemode_choise_function(screen, image_names, Kb)


def window_maker():
    """
    #Ignacy
    tworzy okno o jakichś wymiarach - można spróbować dopasować do ekranu
    :return: screen - obiekt pygame tworzony przez pygame.display.set_mode()
    """
    size_x = 1200
    size_y = 650
    global screen
    screen = pygame.display.set_mode([size_x, size_y])
    pygame.display.set_caption("Miszcz Klawiatury")
    icon = pygame.image.load('../Others/klawiatura.png')
    pygame.display.set_icon(icon)
    screen.fill((255, 255, 255))
    return screen


# GŁÓWNA FUNKCJA PROGRAMU
def main():

    pygame.init()
    # do_order_in_database()
    # stworzenie okna
    screen = window_maker()
    # if get_system_name() == 'Linux':
    #     root_logging()
    # wybór gracza
    player = choose_player(screen)

    # uwaga: hakerski sposób na przechytrzenie pygame+threading+windows
    Thread(target=continue_main,args=[screen,player]).start()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        sleep(1)

def continue_main(screen,player):
    """
    funkcja pozwalająca na bez awaryjne działanie programu
    - awaria polegała na błędzie (Not responding)
    :param screen:
    :return:
    """
    functions = {'sta': show_statistics,
                 'ler': game_loop_learn,
                 'cha': game_loop_chalange,
                 'log': choose_player,
                 }
    # pętla gry
    while True:
        option = main_window(screen)
        code = option[0]
        args = option[1:]
        print(option)
        functions[code](*args, player_nick=player, screen=screen)


# funkcje pomocnicze


def image_shower(screen, image_name):
    image = pygame.image.load(image_name)
    imagerect = image.get_rect()
    image_loc = [0, 0]
    screen.blit(image, [*image_loc, *imagerect[2:4]])
    pygame.display.flip()


def main_choise_function(screen, image_names, Kb):
    image_shower(screen, image_names['main'])
    Kb.pg_str_input()
    while wait(Kb.is_finished):
        main_choise = Kb.current_input[-1] if len(Kb.current_input) > 0 else ''
        if main_choise in ('s', 'g', 'l'):
            return main_choise


def statistisc_choise_function(screen, image_names, Kb):
    image_shower(screen, image_names['stat'])
    to_return = {'t': 1, 'w': 2, 'm': 3, 'e': 4}
    Kb.pg_str_input()
    while wait(Kb.is_finished):
        stat_choise = Kb.current_input[-1] if len(Kb.current_input) > 0 else ''
        if stat_choise in ('t', 'w', 'm', 'e'):
            return ['sta', to_return[stat_choise]]


def gamemode_choise_function(screen, image_names, Kb):
    image_shower(screen, image_names['mode'])
    Kb.pg_str_input()
    while wait(Kb.is_finished):
        mode_choise = Kb.current_input[-1] if len(Kb.current_input) > 0 else ''
        if mode_choise == 'l':
            return ['ler']
        elif mode_choise == 'c':
            break

    image_shower(screen, image_names['level'])
    to_return = {'l': 1, 'm': 2, 'h': 3}
    while wait(Kb.is_finished):
        lvl_choise = Kb.current_input[-1] if len(Kb.current_input) > 0 else ''
        if lvl_choise in ('h', 'm', 'l'):
            return ['cha', to_return[lvl_choise]]


def root_logging():
    elevate()




# GRA
if __name__ == '__main__':
    main()
