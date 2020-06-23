from threading import Thread


def pg_str_input():
    """
    #Ignacy
    odczytuje wciśnity na klawiaturze klawisz
    (funkcje należy umieśćić w pętli)
    uwzgldnia litery polskie,cyfry,cpacje,CAPS,SHIFT,BACKSPACE,ENTER
    funkcja do wklejenia w petle
    Ignacy to robi (prawie gotowe)
    :return: klawisz (klawisze) ktory został wciśnięty jako napis
    """
    global input_enable
    input_enable = True
    Thread(target=input_Thread).start()


def input_Thread():
    """
    - zapisuje aktualny imput klawiatury do zmiennej globalnej
    - wymaga ustawienia imput_enable na True na początku i na False na końcu
    :return:
    """
    global current_input, pygame, code2letter, alt, letter_alt, UPP
    while True:
        letter = ''
        if input_enable:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if len(current_input) > 0:
                            current_input = current_input[:-1]
                    letter = code2letter.get(event.key, '')
            mode = pygame.key.get_mods()
            print(current_input)
            if mode in alt:
                letter = letter_alt.get(letter, letter)
            if mode in UPP:
                current_input += letter.upper()
            else:
                current_input += letter
        else:
            current_input = ''


def game_loop_chalange(level):
    """
    # Karol
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
    # Karol
    #czyści okno i rysuje swoje
    wyswietla litery
    wykorzystuje choose_letter
    jak jest poprawna podaje kolejną a jak nie to czeka aż będzie
    enter przerywa grę
    :return: None
    """


def choose_word(level):
    """
    # Adrian
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
    # Adrian
    funkcja analogiczna jak chose_word tylko zamiast haseł losuje lieterę
    może być prostsza ale fajnie jak by też jakoś minimalizowała powtórki
    :return litera:
    """


def save_score(level, score):
    """
    # Gustaw
    mnoży score razy jakąś wagę zależną od level i zapisuje do bazy
    :param level: poziom gry (easy/medium/hard)
    :param score: wynik jako czas w decysekundach (1s/10)
    :return:
    """
