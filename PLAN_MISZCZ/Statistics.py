def download_input(period):
    """
    pobiera dane z bazy danych do przedstawienia w statystykach
    :param period: okres czasu (jeden z :dziś / tydzień/ miesiąc/ od początku)
    :return period_scores: lista ze słownikami : {'date' : <numer gry w dniu / data dnia / nr tygodnia/ nazwa miesiąca>:
    <wynik z danego czasu>}
    Gustaw ustal jak tu podzielimy te okresy
    (najlepiej żeby było max 10 wyników w jednym okresie żeby się pomieściły w oknie jakoś zgrabnie wraz z nazwami)
    """


def show_statistisc(period_scores):
    """
    #czyści okno i rysuje swoje
    używa download_input
    rysuje statystyki za pomocą pygame - najlepiej w tym samym oknie co gra
    wychodzi z nich po nacisnieciu klawisza E - kończy funkcję
    ma mozliwosc zmainy okresu - moze nie koniecznie rekurencją
    Ignacy to zrobi (już mam prawie gotowe bo się trochę bawiłem)
    wcisniecie q konczy funkcje
    :param period_scores:
    :return:
    """
