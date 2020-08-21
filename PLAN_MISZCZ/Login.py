import sqlite3
import sys

import pygame
from Game import Keyborder

database = r"..\db\mistrz_klawiatury.db"
cx = sqlite3.connect(database, check_same_thread=False)
cu = cx.cursor()


def choose_player(screen=None, player_nick=None):  # TODO naprawić wyświetlanie i pobieranie tekstu
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

    # Zmienne pomocnicze
    gracze = download_users()
    font = pygame.font.Font('freesansbold.ttf', 50)
    zaznaczenie = 0
    len_gracze = len(gracze)

    # Ustawienia Okna
    screen.fill((255, 255, 255))

    # Pętla programu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if zaznaczenie != len_gracze:
                            for gracz in gracze.keys():
                                is_confirmed = check_pass(gracz, gracze[gracz], screen)
                                if is_confirmed:
                                    return gracz
                                else:
                                    screen.fill((255, 255, 255))
                        else:
                            n_gracz = sign_up(screen)
                            if n_gracz != '':
                                return n_gracz
                            else:
                                screen.fill((255, 255, 255))
                    elif (event.key == pygame.K_UP) or (event.key == pygame.K_w):
                        if zaznaczenie == 0:
                            zaznaczenie = len_gracze
                        else:
                            zaznaczenie -= 1
                    elif (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                        if zaznaczenie == len_gracze:
                            zaznaczenie = 0
                        else:
                            zaznaczenie += 1

        # wypisanie nazw
        n = 0
        instr = font.render("Wybór gracza:", True, (0, 0, 0), (255, 255, 255))
        screen.blit(instr, (100, 100))
        for nazwa_ in gracze.keys():
            if zaznaczenie == n:
                wypis = font.render(nazwa_, True, (0, 0, 0), (175, 255, 100))
            else:
                wypis = font.render(nazwa_, True, (0, 0, 0), (255, 255, 255))
            screen.blit(wypis, (115, (n * 60 + 160)))
            n += 1
        dodaj = font.render("+ Nowy gracz", True, (0, 0, 0),
                            ((175, 255, 100) if zaznaczenie == n else (255, 255, 255)))
        screen.blit(dodaj, (115, (n * 60 + 160)))
        pygame.display.flip()


def check_pass(nazwa, haslo, screen=None):
    """
        #Adrian
        #czyści okno i rysuje swoje
        otwiera okienko w pygame do wpisania hasła /
        pobiera hasło przy pomocy klasy Keyborder
        wyswietla info o niepoprawnym haśle / zwraca nazwę gracza
        mozna z niej zamknąć grę
        :return nazwa gracza (string): name - nazwa gracza
        """

    # dane gracza
    nazwa_ = nazwa
    haslo_ = haslo

    # Zmienne pomocnicze
    pob_str = Keyborder()
    tekst = "Wpisz hasło: ( " + nazwa_ + " )"
    check = False

    # Tworzenie okna
    screen.fill((255, 255, 255))
    font = pygame.font.Font('freesansbold.ttf', 50)
    fix = False
    # Pętla programu
    while True:
        wpis = pob_str.current_input
        dl_wpis = len(wpis)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            else:
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
                    return False
                elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
                    if wpis == haslo_:
                        return True
                    else:
                        check = True
                elif fix is not True:
                    pob_str.pg_str_input()
                    fix = True

        # Rysowanie okna
        instr = font.render(tekst, True, (0, 0, 0), (255, 255, 255))
        screen.blit(instr, (100, 100))
        sym = font.render((dl_wpis * "*") + (15 - dl_wpis) * "  ", True, (0, 0, 0), (220, 220, 220))
        screen.blit(sym, (100, 160))
        if check:
            error = font.render("Błędne hasło!", True, (200, 0, 0), (255, 255, 255))
            screen.blit(error, (100, 220))
        back = font.render("Powrót (ESC)", True, (0, 0, 0), (255, 255, 255))
        screen.blit(back, (80, 280))
        pygame.display.flip()


def sign_up(screen=None):
    """
    #Adrian
    #czyści okno i rysuje swoje
    otwiera okienko w pygame do wpisania hasła i nazwy
    pobiera hasło i nazwę przy pomocy klasy Keyborder
    po zatwierdzeniu wywołuje add_player
    mozna z niej zamknąć grę
    :return nazwa gracza (string): name - nazwa gracza
    """
    # Zmienne pomocnicze
    pob_naz = Keyborder()
    pob_has = Keyborder()
    is_name_saved = False
    same = False

    # Tworzenie okna
    screen.fill((255, 255, 255))
    font = pygame.font.Font('freesansbold.ttf', 50)
    # Pętla programu
    flaga_naz = False
    flaga_has = False

    while True:
        nazwa = pob_naz.current_input
        haslo = pob_has.current_input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            else:
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
                    if is_name_saved:
                        is_name_saved = False
                    else:
                        return ''
                elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
                    if is_name_saved:
                        same = add_player(nazwa, haslo)
                        if same:
                            return nazwa
                        else:
                            sign_up(screen)
                    else:
                        is_name_saved = True
                else:
                    if is_name_saved:
                        # pob_has.input_Thread()   # jakiś problem w pg_str ?
                        if flaga_has is not True:
                            pob_has.pg_str_input()
                            flaga_has = True
                    else:
                        # pob_naz.input_Thread()
                        if pob_has.finish is False or pob_naz.finish is False:
                            print("finish false!!!")
                        if flaga_naz is not True:
                            pob_naz.pg_str_input()
                            flaga_naz = True

        # Rysowanie okna
        instr1 = font.render("Wpisz nazwę użytkownika:", True, (0, 0, 0), (255, 255, 255))
        screen.blit(instr1, (100, 100))
        ramka_n = font.render(nazwa + (15 - len(nazwa)) * "  ", True, (0, 0, 0), (220, 220, 220))
        screen.blit(ramka_n, (100, 160))
        instr2 = font.render("Wpisz hasło:", True, (0, 0, 0), (255, 255, 255))
        screen.blit(instr2, (100, 220))
        ramka_n = font.render(len(haslo) * "*" + (15 - len(haslo)) * "  ",
                              True, (0, 0, 0), (220, 220, 220))
        screen.blit(ramka_n, (100, 280))
        if same:
            error = font.render("Istnieje użytkownik o takiej nazwie!", True, (200, 0, 0), (255, 255, 255))
            screen.blit(error, (100, 340))
        back = font.render("Powrót (ESC)", True, (0, 0, 0), (255, 255, 255))
        screen.blit(back, (80, 400))
        pygame.display.flip()


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
            "CREATE TABLE " + nick + "_stat_today (id integer primary key, score int, date text)")
        cu.execute(
            "CREATE TABLE " + nick + "_stat_week (id integer primary key, score int, date text)")
        cu.execute(
            "CREATE TABLE " + nick + "_stat_month (id integer primary key, score int, date text)")
        cu.execute(
            "CREATE TABLE " + nick + "_stat_ever (id integer primary key, score int, date text)")
        return True  # jeśli true, to dodano nowego gracza
    else:
        return False  # dodanie nie powiodlo sie, nick juz wystepuje w bazie
