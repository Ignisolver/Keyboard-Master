import sqlite3
from sqlite3 import Error
from sys import exit as close

database = r"..\db\mistrz_klawiatury.db"
cx = sqlite3.connect(database)
cu = cx.cursor()

import pygame


def download_input(period, nick):
    """
    # Gustaw
    pobiera dane z bazy danych do przedstawienia w statystykach
    :param period: okres czasu (jeden z :dziś / tydzień/ miesiąc/ od początku)
    :param nick:
    :return period_scores: lista ze słownikami : {'date' : <numer gry w dniu / data dnia / nr tygodnia/ nazwa miesiąca>(nie dluższe niz 12 znaków),
    'score' : <wynik z danego czasu> (int między 0 a 100 włacznia)}
    Gustaw ustal jak tu podzielimy te okresy
    (najlepiej żeby było max 10 wyników w jednym okresie żeby się pomieściły w oknie jakoś zgrabnie wraz z nazwami)
    """
    # today
    period_scores = None
    if period == 'dziś':
        cu.execute("select rowid, date, score from " + nick + "_stat_today")
        cx.commit()
        period_scores = cu.fetchall()

        for el in period_scores:
            print(el)
    else:
        pass

    return period_scores


download_input("dziś", "dfdfd")


def show_statistics(period, screen, size_x, size_y):
    """
    # Ignacy - DONE
    #czyści okno i rysuje swoje
    używa download_input
    rysuje statystyki za pomocą pygame - najlepiej w tym samym oknie co gra
    wychodzi z nich po nacisnieciu klawisza E - kończy funkcję
    Ignacy to zrobi (już mam prawie gotowe bo się trochę bawiłem)
    wcisniecie q konczy funkcje
    :param period:
    :return:
    """
    scores = download_input(period)
    amount_of_scores = len(scores)

    # ustawienia pola rysowania
    x0 = int(size_x / 12)
    y0 = int(size_y / 6.5) + 22
    x_max = int(size_x / 1.33)
    y_max = int(size_y / 1.345)
    x_length = x_max - x0
    y_length = abs(y0 - y_max)
    unit_q = 2
    unit = x_length / (unit_q * amount_of_scores)
    pole_width = unit
    rectangles = [pygame.Rect(x0 + i * unit_q * int(unit), y_max, int(pole_width), 2) for i in range(amount_of_scores)]

    # dane
    scores_points = [day['score'] for day in scores]
    scores_high = [y_max - y_length * i / 100 for i in scores_points]

    # ładowanie tła pokazywania statystyk
    myimage = pygame.image.load("siatka2.png")
    imagerect = myimage.get_rect()
    image_loc = [-5, -22]
    screen.blit(myimage, [*image_loc, *imagerect[2:4]])

    # rysowanie przedziałów czasowych
    black = (0, 0, 0)
    font = pygame.font.Font('freesansbold.ttf', 20)
    for nr, score in enumerate(scores):
        napis = score["date"]
        napis = napis if len(napis) < 12 else napis[:12]
        text = font.render(napis, True, black)
        text = pygame.transform.rotate(text, -70)
        textRect = text.get_rect()
        textRect.topleft = (rectangles[nr].left, rectangles[nr].bottomleft[1] + 5)
        screen.blit(text, textRect)
    pygame.display.update()

    running_flag = False  # gdy już słupki sie narysują wtedy przyjmuje wartosć False i wychodzi z pętli

    # pętla rysowania
    while not running_flag:
        # sprawdzanie zamknięcia
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close(0)

        running_flag = True

        for i in range(amount_of_scores):
            if rectangles[i].y >= scores_high[i]:
                pygame.draw.rect(screen, (0, 150, 255), rectangles[i])
                rectangles[i].y -= 1
                running_flag = running_flag and False
            else:
                running_flag = running_flag and True
        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            # sprawdzanie zamknięcia
            if event.type == pygame.QUIT:
                close(0)
            # sprawdzanie escape
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
        pygame.time.wait(100)


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
