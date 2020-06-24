import sqlite3
import sys
import pygame

database = r"..\db\mistrz_klawiatury.db"
cx = sqlite3.connect(database)
cu = cx.cursor()


def choose_player():
    """
    #Adrian
    #czyści okno i rysuje swoje
    używa funkcji download_users do pobrania graczy
    rysuje w pygame ekran wyboru z prostokątem ktory podswietla aktualnego gracza
    wybranie gracza nastepuje poprzez enter
    możliwośc wycofania
    możliwość wyboru ADD PLAYER - uruchamia funkcję add_player
    otwiera okienko w tkinter do wpisania hasła /
    pobiera hasło za pomocą pygame (Ignacy zrobi funkcje do pobierania znaków z pygame)
    wyswietla info o niepoprawnym haśle / przechodzi dalej
    mozna z niej zamknąć grę
    :return nazwa gracza (string): name - nazwa gracza
    """

    pygame.init()

    # Zmienne pomocnicze

    gracze = download_users()
    font = pygame.font.Font('freesansbold.ttf', 50)
    zaznaczenie = 0
    len_gracze = len(gracze)

    # Ustawienia Okna

    screen = pygame.display.set_mode((1200, 650))
    pygame.display.set_caption("Mistrz Klawiatury")
    screen.fill((255,255,255))

    # Pętla programu

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if zaznaczenie != len_gracze:
                            check_pass(gracze[zaznaczenie])
                        else:
                            sign_in()
                    elif (event.key == pygame.K_UP) or (event.key == pygame.K_w)
                        if zaznaczenie == 0:
                            zaznaczenie = len_gracze
                        else:
                            zaznaczenie -= 1
                    elif (event.key == pygame.K_DOWN) or (event.key == pygame.K_s)
                        if zaznaczenie == len_gracze:
                            zaznaczenie = 0
                        else:
                            zaznaczenie += 1

        # wypisanie nazw
        n = 0
        instr = font.render("Wybór gracza:", True, (0,0,0))
        screen.blit(instr, (100,100))
        for gracz in gracze:
            for nazwa in gracz.keys():
                nazwa_ = nazwa
            if zaznaczenie == n:
                wypis = font.render(nazwa_, True, (0,0,0), (175,255,100))
            else:
                wypis = font.render(nazwa_, True, (0, 0, 0))
            screen.blit(wypis, (115,(n*60+160)))
            n+=1
        dodaj = font.render("+Nowy gracz", True, (0,0,0),
                            ( (175,255,100) if zaznaczenie == n else (0,0,0) ))
        screen.blit(dodaj,(115,(n*60+160)))
        pygame.display.flip()





def check_pass(gracz):
    """
        #Adrian
        #czyści okno i rysuje swoje
        otwiera okienko w pygame do wpisania hasła /
        pobiera hasło przy pomocy klasy Keyborder
        wyswietla info o niepoprawnym haśle / zwraca nazwę gracza
        mozna z niej zamknąć grę
        :return nazwa gracza (string): name - nazwa gracza
        """


    pygame.init()

    #dane gracza
    for g in gracz.keys():
        nazwa = g
        haslo = gracz[g]

    #Zmienne pomocnicze
    tekst = "Wpisz hasło: ( " + nazwa + " )"
    wpis =  Keyborder.current_input
    check = False
    dl_wpis = len(wpis)

    # Tworzenie okna
    screen = pygame.display.set_mode((1200, 650))
    pygame.display.set_caption("Mistrz Klawiatury")
    screen.fill((255, 255, 255))
    font = pygame.font.Font('freesansbold.ttf', 50)

    #Pętla programu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    choose_player()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if wpis == haslo:
                        return nazwa
                    else:
                        check = True
                else:
                    Keyborder.pg_str_input()

        # Rysowanie okna
        instr = font.render(tekst, True, (0, 0, 0))
        screen.blit(instr, (100, 100))
        sym = font.render(dl_wpis*"*", True, (0, 0, 0), (200,200,200))
        screen.blit(sym, (100, 160))
        if check:
            error = font.render("Błędne hasło", True, (200, 0, 0))
            screen.blit(error, (100, 220))
        back = font.render("Powrót (ESC)", True, (0, 0, 0))
        screen.blit(back, (80, 280))
        pygame.display.flip()




def sign_in():
    """
    #Adrian
    #czyści okno i rysuje swoje
    otwiera okienko w pygame do wpisania hasła i nazwy
    pobiera hasło i nazwę przy pomocy klasy Keyborder
    po zatwierdzeniu wywołuje add_player
    mozna z niej zamknąć grę
    :return nazwa gracza (string): name - nazwa gracza
    """


def download_users():
    """
    # Gustaw
    pobiera niki użytkowników z hasłami
    :return gracze: lista ze słownikami {'nazwa gracza': 'hasło'}
    """
    cu.execute("SELECT nick, password FROM players")
    cx.commit()
    gracze = cu.fetchall()  # wynik jest w formie słownika, klucz to nick, wartość to hasło
    nicknames = []
    passwords = []

    for el in gracze:
        nicknames.append(el[0])
        passwords.append(el[1])

    gracze = dict(zip(nicknames, passwords))  # list to dict conversion
    return gracze


def add_player(nick, password):
    """
    #Gustaw
    pozwala dodać gracza do bazy
    jest wywoływana z funkcji chose_player
    sprawdza czy już istanieje gracz o tej nazwi
    :return:
    """
    cu.execute("SELECT COUNT(*) FROM players WHERE nick==?", (nick,))
    cx.commit()
    result = cu.fetchone()
    if result == (0,):
        cu.execute("INSERT INTO players (nick, password) VALUES (?,?)", (nick, password))
        cx.commit()
        cu.execute(
            "CREATE TABLE " + nick + "_stat_today (id integer primary key, score int, date date)")
        cu.execute(
            "CREATE TABLE " + nick + "_stat_week (id integer primary key, score int, date date)")
        cu.execute(
            "CREATE TABLE " + nick + "_stat_month (id integer primary key, score int, date date)")
        cu.execute(
            "CREATE TABLE " + nick + "_stat_ever (id integer primary key, score int, date date)")
        return True  # jeśli true, to dodano nowego gracza
    else:
        return False  # dodanie nie powiodlo sie, nick juz wystepuje w bazie


add_player('gracztestowy', 'maslo')
