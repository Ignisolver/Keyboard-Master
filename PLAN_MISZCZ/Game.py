import sqlite3
from threading import Thread
import pygame

database = r"..\db\mistrz_klawiatury.db"
cx = sqlite3.connect(database)
cu = cx.cursor()


class Keyborder:
    UPP = (12288, 4098, 4097, 28672, 20482, 20481, 12545, 12546, 8192, 2, 1, 24576, 16386, 16385, 8449, 8450)
    alt = (20480, 28672, 20482, 20481, 12545, 12546, 16384, 24576, 16386, 16385, 8449, 8450)
    code2letter = {97: 'a',
                   98: 'b',
                   99: 'c',
                   100: 'd',
                   101: 'e',
                   102: 'f',
                   103: 'g',
                   104: 'h',
                   105: 'i',
                   106: 'j',
                   107: 'k',
                   108: 'l',
                   109: 'm',
                   110: 'n',
                   111: 'o',
                   112: 'p',
                   113: 'q',
                   114: 'r',
                   115: 's',
                   116: 't',
                   117: 'u',
                   118: 'w',
                   119: 'v',
                   120: 'x',
                   121: 'y',
                   122: 'z',
                   32: ' '}
    letter_alt = {
        'l': 'ł',
        'n': 'ń',
        's': 'ś',
        'o': 'ó',
        'a': 'ą',
        'e': 'ę',
        'z': 'ż',
        'x': 'ź',
        'c': 'ć',
    }
    current_input = ''
    finish = False

    def pg_str_input(self):
        """
        #Ignacy
        odczytuje wciskane na klawiaturze klawisze
        jest uruchamiana w osobnym wątku
        kończy działanie po naciśnięciu enter - ustawia atrbut finish na True
        podczas działania zapisuje aktualny stan wpisywanego wyrazu do atrybutu current_input
        """
        self.finish = False
        Thread(target=self.input_Thread).start()

    def input_Thread(self):
        """
        - zapisuje aktualny imput klawiatury do zmiennej globalnej
        - wymaga ustawienia imput_enable na True na początku i na False na końcu
        :return:
        """
        self.current_input = ''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.finish = True
                        return None
                    if event.key == pygame.K_BACKSPACE:
                        if len(self.current_input) > 0:
                            self.current_input = self.current_input[:-1]
                    letter = self.code2letter.get(event.key, '')
                    mode = pygame.key.get_mods()
                    if mode in self.alt:
                        letter = self.letter_alt.get(letter, letter)
                    if mode in self.UPP:
                        self.current_input += letter.upper()
                    else:
                        self.current_input += letter


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
