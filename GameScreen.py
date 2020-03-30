import random
import tkinter as tk

import GameSession

LARGE_FONT = ("Verdana", 12)

# czcionka jako krotka
LARGE_FONT = ("Verdana", 12)

# lista plików ze słowami
levels = ['easy_words.txt', 'medium_words.txt', 'hard_words.txt']

# otwieranie pliku ze słowami
words_file = open(levels[GameSession.level], 'r')
words_list = words_file.readlines()


def get_word():
    word_number = random.randint(0, 24)
    word = words_list[word_number]
    return word


# TODO: Dużo pracy się tu szykuje...
class GameScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        word = get_word()
        # TODO: sprawdzic dlaczego wyrzuca wyrazy już w menu głównym :(
        word_label = tk.Label(text=word, font=LARGE_FONT)
        word_label.pack()
