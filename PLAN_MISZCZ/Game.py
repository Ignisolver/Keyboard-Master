def pg_str_input():
    """
    odczytuje wciśnity na klawiaturze klawisz
    (funkcje należy umieśćić w pętli)
    uwzgldnia litery polskie,cyfry,cpacje,CAPS,SHIFT,BACKSPACE,ENTER
    funkcja do wklejenia w petle
    Ignacy to robi (prawie gotowe)
    :return: klawisz (klawisze) ktory został wciśnięty jako napis
    """


def game_loop_chalange(level):
    """
    #czyści okno i rysuje swoje
    prowadzi grę w trybie wyzwanie czyli mierzy czas poprawnego wpisania wyrazu
    czysci okno (niech coś swojego rysuje)
    używa funkcji pg_str_input i chose_word
    wyswietla napis który ma zostać wpisany
    nie pozwala wpisywac wyrazu dluzszego niz przewidziany - zapala kontrolke z komunikatem
    wyswietla litery wpisywane wraz z podświetleniem na kolor zielony - ok / czerwony - błędny wpis
    mierzy czas wpisywania wyrazu od naciśnięcia enter do poprawnego skończenia / enter przerywa - nie zapisuje wyniku
    wykorzystuje funkcję save_score której przekazuje poziom gry
    :param level: poziom gry (easy/medium/hard)
    :return: None
    """


def game_loop_learn():
    """
    #czyści okno i rysuje swoje
    wyswietla litery
    wykorzystuje choose_letter
    jak jest poprawna podaje kolejną a jak nie to czeka aż będzie
    enter przerywa grę
    :return: None
    """


def choose_word(level):
    """
    losuje hasło z bazy o zadanym lewelu
    uwzględnia czy hasło było ostatnio używane (baza powinna to obsługiwać przechowując
     powiązaną z każdym hasłem wartość [może też być dla każdego gracza własna]
      True gdy hasło było użyte lub False gdy nie)
    jeżeli wszystkie hasła mają wartość true zmiania wszystkie na False i losuje
    :param level: poziom gry (easy/medium/hard)
    :return: słowo
    """


def choose_letter():
    """
    funkcja analogiczna jak chose_word tylko zamiast haseł losuje lieterę
    może być prostsza ale fajnie jak by też jakoś minimalizowała powtórki
    :return litera:
    """


def save_score(level, score):
    """
    mnoży score razy jakąś wagę zależną od level i zapisuje do bazy
    :param level: poziom gry (easy/medium/hard)
    :param score: wynik jako czas w decysekundach (1s/10)
    :return:
    """