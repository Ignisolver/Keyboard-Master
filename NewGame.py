import json
import tkinter as tk

from Player import Player

LARGE_FONT = ("Verdana", 12)


class NewGame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Nowa gra", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        user_name = tk.Entry(self)
        user_name.pack()

        label_level = tk.Label(self, text='Wybierz poziom trudności', font=LARGE_FONT)
        label_level.pack()

        # radiobuttony
        level_choice = tk.IntVar()
        tk.Radiobutton(self, text='ŁATWY', variable=level_choice, value=1, indicatoron=0).pack()
        tk.Radiobutton(self, text='ŚREDNI', variable=level_choice, value=2, indicatoron=0).pack()
        tk.Radiobutton(self, text='TRUDNY', variable=level_choice, value=3, indicatoron=0).pack()

        def make_user():
            player = Player(user_name.get(), level_choice.get())
            with open('users.txt', 'a') as outfile:
                json.dump(player.__dict__, outfile)

        # guzik zapisu
        save_button = tk.Button(text='Zapisz', command=make_user)
        save_button.pack()
