def choose_player():
    """
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
    pobiera niki użytkowników z hasłami
    :return gracze: lista ze słownikami {'nazwa gracza': 'hasło'}
    """

def add_player():
    """
    pozwala dodać gracza do bazy
    jest wywoływana z funkcji chose_player
    :return:
    """