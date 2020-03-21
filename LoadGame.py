import tkinter as tk


class LoadGame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Załaduj grę", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
