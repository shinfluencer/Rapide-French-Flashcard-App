import tkinter
import pandas
import random

# Constants
BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"

# Data
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
finally:
    french_words = data.French.to_list()
    english_words = data.English.to_list()

current_card = None

# Commands
def new_card():
    global current_card 
    
    french_word = random.choice(french_words)
    english_translation = english_words[french_words.index(french_word)]
    
    current_card = {
        "Term": french_word,
        "Translation": english_translation
    }
    
    next_card(current_card)
    

def next_card(card):
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(title_text, fill="black")
    canvas.itemconfig(word_text, fill="black")
    
    canvas.itemconfig(title_text, text="French")
    canvas.itemconfig(word_text, text=card["Term"])
    
    window.after(3000, flip_card, card["Translation"])

def flip_card(translation):
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=translation, fill="white")
    
def is_known():
    french_words.remove(current_card["Term"])
    english_words.remove(current_card["Translation"])

    new_card()
    
# UI Setup
window = tkinter.Tk()
window.title("Rapide")
ico = tkinter.PhotoImage(file="images/icon.png")
window.iconphoto(False, ico)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.resizable(width=False, height=False)

# Canvas
canvas = tkinter.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = tkinter.PhotoImage(file="images/card_front.png")
card_back = tkinter.PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front)
title_text = canvas.create_text(400, 150, text="Title", font=(FONT_NAME, 40, "italic"))
word_text = canvas.create_text(400, 263, text="Word", font=(FONT_NAME, 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Buttons

wrong_image = tkinter.PhotoImage(file="images/wrong.png")
wrong_button = tkinter.Button(image=wrong_image, highlightthickness=0, command=new_card)
wrong_button.grid(column=0, row=1)

right_image = tkinter.PhotoImage(file="images/right.png")
right_button = tkinter.Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

new_card()

window.mainloop()

# Saving Data
words_to_learn = {
    "French": french_words,
    "English": english_words
}

pandas.DataFrame(words_to_learn).to_csv("data/words_to_learn.csv")
