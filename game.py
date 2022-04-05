from tkinter import *
from words import words_clean
import random
import math


class Game:
    def __init__(self):
        self.words_to_guess = 30
        self.countdown_timer = None
        self.words = []
        self.cur_word_index = 0
        self.cur_word = ""
        self.timer = None
        self.time_seconds = 0
        self.time_formatted = ""
        self.words_per_minute = 0
        self.game_is_on = False

        # GUI
        self.window = Tk()
        self.window.title("Test your typing speed!")
        self.window.config(padx=20, pady=20)
        # labels
        self.rules_label = Label(
            text="Click start and type the words that appear as fast as you can.\n You will have a list of 30 "
                 "words to guess.\n Careful, only words spelt correctly will count.")
        self.rules_label.grid(row=0, column=0, pady=20)

        self.get_ready_label = Label(text="Get Ready!", font=("Arial", 30))
        self.get_ready_label.grid(column=0, row=2)

        self.time_label = Label(text="Time: 00:00")
        self.time_label.grid(column=0, row=4)

        # button
        self.start_button = Button(text="Get Started!", command=self.start_game)
        self.start_button.grid(column=0, row=1, pady=20)

        # entry
        self.new_entry = Entry(width=20)
        # new_entry.focus_set()
        self.new_entry.bind("<KeyRelease>", self.check_entry)
        self.new_entry.grid(column=0, row=3, pady=20)

    def start_game(self):
        for _ in range(self.words_to_guess):
            self.words.append(random.choice(words_clean))
        print(self.words)
        self.cur_word = self.words[self.cur_word_index]
        self.game_is_on = True
        self.begin_countdown(3)

    def begin_countdown(self, count):
        if count == 0:
            self.get_ready_label["text"] = self.cur_word
            self.start_timer()
        else:
            self.get_ready_label["text"] = count
        self.countdown_timer = self.window.after(1000, self.begin_countdown, count - 1)

    def start_timer(self):
        self.window.after_cancel(self.countdown_timer)
        self.time_seconds += 1
        minutes = math.floor(self.time_seconds / 60)
        seconds = self.time_seconds % 60
        if seconds < 10:
            seconds = f"0{seconds}"
        self.time_formatted = f"{minutes}:{seconds}"
        self.time_label["text"] = f"Time: {self.time_formatted}"
        self.timer = self.window.after(1000, self.start_timer)

    def check_entry(self, event):
        if self.new_entry.get() == self.cur_word:
            self.new_word()

    def new_word(self):
        if self.cur_word_index == len(self.words) - 1:
            self.end_game()
        else:
            self.cur_word_index += 1
            self.cur_word = self.words[self.cur_word_index]
            self.get_ready_label["text"] = self.cur_word
            self.new_entry.delete(0, END)
            self.new_entry.focus()

    def end_game(self):
        print("Game is finished")
        self.game_is_on = False
        self.window.after_cancel(self.timer)
        self.words_per_minute = round((self.words_to_guess / self.time_seconds) * 60)
        self.new_entry.delete(0, END)
        self.new_entry.focus()
        self.time_label["text"] = f"Congrats, you have found {self.words_to_guess} words in {self.time_formatted}.\n" \
                                  f" Your typing speed is {self.words_per_minute} words per minute."
        self.reset_game()

    def reset_game(self):
        self.get_ready_label["text"] = "Get Ready!"
        self.time_seconds = 0
        self.cur_word_index = 0
        self.words = []
