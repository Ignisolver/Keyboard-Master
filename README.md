# Mistrz Klawiatury

## Wstęp

Mistrz klawiatury to gra polegająca na przepisywaniu wyświetlanych wyrazów w jak najkrótszym czasie.

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
Funkcja ```do_order_in_database``` pobiera z tabeli ```<player>_stat_today``` wyniki, następnie grupuje je po dacie a wyniki sumuje, po czym wstawia je do tabeli ```<player>_stat_week```, a w końcu stosuje polecienie ``` DELETE``` to wyczyszczenia zawartości pierwszej z tabel. Dzieje się tak dla każdego gracza.

## ```window_maker()```

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

## ```main()```

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

### ```GameMenu.py```

W tej klasie zdefiniowano ramkę, która wczytywana jest zaraz po uruchomieniu aplikacji, wyposażone jest w przyciski służące do załadowania wcześniejszego stanu gry i do utworzenia nowego zapisu.

```python
class GameMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Mistrz Klawiatury", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Nowa gra",
                           command=lambda: controller.show_frame(NewGame)) # Przyciśnięcie spowoduje podniesienie ramki z kontrolkami
        button.pack()                                                      # do tworzenia nowego zapisu.

        button2 = tk.Button(self, text="Załaduj grę",
                            command=lambda: controller.show_frame(LoadGame))
        button2.pack()
```
