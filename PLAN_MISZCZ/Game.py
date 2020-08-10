import random
import sqlite3
import sys
from threading import Thread
from keyboard import read_event
import pygame

database = r"..\db\mistrz_klawiatury.db"  # db connection using relative path
cx = sqlite3.connect(database)
# cx = sqlite3.connect(os.path.abspath(database))

cu = cx.cursor()


class Keyborder:
    """
    aby korzystać z funkcji wprowadania tekstu nalerzy utworzyć obiekt tej klasy
    - wywołanie funkcji pg_str_input spowoduje że w atrybucie current_input będzie się znajdował ciąg znaków
    który cały czas będzie się aktualizował ( w zależności od tego co będzie wpisywae na klawiaturze) - działa w
    osobnym wątku aż do naciśnięcia enter - po naciśnięciu current_input się nie usuwa
    obsługuje backspace,alr,shift
    """

    def pg_str_input(self):
        """
        #Ignacy
        odczytuje wciskane na klawiaturze klawisze, jest uruchamiana w osobnym wątku,
        kończy działanie po naciśnięciu enter - ustawia atrybut finish na True
        podczas działania zapisuje aktualny stan wpisywanego wyrazu do atrybutu current_input
        """
        self.finish = False
        self.current_input = ''
        Thread(target=self.input_Thread).start()

    def input_Thread(self):
        """
        - zapisuje aktualny input klawiatury do zmiennej globalnej
        - wymaga ustawienia input_enable na True na początku i na False na końcu
        :return:
        """
        hotkey_press = {'shift': False, 'alt': False, 'backspace': False}
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
        self.current_input = ''
        while True:
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         pygame.quit()
            #         exit(0)
            out = ''
            event = str(read_event())
            if 'alt' in event:
                hotkey_press['alt'] = True if 'down' in event else False
                continue
            if 'shift' in event:
                hotkey_press['shift'] = True if 'down' in event else False
                continue
            if 'backspace' in event:
                self.current_input = self.current_input[:-1] if len(self.current_input) >= 1 else ''
            if 'enter' in event:
                self.finish = True
                break
            pocz = event.find('(')
            end = event.find(')')
            event = event[pocz + 1:end]
            event = event.split(' ')
            if len(event) == 2:
                event, action = event

                if len(event) == 1 and action == 'down':
                    out = event
                    if hotkey_press['alt']:
                        out = letter_alt.get(out, out)
                    if hotkey_press['shift']:
                        out = out.capitalize()
                    self.current_input += out


def game_loop_chalange(level, player_nick=None, screen=None):
    """
        # Karol
        #czyści okno i rysuje swoje
        prowadzi grę w trybie wyzwanie czyli mierzy czas poprawnego wpisania wyrazu
        czysci okno (niech coś swojego rysuje)
        używa funkcji chose_word
        wyswietla napis który ma zostać wpisany
        nie pozwala wpisywac wyrazu dluzszego niz przewidziany - zapala kontrolke z komunikatem
        wyswietla litery wpisywane wraz z podświetleniem na kolor zielony - ok / czerwony - błędny wpis
        mierzy czas wpisywania wyrazu od naciśnięcia enter do poprawnego skończenia / enter przerywa - nie zapisuje wyniku
        wykorzystuje funkcję save_score której przekazuje poziom gry
        ESCAPE zamyka tryb
        :param level: poziom gry (easy/medium/hard)
        :return: None
        """

    # Inicjalizacja
    # Wartosci Pomocnicze
    white = (255, 255, 255)
    colour = (255, 0, 0)
    clock = pygame.time.Clock()
    delta = 0
    # Ustawienia Okna
    screen.fill(white)
    # Wartosci Początkowe
    word = choose_word(level)
    czas = 0
    warn = ""
    ipt = ""
    font = pygame.font.Font('freesansbold.ttf', 70)
    font1 = pygame.font.Font('freesansbold.ttf', 20)
    while True:
        for event in pygame.event.get():
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
                    # Koniec
                    if event.key == pygame.K_ESCAPE:
                        save_score(level, czas * 10, player_nick)
                        return None
                    letter = Keyborder.code2letter[event.key]
                    ipt += letter
                # Zatwierdzanie Poprawnego Wyniku
                if ipt == word and event.key == 13:
                    word = choose_word(level)
                    ipt = ""
                    czas += delta
                    delta = 0
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
def game_loop_learn(screen=None, player_nick=None):
    """
        # Karol
        #czyści okno i rysuje swoje
        wyswietla litery
        wykorzystuje choose_letter
        jak jest poprawna podaje kolejną a jak nie to czeka aż będzie
        enter przerywa grę
        :return: None
        """

    # Inicjalizacja
    # Wartosci Pomocnicze
    white = (255, 255, 255)
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
