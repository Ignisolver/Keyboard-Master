# Mistrz Klawiatury

## Wstęp

Mistrz klawiatury to gra polegająca na przepisywaniu wyświetlanych wyrazów w jak najkrótszym czasie.

## Uruchomienie

Aby włączyć grę, należy w głównym katalogu projektu wykonać następujący skrypt:

```bash
main.py
```

## Struktura aplikacji

### ```main.py```

W pliku ```main.py``` zostałą zdefiniowana klasa ```Application```, która odpowiada za wczytanie wszystkich ramek programu (aplikacja wykorzystuje moduł GUI TkInter. Odbywa się to w następującej pętli:

```python
for F in (GameMenu, NewGame, LoadGame, GameScreen):
        frame = F(container, self)

        self.frames[F] = frame

        frame.grid(row=0, column=0, sticky="nsew")
```

Metoda w klasie ```Application``` o nazwie ```show_frame()``` służy do podnoszenia wybranej ramki na wierzch aplikacji.

```python
def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
```

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
