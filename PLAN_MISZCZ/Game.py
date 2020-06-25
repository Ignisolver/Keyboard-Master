import random
import sqlite3
import sys
from threading import Thread

import pygame

database = r".\db\mistrz_klawiatury.db"  # db connection using relative path
cx = sqlite3.connect(database)
# cx = sqlite3.connect(os.path.abspath(database))
cu = cx.cursor()


class Keyborder:
    """
    aby korzystać z funkcji wprowadania tekstu nalerzy utworzyć obiekt tej klasy
    - wywołanie funkcji pg_str_input spowoduje że w atrybucie current_input będzie się znajdował ciąg znaków
    który cały czas będzie się aktualizował ( w zależności od tego co będzie wpisywae na klawiaturze) - działa w
    osobnym wątku aż do naciśnięcia enter
    """
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
        odczytuje wciskane na klawiaturze klawisze, jest uruchamiana w osobnym wątku,
        kończy działanie po naciśnięciu enter - ustawia atrybut finish na True
        podczas działania zapisuje aktualny stan wpisywanego wyrazu do atrybutu current_input
        """
        self.finish = False
        Thread(target=self.input_Thread).start()

    def input_Thread(self):
        """
        - zapisuje aktualny input klawiatury do zmiennej globalnej
        - wymaga ustawienia input_enable na True na początku i na False na końcu
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
    # Inicjalizacja
    pygame.init()
    # Wartosci Pomocnicze
    white = (255, 255, 255)
    green = (0, 255, 0)
    colour = (255, 0, 0)
    clock = pygame.time.Clock()
    delta = 0
    # Ustawienia Okna
    res = (1200, 650)
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption("Mistrz Klawiatury")
    screen.fill(white)
    # Wartosci Początkowe
    n = 0
    word = choose_word(level)
    czas = 0
    warn = ""
    ipt = ""
    font = pygame.font.Font('freesansbold.ttf', 70)
    font1 = pygame.font.Font('freesansbold.ttf', 20)
    while True:
        for event in pygame.event.get():
            if n == 10:
                save_score(level, czas)
            # Ostrzeżenie o liczbie liter
            if len(ipt) > len(word):
                warn = "Uwaga! Za dużo liter"
            else:
                warn = ""
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == 13 and ipt == "":
                    delta = 0
                if event.key == pygame.K_BACKSPACE:
                    if len(ipt):
                        ipt = ipt[:-1]
                else:
                    letter = Keyborder.code2letter[event.key]
                    ipt += letter
                # Zatwierdzanie Poprawnego Wyniku
                if ipt == word and event.key == 13:
                    word = choose_word()
                    ipt = ""
                    czas += delta
                    delta = 0
                    n += 1
        # Zarzadzanie kolorem czcionki
        if len(ipt) == 1:
            if ipt == word[0]:
                colour = (0, 255, 0)
            else:
                colour = (255, 0, 0)
        elif len(ipt) != 0:
            for i in range(len(ipt)):
                if ipt[:i + 1] == word[:i + 1]:
                    colour = (0, 255, 0)
                else:
                    colour = (255, 0, 0)
        # Zegar
        delta += clock.tick() / 1000.0
        # Rysowanie
        pygame.display.update()
        screen.fill(white)
        # Wyraz Wylosowany
        tekst = font.render(word, True, (0, 0, 0))
        tekst_prost = tekst.get_rect()
        tekst_prost.center = (600, 163)
        screen.blit(tekst, tekst_prost)
        # Wyraz Wpisany
        tekst1 = font.render(ipt, True, colour)
        tekst1_prost = tekst1.get_rect()
        tekst1_prost.center = (600, 325)
        screen.blit(tekst1, tekst1_prost)
        # Ostrzeżenie
        tekst2 = font.render(warn, True, (255, 0, 0))
        tekst2_prost = tekst2.get_rect()
        tekst2_prost.center = (600, 500)
        screen.blit(tekst2, tekst2_prost)
        # Czas
        tekst3 = font1.render("Czas odpowiedzi to " + str(czas)[:5] + " s", True, (0, 0, 0))
        tekst3_prost = tekst3.get_rect()
        tekst3_prost.center = (900, 30)
        screen.blit(tekst3, tekst3_prost)
        pygame.display.flip()


# Karol
def choose_letter():
    rand = random.randint(97, 122)
    return Keyborder.code2letter[rand]


# Karol
def game_loop_learn():
    # Inicjalizacja
    pygame.init()
    # Wartosci Pomocnicze
    white = (255, 255, 255)
    green = (0, 255, 0)
    # Ustawienia Okna
    res = (1200, 650)
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption("Mistrz Klawiatury")
    screen.fill(white)
    # Wartosci Początkowe
    char = choose_letter()
    letter = ''
    font = pygame.font.Font('freesansbold.ttf', 70)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == 13:
                    sys.exit(0)
                letter = Keyborder.code2letter[event.key]
                if letter == char:
                    char = choose_letter()
        # Rysowanie
        pygame.display.update()
        screen.fill(white)
        # Litera Wylosowana
        tekst = font.render(char, True, (0, 0, 0))
        tekst_prost = tekst.get_rect()
        tekst_prost.center = (600, 163)
        screen.blit(tekst, tekst_prost)
        # Litera Wpisana
        tekst1 = font.render(letter, True, (0, 0, 0))
        tekst1_prost = tekst1.get_rect()
        tekst1_prost.center = (600, 325)
        screen.blit(tekst1, tekst1_prost)
        pygame.display.flip()


# użyj poniższej funkcji po wylosowaniu słowa, jako argumenty podaj poziom (easy, medium lub hard oraz to słowo)

def increment_use_of_word(level, word):
    cu.execute("UPDATE " + level + "_words SET use_number = use_number + 1 WHERE word = \"" + word + "\" ")
    cx.commit()


def choose_word(level):
    """
    # Adrian
    losuje hasło z bazy o zadanym lewelu
    uwzględnia czy hasło było ostatnio używane (baza powinna to obsługiwać przechowując
     powiązaną z każdym hasłem wartość [może też być dla każdego gracza własna]
      True gdy hasło było użyte lub False gdy nie)
    jeżeli wszystkie hasła mają wartość true zmiania wszystkie na False i losuje
    :param level: poziom gry (easy, medium, hard)
    :return: słowo
    """
    wylosowana_liczba = random.randint(1, 25)

    cu.execute("SELECT \"word\" FROM " + level + "_words WHERE rowid = " + str(wylosowana_liczba))
    word = cu.fetchone()[0]
    increment_use_of_word(level, word)
    return word


def save_score(level, score, nick):
    """
    # Gustaw
    mnoży score razy jakąś wagę zależną od level i zapisuje do bazy
    :param level: poziom gry (1/2/3)
    :param score: wynik jako czas w decysekundach (1s/10)
    :param nick: nick
    :return:
    """
    score_to_db = str(score * level)
    cu.execute("insert into " + nick + "_stat_today (score,date) values (" + score_to_db + ",date('now'))")
    cu.execute("insert into " + nick + "_stat_ever (score,date) values (" + score_to_db + ",date('now'))")
    cx.commit()
    print('Score saved.')

# save_score(3, 23, 'gracztestowy')
