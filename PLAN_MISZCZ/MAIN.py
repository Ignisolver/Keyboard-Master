# IMPORT PLIKÓW

# IMPORT PAKIETÓW  - potem można przerobić tak żeby się pobierały tylko używane funkcje
import sqlite3
from threading import Thread
import pygame
from Game import Keyborder
# GLOBAL VARIABLES:
from Game import game_loop_learn, game_loop_chalange
from Login import choose_player
from Statistics import show_statistics

player = ''  # nazwa gracza
screen = None  # okno gry tworzone w window_maker
database = r"..\db\mistrz_klawiatury.db"
cx = sqlite3.connect(database)
cu = cx.cursor()


# FUNKCJE INICJALIZACYJNE
def do_order_in_database():
    """
    Gustaw
    robi pożądek w bazie danych
    wykonuje się tuż po uruchomieniu
    jak niema plików to je tworzy
    np przepisuje wyniki z poprzedniego dnia do tygodnia itp
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
        print(stats_from_week)
        for el in stats_from_week:
            cu.execute(
                "INSERT INTO " + playerdb + "_stat_month (\"score\", \"date\") VALUES (" + str(el[1]) + ", \"" + str(
                    el[0]) + "\")")
            cx.commit()
        cu.execute("DELETE FROM " + playerdb + "_stat_today")
        cx.commit()


def main_window(screen=None):
    """
    #Ignacy
    funkcja wyswietlająca ekran wyboru: trybu gry, poziomu, przejscia do statystyk, wylogowania.
    Pobiera z klawiatury literke i przechodzi do odpowiedniej funkcji
    :return chose_option: tablica [kod operacji, *args]
    kody operacji:
    'sta' - pokaż statystyki *arg: wybrany okres (day,week,month,begin) - do zmiany
    'ler' - tryb nauki *arg: -
    'cha' - tryb challange *arg: poziom trudnośi (easy/medium/hard)
    'log' - log off *arg: -
    'qui' - zamknij grę *arg: -
    """
    screen.fill((255, 255, 255))
    Kb = Keyborder()
    image_names = {'main': "Others/main_window_images/main_main.png",
                   'stat': 'Others/main_window_images/main_statistics.png',
                   'level': 'Others/main_window_images/main_challenge_level.png',
                   'mode': 'Others/main_window_images/main_gamemode.png'}
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
    :return:
    """
    size_x = 1200
    size_y = 650
    global screen
    screen = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption("Miszcz Klawiatury")
    icon = pygame.image.load('../Others/klawiatura.png')
    pygame.display.set_icon(icon)
    screen.fill((255, 255, 255))
    return screen


# GŁÓWNA FUNKCJA PROGRAMU
def main():
    # inicjalizacja gry
    # Ignacy
    # inicjalizacja pygame
    pygame.init()
    Thread(target=QUIT_enabler).start()
    # uporządkowanie bazy danych
    do_order_in_database()
    # stworzenie okna
    screen = window_maker()
    # wybór gracza
    global player
    player = choose_player(screen)
    # słownik z funkcjami
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
        functions[code](args, player_nick=player, screen=screen)


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
    Kb.current_input = Kb.current_input
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


def statistisc_choise_function(screen, image_names, keyborder_obj):
    image_shower(screen, image_names['stat'])
    keyborder_obj.pg_str_input()
    while True:
        keyborder_obj.current_input = keyborder_obj.current_input[-1] if len(
            keyborder_obj.current_input) > 10 else keyborder_obj.current_input
        if keyborder_obj.finish is True:
            if keyborder_obj.current_input[-1] == ('t' or 'T'):
                stat_choise = 1
                break
            if keyborder_obj.current_input[-1] == ('w' or 'W'):
                stat_choise = 2
                break
            if keyborder_obj.current_input[-1] == ('m' or 'M'):
                stat_choise = 3
                break
            if keyborder_obj.current_input[-1] == ('e' or 'E'):
                stat_choise = 4
                break
    return ['sta', stat_choise]  # TODO trzaba jakoś uwzględnić pobór niku w show_statistisc()


def gamemode_choise_function(screen, image_names, Kb):
    Kb.pg_str_input()
    Kb.current_input = Kb.current_input
    image_shower(screen, image_names['mode'])
    while True:
        Kb.current_input = Kb.current_input[-1] if len(Kb.current_input) > 10 else Kb.current_input
        if Kb.finish is True:
            if Kb.current_input[-1] == ('c' or 'C'):
                break
            if Kb.current_input[-1] == ('l' or 'L'):
                return ['ler']

    image_shower(screen, image_names['level'])

    Kb.pg_str_input()
    while True:
        Kb.current_input = Kb.current_input[-1] if len(Kb.current_input) > 10 else Kb.current_input
        if Kb.finish is True:
            if Kb.current_input[-1] == ('h' or 'H'):  # hard
                lvl_choise = 3
                break
            if Kb.current_input[-1] == ('m' or 'M'):  # medium
                lvl_choise = 2
                break
            if Kb.current_input[-1] == ('l' or 'L'):  # low
                lvl_choise = 1
                break
    return ['cha', lvl_choise]

def QUIT_enabler():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

# GRA
if __name__ == '__main__':
    main()
