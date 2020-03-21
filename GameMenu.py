import tkinter as tk


class GameMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Menu główne", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Nowy gracz",
                            command=lambda: controller.show_frame("NewGame"))
        button2 = tk.Button(self, text="Załaduj grę",
                            command=lambda: controller.show_frame("LoadGame"))
        button1.pack()
        button2.pack()
