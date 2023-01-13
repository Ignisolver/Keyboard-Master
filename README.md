# Mistrz Klawiatury

## Wstęp

Mistrz klawiatury to gra polegająca na przepisywaniu wyświetlanych wyrazów w jak najkrótszym czasie. Wykorzystuje ona moduł ```pygame``` oraz bazę danych sqlite3.

## Uruchomienie

Aby włączyć grę, należy w katalogu ```PLAN_MISZCZ``` wykonać następujący skrypt:

```bash
    MAIN.py
```

## Struktura aplikacji

## ```MAIN.py```

W pliku ```MAIN.py``` zostały zdefiniowane funkcje inicjalizacyjne, które odpowiadają za przygotowanie wszystkich niezbędnych zmiennych oraz bazy danych do rozgrywki, wyniki z poprzedniego dnia trafiają do tabeli w bazie odpowiadającej za rejestrowanie wyników z całego tygodnia.

### ```do_order_in_database()```

```python
    cu.execute("SELECT nick FROM players")
    nicks = []
    nicks_from_db = cu.fetchall()
    for el in nicks_from_db:
        nicks.append(el[0])

    for playerdb in nicks:
        cu.execute(
            "SELECT SUM(\"score\"), \"date\" FROM " + playerdb + "_stat_today GROUP BY \"date\"")
        stats_from_today = cu.fetchall()
        for el in stats_from_today:
            cu.execute(
                "INSERT INTO " + playerdb + "_stat_week (\"score\", \"date\") VALUES (" + str(el[0]) + ", \"" + str(
                    el[1]) + "\")")
            cx.commit()

        cu.execute(
            "select strftime(\'%m\',\"date\") as \"miesiac\", sum(\"score\") as \"wynik\" from " + playerdb + "_stat_week group by strftime(\'%m\',\"date\")")
        stats_from_week = cu.fetchall()
        print(stats_from_week)
        for el in stats_from_week:
            cu.execute(
                "INSERT INTO " + playerdb + "_stat_month (\"score\", \"date\") VALUES (" + str(el[1]) + ", \"" + str(
                    el[0]) + "\")")
            cx.commit()
        cu.execute("DELETE FROM " + playerdb + "_stat_today")
        cx.commit()
```
Funkcja ```do_order_in_database``` pobiera z tabeli ```<player>_stat_today``` wyniki, następnie grupuje je po dacie, a wyniki sumuje, po czym wstawia je do tabeli ```<player>_stat_week```, a w końcu stosuje polecenie ``` DELETE``` do wyczyszczenia zawartości pierwszej z tabel. Dzieje się tak dla każdego gracza.

### ```window_maker()```

```python
    size_x = 1200
    size_y = 650
    global screen
    screen = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption("Miszcz Klawiatury")
    icon = pygame.image.load('klawiatura.png')
    pygame.display.set_icon(icon)
    screen.fill((255, 255, 255))
```
Funkcja odpowiada za utworzenie okna, w którym będą wyświetlane wybrane ramki.
params: nie przyjmuje argumentów
return: screen - obiekt pygame tworzony przez pygame.display.set_mode()
Własności okna:
    szerokość: 1200 pix
    wysokość: 600 pix
    ikona: Klawiatura.png
    nagłówek okna: Miszcz Klawiatury
    kolor wypełnienia: biały

### ```main_window(screen=None)```
Funkcja tworząca na ekranie (```screen```) główne okno aplikacji - to z którego użytkownik będzie mógł wybrac czy chce grać czy używać statystyki czy się wylogować.
Pozwala wybrać tryb i poziom gry oraz okres z jakiego mają być wyswietlone statystyki.
Co zwraca:
Gdy zostanie wybrana opcja wylogowania zwraca ```['log']```
Gdy zostanie wybrana opcja pokazania statystyk zwraca krotkę. Pierwszy element to ```'sta'``` a drugi to int z zakresu 1,2,3,4 gdzie 1=tomorrow, 2=week, 3=month, 4=ever
Gdy zostanie wybrana opcja gry w trybie nauki zwraca ```['ler']```.
Gdy zostanie wybrana opcja gry w trybie wyzwania zwraca krotkę. Pierwszy element to ```'cha'``` a drugi to int z zakresu 1,2,3 gdzie 1=low, 2=medium, 3=hard

### ```main()```

```python
    pygame.init()
    do_order_in_database()
    window_maker()
    global player
    player = choose_player()
    functions = {'sta': show_statistics,
                 'ler': game_loop_learn,
                 'cha': game_loop_chalange,
                 'log': choose_player,
                 'qui': exit}
    while True:
        option = main_window()
        args = option[1:]
        code = option[0]
        if bool(args):
            functions[code](args)
        else:
            functions[code]()
```

W funkcji ```main()``` po kolei zostają wywoływane funkcje, które odpowiadają za poprawną inicjalizację aplikacji.

## ```Game.py```

W tym module zaimplementowana została cała logika rozgrywki, jak na przykład losowanie wyrazów.

### ```save_score(level, score, nick)```

```python
    score_to_db = str(score * level)
    cu.execute("insert into " + nick + "_stat_today (score,date) values (" + score_to_db + ",date('now'))")
    cu.execute("insert into " + nick + "_stat_ever (score,date) values (" + score_to_db + ",date('now'))")
    cx.commit()
    print('Score saved.')
```

Powyższa funkcja przyjmuje 3 argumenty: ```level, score, nick```, gdzie ```level``` to liczba z zakresu 1-3 (1 - łatwy, 2 - trudny, 3 - średni), dwa pozostałe są oczywiste. Następnie wynik i poziom trudności są mnożone i wstawianie do tabeli z dnia obecnego ( ```<player>_stat_today``` ) oraz do tabeli historycznej, która agreguje wszystkie wyniki od początku ( ```<player>_stat_ever``` ).


### ```game_loop_learn(screen, player_nick)```

```python
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
```

Funkcja (jak sama nazwa wskazuje) służy do nauki podstawowych zasad gry oraz jej integracji z klawiaturą. Przyjmuje ona argumenty ```screen``` i ```player_nick```, których znaczenie jest oczywiste. 
W pierwszym etapie "czyści" ona ekran oraz korzystając z funkcji ```choose_letter()```, losuje literę którą użytkownik powinien wpisać. W przypadku błędu proces jest ponawiany, zaś w przypadku wpisania prawidłowej litery, funkcja losuje kolejną, aż do momentu w którym użytkownik zdecyduje się zakończyć zabawę. 


### ```game_loop_challange(level, player_nick, screen)```

```python
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
```

Nadrzędnym celem powyższej funkcji jest zbadanie stopnia zaawansowania użytkownika oraz czasu jego reakcji. Funkcja przyjmuje za argumenty ```level```, ```player_nick``` oraz ```screen``` i nie zwraca żadnej wartości. 
Korzystając z funkcji ```choose_word()```, losuje ona słowo które gracz musi wpisać oraz zatwierdzić klawiszem ENTER. Funkcja mierzy czas pomiędzy kolejnymi odpowiedziami, następnie przy pomocy funkcji ```save_score()``` przekazuje wynik gracza. Dodatkowo podczas gry wprowadzone są pewne ograniczenia związane z błędną długością wpisywanego wyrazu.


### ```Keyborder```
Klasa służąca obsłudze wprowadzania znaków z klawiatury.
Użytkowanie:
    Należy stworzyć obiekt klasy ```KB = Keyborder()```
    W celu rozpoczęcia przechwytywania znaków ależy uruchomić metodę ```pg_str_input```: ```KB.pg_str_input()```
    Po jej uruchomieniu w atrybucie ```current_input``` (```KB.current_input```) znajduje się ciąg znaków zawierający wszystkie litery jakie po kolei były odczytywane z klawiatury. 
Funkcja uwzględnia alt , shift i backspace.
Funkcja kończy działanie po wciśnięciu klawisza ENTER - zmienia wtedy stan atrybutu ```finish``` na ```True```
Po zakończeniu działania funkcji atrybut ```current_input``` nie zostaje wyczyszczony - dzieje się to dopiero po ponownym wywołaniu metody.
Funkcja uruchamia się w osobnym wątku co gwarantuje nie pominięcie przechwycenia jakiegoś klawisza.

### ```increment_use_of_word(level, word)```

```python
    cu.execute("UPDATE " + level + "_words SET use_number = use_number + 1 WHERE word = \"" + word + "\" ")
    cx.commit()
```

Funkcja przyjmuje jako argument poziom oraz wyraz, a następnie zwiększa ilość  użyć danego słowa w bazie.

### ```choose_word(level)```

```python
    wylosowana_liczba = random.randint(1, 25)

    cu.execute("SELECT \"word\" FROM " + level + "_words WHERE rowid = " + str(wylosowana_liczba))
    word = cu.fetchone()[0]
    increment_use_of_word(level, word)
    return word
```

Funkcja losuje wyraz z bazy słów z podanego jako argument poziomu, przy pomocy funkcji ```increment_use_of_word()``` zwiększa w bazie zapisaną ilość jego wystąpień i zwraca wylosowane słowo.  



## ```Statistics.py```

### ```download_input(period, nick)```

```python
    period_dict = {1: "today", 2: "week", 3: "month", 4: "ever"}
    period_scores = None
    cu.execute(
        "select rowid, date, score from " + nick + "_stat_" + period_dict[period] + " ORDER BY \"date\" DESC LIMIT 10")
    cx.commit()
    period_scores = cu.fetchall()
    return period_scores
```

```download_input()``` służy do pobierania z bazy danych wyników dla dowolnego gracza za wybrany okres (dzień, tydzień, miesiąc, od początku), wymaga ona podania jako argumentów nicku gracza oraz wartości liczbowej przypisanej danemu okresowi. Jakie są to wartości, widać w pierwszej linii. Funkcja zwraca listę trójelementowych krotek, każda w formacie (numer wiersza, data , wynik).


### ```show_statistics(period, screen, player_nick)```
Funkcja pokazująca na ekranie (```screen```) statystyki gracza o danym nicku (```player_nick```) z danego okresu (```period```)
params:
```screen``` - obiekt ```pygame.display.set_mode((size_x, size_y))```
```period, player_nick``` - takie jak argumenty funkcji ```download_input```
return:



## ```Login.py```

Tu zawarta została mechanika logowania, oraz inicjalizacji nowego gracza.

### ```choose_player(screen, player_nick)```

```python

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
                            for x in gracze.keys():
                                check_pass(x, gracze[x], screen)
                        else:
                            sign_up(screen)
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
        for gracz in gracze.keys():
            for nazwa in gracz:
                nazwa_ = nazwa
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
```

Funkcja wyświetlająca menu wyboru gracza. Jako parametr (`screen`) przyjmuje okno, na którym rysuje. Pozwala na wybranie przy pomocy klawiatury jednego z listy graczy pobranej z bazy, lub na utworzenie nowego. Umożliwia zamknięcie programu. Zwraca nazwę wybranego użytkownika.

### ```check_pass(nazwa, haslo, screen)```

```python
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
                else:
                    pob_str.pg_str_input()

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
```

Funkcja wyświetlająca ekran logowania. Przyjmuje nazwę gracza, hasło z nim powiązane oraz okno (```screen```), na którym rysuje. Pozwala wprowadzić hasło, które jest porównywane z przyjętym parametrem. Błędne hasło wyświetla informację. Zwraca ```True``` gdy hasło jest zgodne, lub ```False``` gdy użytkownik wycofał.

### ```sign_up(screen)```

```python

    # Zmienne pomocnicze
    pob_naz = Keyborder()
    pob_has = Keyborder()
    is_name_saved = False
    same = False

    # Tworzenie okna
    screen.fill((255, 255, 255))
    font = pygame.font.Font('freesansbold.ttf', 50)
    # Pętla programu
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
                        pob_has.pg_str_input()
                    else:
                        # pob_naz.input_Thread()
                        if pob_has.finish is False or pob_naz.finish is False:
                            print("finish false!!!")
                        pob_naz.pg_str_input()

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

```

Funkcja wyświetlająca ekran rejestracji nowego użytkownika. Przyjmuje parametr ```screen``` , na którym rysowane są wprowadzane dane. Możliwość wycofania i wyświetlenia informacji, gdy istnieje użytkownik o podanej nazwie. Zwraca nazwę nowego gracza.

### ```download_users()```

```python
    cu.execute("SELECT nick, password FROM players")
    cx.commit()
    gracze = cu.fetchall()
    nicknames = []
    passwords = []

    for el in gracze:
        nicknames.append(el[0])
        passwords.append(el[1])

    gracze = dict(zip(nicknames, passwords))
    return gracze
```

Funkcja może być wywołana, aby sprawdzić, czy logujący się użytkownik jest już w bazie, pobiera ona listę nicków oraz haseł, a nastęnie zwraca je w formie słownika, gdzie klucz to nick, a wartość to hasło.

### ```add_player(nick, password)```

```python
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
        return True
    else:
        return False
```

Funkcja służy do dopisywania nowego gracza do bazy, jako parametry przyjmuje nick, oraz hasło, które może być alfanumeryczne, następnie przeszukuje tabelę z użytkownikami w poszukiwaniu powtórzeń nicku, jeżeli nie znajdzie, zostaną utworzone cztery tabele na zapisywanie statystyk danego gracza, a sama funkcja zwróci wartość ```python True```, w przeciwnym wypadku, tabela nie zostaną utowrzone i zostanie zwrócone ```python False```.


## Działanie aplikacji
### Wybór gracza
![obraz](https://user-images.githubusercontent.com/62255841/212265652-3d9dcd1a-41a8-43c4-911f-3a8194a6acec.png)
### Ekran logowania
![obraz](https://user-images.githubusercontent.com/62255841/212265720-72e93f14-4c29-45ae-9eb8-617e1f3e21c4.png)
### Wybór opcji
![obraz](https://user-images.githubusercontent.com/62255841/212265772-79d3cf01-03a2-4d76-bcf2-3bfd3b9954ee.png)
### Wybór trybu gry
![obraz](https://user-images.githubusercontent.com/62255841/212265825-f8cde4fa-291c-4c78-833a-af50dc5bce07.png)
### Tryb nauki
![obraz](https://user-images.githubusercontent.com/62255841/212265887-34735e72-d350-4c2c-8fd9-3dbb5f39aebe.png)
### Wybór poziomu gry w trybie challenge
![obraz](https://user-images.githubusercontent.com/62255841/212265944-f20dd626-5eac-442a-95a1-22f0536812ec.png)
### Tryb challenge - poprawne wpisanie słowa
![obraz](https://user-images.githubusercontent.com/62255841/212266197-5e1afab4-7084-451e-976b-94161d7dd221.png)
### Tryb challenge - niepoprawne wpisanie słowa
![obraz](https://user-images.githubusercontent.com/62255841/212267516-234f07e0-432b-4b48-a0d3-afa483c0ad73.png)


## Autorzy
Porjekt był realizowany w ramach projektu na studia wspólnie z trzema kolegami.

