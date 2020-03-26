import tkinter as tk

# czcionka jako krotka
LARGE_FONT = ("Verdana", 12)


class LoadGame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Załąduj grę", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # TODO: Zaimplementować ładowanie stanu gry (proponuję z *.txt), do omówienia rodzaj zapisywanych statów
