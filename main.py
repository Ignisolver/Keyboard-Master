import tkinter as tk

from GameMenu import GameMenu
from GameScreen import GameScreen
from LoadGame import LoadGame
from NewGame import NewGame

LARGE_FONT = ("Verdana", 12)


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        # fullscreen
        self.overrideredirect(True)
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # wczytanie wszystkich ramek do krotki
        for F in (GameMenu, NewGame, LoadGame, GameScreen):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(GameMenu)

    # metoda podnosząca wybraną ramkę
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# start aplikacji
app = Application()
app.mainloop()
