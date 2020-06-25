# IMPORT PLIKÓW

# IMPORT PAKIETÓW  - potem można przerobić tak żeby się pobierały tylko używane funkcje
from PLAN_MISZCZ.Game import *
from PLAN_MISZCZ.Login import *
from PLAN_MISZCZ.Statistics import *

# GLOBAL VARIABLES:
player = ''  # nazwa gracza
screen = None  # okno gry tworzone w window_maker
database = r"..\db\mistrz_klawiatury.db"
cx = sqlite3.connect(database)
cu = cx.cursor()


# FUNKCJE INICJALIZACYJNE
def do_order_in_database():
    """
    Gustaw
    robi porządek w bazie danych, wykonuje się tuż po uruchomieniu, jak nie ma plików to je tworzy
    np przepisuje wyniki z poprzedniego dnia do tygodnia itp. Tutaj Gustaw może to rozplanować #order in data_base
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


def main_window():
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

    operation_code = 'qui'  # wstępnie napisane żeby Pycharm nie marudził
    arg = None
    return [operation_code, arg]


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
    icon = pygame.image.load('klawiatura.png')
    pygame.display.set_icon(icon)
    screen.fill((255, 255, 255))


# GŁÓWNA FUNKCJA PROGRAMU
def main():
    # inicjalizacja gry
    # Ignacy
    # inicjalizacja pygame
    pygame.init()
    # uporządkowanie bazy danych
    do_order_in_database()
    # stworzenie okna
    window_maker()
    # wybór gracza
    global player
    player = choose_player()
    # słownik z funkcjami
    functions = {'sta': show_statistics,
                 'ler': game_loop_learn,
                 'cha': game_loop_chalange,
                 'log': choose_player,
                 'qui': exit}

    # pętla gry
    while True:
        option = main_window()
        args = option[1:]
        code = option[0]
        if bool(args):
            functions[code](args)
        else:
            functions[code]()


# GRA
if __name__ == '__main__':
    main()
