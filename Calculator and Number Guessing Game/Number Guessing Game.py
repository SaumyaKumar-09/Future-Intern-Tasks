import random
import tkinter as tk
from tkinter import font as tkfont

class NumberGuessingGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Number Guessing Game")
        self.master.geometry("300x300")  # Set an initial size, but allow resizing

        self.master.grid_columnconfigure(0, weight=1)
        for i in range(6):
            self.master.grid_rowconfigure(i, weight=1)

        self.custom_font = tkfont.Font(family="Helvetica", size=12)

        self.secret_number = random.randint(1, 100)
        self.attempts = 0

        self.label = tk.Label(master, text="Guess a number between 1 and 100:", font=self.custom_font, wraplength=250)
        self.label.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        self.entry = tk.Entry(master, font=self.custom_font)
        self.entry.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

        self.submit_button = tk.Button(master, text="Submit Guess", command=self.check_guess, font=self.custom_font)
        self.submit_button.grid(row=2, column=0, pady=5, padx=10, sticky="ew")

        self.result_label = tk.Label(master, text="", font=self.custom_font, wraplength=250)
        self.result_label.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")

        self.play_again_button = tk.Button(master, text="Play Again", command=self.new_game, font=self.custom_font, state=tk.DISABLED)
        self.play_again_button.grid(row=4, column=0, pady=5, padx=10, sticky="ew")

        self.quit_button = tk.Button(master, text="Quit", command=self.master.quit, font=self.custom_font)
        self.quit_button.grid(row=5, column=0, pady=5, padx=10, sticky="ew")

        # Bind the Configure event to update label wraplength
        self.master.bind("<Configure>", self.update_wraplength)

    def update_wraplength(self, event=None):
        # Update wraplength of labels when window is resized
        new_width = self.master.winfo_width() - 40  # Subtract some padding
        self.label.config(wraplength=new_width)
        self.result_label.config(wraplength=new_width)

    def check_guess(self):
        try:
            guess = int(self.entry.get())
            self.attempts += 1

            if guess < self.secret_number:
                result_text = f"Too low! Attempts: {self.attempts}"
            elif guess > self.secret_number:
                result_text = f"Too high! Attempts: {self.attempts}"
            else:
                result_text = f"Congratulations! You guessed the number {self.secret_number} in {self.attempts} attempts!"
                self.submit_button.config(state=tk.DISABLED)
                self.play_again_button.config(state=tk.NORMAL)

            self.result_label.config(text=result_text)

        except ValueError:
            self.result_label.config(text="Please enter a valid number")

        self.entry.delete(0, tk.END)

    def new_game(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.result_label.config(text="")
        self.entry.delete(0, tk.END)
        self.submit_button.config(state=tk.NORMAL)
        self.play_again_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()