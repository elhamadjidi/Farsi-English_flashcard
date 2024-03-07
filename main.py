import csv
from tkinter import *
# from tkinter import messagebox
import pandas
import secrets

BACKGROUND_COLOR = "#B1DDC6"
# --------------------------------change---------------------------


try:
    df = pandas.read_csv("data/words_to_remember.csv")
except FileNotFoundError:
    df = pandas.read_csv("data/farsi-english.csv")

dic_list = df.to_dict(orient="records")  # makes a list of dictionary of rows
# for the first time the list should be the original but when you start learning it should get updated and then you
# should see the updated csv file
random_word = {}  # the words are randomly selected to show to participant


def next_card():
    global random_word, flip_timer
    window.after_cancel(flip_timer)  # invalidate the timer, so it stops using the one it never stopped counting down on
    random_word = secrets.SystemRandom().choice(dic_list)
    canvas.itemconfig(title, text="Farsi", fill="black")  # to hold on to the text in canvas
    canvas.itemconfig(word, text=random_word["Farsi"], fill="black")
    canvas.itemconfig(canvas_image, image=front_pic)
    flip_timer = window.after(ms=3000, func=flip)  # set up a new timer so it can wait another 3 seconds


def update():
    dic_list.remove(random_word)
    updated_data = pandas.DataFrame(dic_list)  # make a dataframe of the list to add it to csv file easily
    updated_data.to_csv("data/words_to_remember.csv", index=False)
    next_card()


def flip():
    canvas.itemconfig(canvas_image, image=back_pic)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, fill="white", text=random_word["English"])


# --------------------------------UI--------------------------------


window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(ms=3000, func=flip)
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_pic = PhotoImage(file="images/card_front.png")
back_pic = PhotoImage(file="images/card_back.png")
right_pic = PhotoImage(file="images/right.png")
wrong_pic = PhotoImage(file="images/wrong.png")
canvas_image = canvas.create_image(400, 263, image=front_pic)  # starting x and y
canvas.grid(row=0, column=0, columnspan=2)
wrong_button = Button(image=wrong_pic, highlightthickness=0, command=next_card)
# it means that they know the current word on the flashcard
right_button = Button(image=right_pic, highlightthickness=0, command=update)
wrong_button.grid(row=1, column=0)
right_button.grid(row=1, column=1)
title = canvas.create_text(400, 150, text="Farsi", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="عشق", font=("Arial", 60, "bold"))
next_card()
window.mainloop()  # in the mainloop() you should not create additional delayed loops
# e.g. with time.sleep() but  instead, use window.after()
