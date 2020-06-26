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
Własności okna:
    szerokość: 1200 pix
    wysokość: 600 pix
    ikona: Klawiatura.png
    nagłówek okna: Miszcz Klawiatury
    kolor wypełnienia: biały

### ```main_window(screen=None)```
Funkcja tworząca na ekranie (```screen```) główne okno alpikacji - to z którego użytkownik będzie mógł wybrac czy chce grać czy używać statystyki czy się wylogować.
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


### ```Keyborder```
Klasa służąca obsłudze wprowadzania znaków z klawiatury.
Użytkowanie:
    Należy stworzyć obiekt klasy ```KB = Keyborder()```
    W celu rozpoczęcia przechwytywania znaków ależy uruchomić metodę ```pg_str_input```: ```KB.pg_str_input()```
    Po jej uruchomieniu w atrybucie ```current_input``` (```KB.current_input```) znajduje się ciąg znaków zawierający wszystkie litery jakie po kolei były odczytywane z klawiatury. 
Funkcja uwzględnia małe i duze litery i backspace.
Funkcja kończy działanie po wciśnięciu klawisza ENTER - zmienia wtedy stan atrybutu ```finish``` na ```True```
Po zakończeniu działania funkcji atrybut ```current_input``` nie zostaje wyczyszczony - dzieje się to dopiero po ponownym wywołaniu metody.
Funkcja uruchamia się w osobnym wątku co gwarantuje nie pominięcie przechwycenia jakiegoś klawisza.
Obsługuje wyłączenie programu


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

## ```Login.py```

Tu zawarta została mechanika logowania, oraz inicjalizacji nowego gracza.

### ```choose_player()```

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

Funkcja wyświetlająca menu wyboru gracza. Jako parametr przyjmuje okno, na którym rysuje. Pozwala na wybranie przy pomocy klawiatury jednego z listy graczy pobranej z bazy, lub na utworzenie nowego. Umożliwia zamknięcie programu. Zwraca nazwę wybranego użytkownika.

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

Funkcja służy do dopisywania nowego gracza do bazy, jako poarametry przyjmuje nick, oraz hasło, które może być alfanumeryczne, następnie przeszukuję tabelę z użytkownikami w poszukiwaniu powtórzeń nicku, jeżeli nie znajdzie, zostaną utworzone cztery tabele na zapisywanie statystyk danego gracza, a sama funkcja zwróci wartość ```python True```, w przeciwnym wypadku, tabela nie zostaną utowrzone i zostanie zwrócone ```python False```.

### ```show_statistics(period, screen, player_nick)```
Funkcja pokazująca na ekranie (```screen```) statystyki gracza o danym nicku (```player_nick```) z danego okresu (```period```)
argumenty:
```screen``` - obiekt ```pygame.display.set_mode((size_x, size_y))```
```period, player_nick``` - takie jak argumenty funkcji ```download_input```





