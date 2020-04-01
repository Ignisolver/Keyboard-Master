# Mistrz Klawiatury

## Wstęp

Mistrz klawiatury to gra polegająca na przepisywaniu wyświetlanych wyrazów w jak najkrótszym czasie.

## Uruchomienie

Aby włączyć grę, należy w głównym katalogu projektu wykonać następujący skrypt:

```bash
main.py
```

## Struktura aplikacji

### ``` main.py ```

W pliku ``` main.py ``` zostałą zdefiniowana klasa ``` Application ```, która odpowiada za wczytanie wszystkich ramek programu (aplikacja wykorzystuje moduł GUI TkInter. Odbywa się to w następującej pętli:

```python
        for F in (GameMenu, NewGame, LoadGame, GameScreen):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
```
