from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"


# -------------------------- Generate a french Word ------------------------------- #
try:
    # try read the data from the french_words.csv if existing
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
    print(data)

to_learn = data.to_dict(orient="records")

current_card = None


def next_card():
    global current_card, timer_count
    window.after_cancel(timer_count)

    current_card = random.choice(to_learn)
    canvas.itemconfig(card_main, image=card_img)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word,
                      text=current_card["French"],
                      fill="black")
    timer_count = window.after(3000, func=english_card)


def is_known():
    global current_card
    to_learn.remove(current_card)
    # Create a copy of the French words, so that no words are lost
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    print(data)
    next_card()


def english_card():
    global current_card
    canvas.itemconfig(card_main, image=card_img2)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word,
                      text=current_card["English"],
                      fill="white")


window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

# Set the timer
timer_count = window.after(3000, func=next_card)

# Create two flashcards = French and English
canvas = Canvas(width=800, height=530, highlightthickness=0, bg=BACKGROUND_COLOR)
card_img = PhotoImage(file="./images/card_front.png")
card_img2 = PhotoImage(file="./images/card_back.png")
card_main = canvas.create_image(400, 263, image=card_img)
canvas.grid(columnspan=2, column=0, row=0)

# small text - French
card_title = canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
canvas.grid(columnspan=2, column=0, row=0)

# big text - French word
card_word = canvas.create_text(400, 263, font=("Ariel", 60, "italic"))
canvas.grid(columnspan=2, column=0, row=0)


# Create 2 Buttons - right and wrong
right_image = PhotoImage(file="./images/right.png")
right = Button(image=right_image, highlightthickness=0, bg=BACKGROUND_COLOR,
               border=0, activebackground=BACKGROUND_COLOR, command=is_known)
right.grid(column=1, row=1)

wrong_image = PhotoImage(file="./images/wrong.png")
wrong = Button(image=wrong_image, highlightthickness=0, bg=BACKGROUND_COLOR,
               border=0, activebackground=BACKGROUND_COLOR, command=next_card)
wrong.grid(column=0, row=1)


next_card()
window.mainloop()
