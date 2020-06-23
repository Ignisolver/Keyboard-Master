import sqlite3
from sqlite3 import Error

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


def download_users():
    """
    # Gustaw
    pobiera niki użytkowników z hasłami
    :return gracze: lista ze słownikami {'nazwa gracza': 'hasło'}
    """
    cu.execute("SELECT nick, password FROM players")
    cx.commit()
    gracze = cu.fetchall()
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
    else:
        pass


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
