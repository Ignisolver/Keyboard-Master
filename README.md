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
            # print(el[1])
            cu.execute(
                "INSERT INTO " + playerdb + "_stat_week (\"score\", \"date\") VALUES (" + str(el[0]) + ", \"" + str(
                    el[1]) + "\")")
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
    size_y = 650
    pygame.display.set_caption("Miszcz Klawiatury")
    icon = pygame.image.load('klawiatura.png')
    pygame.display.set_icon(icon)
    screen.fill((255, 255, 255))
```
Funkcja odpowiada za utworzenie okna, w którym będą wyświetlane wybrane ramki.

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

## ```Statistics.py```

### ```download_input(period, nick)```

```python
    period_dict = {1: "today", 2: "week", 3: "month", 4: "ever"}
    period_dict_d = {1: 500, 2: 7, 3: 30, 4: 666}
    period_scores = None
    cu.execute(
        "select rowid, date, score from " + nick + "_stat_" + period_dict[period] + " ORDER BY \"date\" DESC LIMIT ?",
        (str(period_dict_d[period])))
    cx.commit()
    period_scores = cu.fetchall()
    return period_scores
```

```download_input()``` służy do pobierania z bazy danych wyników dla dowolnego gracza za wybrany okres (dzień, tydzień, miesiąc, od początku), wymaga ona podania jako argumentów nicku gracza oraz wartości liczbowej przypisanej danemu okresowi. Jakie są to wartości, widać w pierwszej linii.

## ```Login.py```

Tu zawarta została mechanika logowania, oraz inicjalizacji nowego gracza.

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
