import tkinter as tk


class NewGame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Menu główne")
        label.pack(side="top", fill="x", pady=10)
