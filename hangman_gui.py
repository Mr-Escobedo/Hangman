#Author: Kevin C. Escobedo
#Email: escobedo001@gmail.com
from hangman_logic import HangmanGame
import tkinter
import os
import sys

class HangmanGUI:
    def __init__(self):
        self.root_window = tkinter.Tk()
        self.root_window.configure(background = "white")
        self.root_window.geometry("300x250")
        self.root_window.title("Hangman")
        self.root_window.resizable(0,0)
        self.root_window.iconbitmap(self.resource_path("hangman_icon.ico"))
        self.enter_letter = tkinter.Entry(self.root_window, width = 6)
        self.game = HangmanGame(word_bank = self.resource_path("Words/other_words.txt"))
        self.past_letters = tkinter.StringVar()
        self.lines = tkinter.StringVar()
        self.error_message = tkinter.StringVar()
        self.show_pic = tkinter.Label(self.root_window)

    def resource_path(self, relative_path):
        '''Get absolute path to resource, works for dev and for PyInstaller'''
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def check_not_game_over(self):
        '''Checks if the game is over'''
        return self.game.tries > 0 and self.game.num_letter != 0

    def get_the_guess(self):
        '''Gets the guess from the Entry box'''
        try:
            guess = self.enter_letter.get()
            if not guess.isalpha():
                raise TypeError
            if len(guess) != 1:
                raise ValueError
            if guess in self.game.guessed_letters:
                raise IndexError
            self.enter_letter.delete(0, tkinter.END)
            return guess.upper()
        except TypeError:
            self.error_message.set("ERROR: Entry not a letter")
        except ValueError:
            self.error_message.set("ERROR: Entry must be single letter")
        except IndexError:
            self.error_message.set("ERROR: Entry already guessed")
                


    def check_guess(self):
        '''Checks if the guessed letter is in the word'''
        if self.check_not_game_over():
            guess = self.get_the_guess()
            try:
                self.game.update_game(guess)
                self.error_message.set("")
                img = tkinter.PhotoImage(file = self.resource_path("States/hangman_{}.gif".format(self.game.tries)))
                self.show_pic.configure(image = img)
                self.show_pic.image = img
            except TypeError:
                pass
            if len(self.game.guessed_letters) > 0:
                self.past_letters.set(self.show_past_letters())
            self.lines.set(self.game.show_lines)
            if self.game.tries == 0:
                self.lines.set(self.game.word)
                self.error_message.set("Game Over")
        else:
            self.lines.set(self.game.word)
            self.error_message.set("Game Over")

    def key(self, event):
        '''Handles keyboard input'''
        if event.keysym == "Return":
            self.check_guess()

    def show_past_letters(self):
        '''Gets the guessed letters from the set'''
        past_string = ""
        temp_list = list(self.game.guessed_letters)
        for letter in temp_list:
            past_string += " {} ".format(letter)
        return past_string.strip()

    def run(self):
        tkinter.Label(self.root_window, textvariable = self.lines, background = "white").pack()
        self.enter_letter.pack()

        guess_button = tkinter.Button(self.root_window, text = "Guess",  command = self.check_guess)
        guess_button.pack()

        tkinter.Label(self.root_window, textvariable = self.past_letters, background = "white").pack()

        img = tkinter.PhotoImage(file = self.resource_path("States/hangman_{}.gif".format(self.game.tries)))

        self.show_pic.configure(image = img)
    
        self.show_pic.pack()

        tkinter.Label(self.root_window, textvariable = self.error_message, background = "white").pack()


        if len(self.game.guessed_letters) > 0:
            self.past_letters.set(self.show_past_letters())

        self.lines.set(self.game.show_lines)

        self.root_window.bind("<KeyPress>", self.key)

        self.root_window.mainloop()


if __name__ == "__main__":
    HangmanGUI().run()
