import tkinter as tk

LARGE_FONT = ("Verdana", 12)


class NewGame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Nowa gra", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

    # TODO: trzeba zrobić form na dane gracza i wybór poziomu trudności, no i pomyśleć nad ramką samej gry
