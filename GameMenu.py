import tkinter as tk

from LoadGame import LoadGame
from NewGame import NewGame

LARGE_FONT = ("Verdana", 12)


class GameMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Mistrz Klawiatury", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Nowa gra",
                           command=lambda: controller.show_frame(NewGame))
        button.pack()

        button2 = tk.Button(self, text="Załaduj grę",
                            command=lambda: controller.show_frame(LoadGame))
        button2.pack()
