from tkinter import * 
from PIL import ImageTk, Image

global first_base
global second_base
global third_base
first_base = False
second_base = False
third_base = False

def first_base_runner():
    global first_base
    if first_base:
        button_First_Base.configure(image = Base_icon)
        first_base = False
    else:
        button_First_Base.configure(image = Runner_icon)
        first_base = True


def second_base_runner():
    global second_base
    if second_base:
        button_Second_Base.configure(image = Base_icon)
        second_base = False
    else:
        button_Second_Base.configure(image = Runner_icon)
        second_base = True

def third_base_runner():
    global third_base
    if third_base:
        button_Third_Base.configure(image = Base_icon)
        third_base = False
    else:
        button_Third_Base.configure(image = Runner_icon)
        third_base = True

def ball_value():
    num = ball.get()
    if num == "0":
        ball1.configure(image = None_icon)
    if num == "1":
        ball1.configure(image = Ball_icon)
        ball2.configure(image = None_icon)
    if num == "2":
        ball2.configure(image = Ball_icon)
        ball3.configure(image = None_icon)
    if num == "3":
        ball3.configure(image = Ball_icon)

def strike_value():
    num = strike.get()
    if num == "0":
        strike1.configure(image = None_icon)
    if num == "1":
        strike1.configure(image = Strike_icon)
        strike2.configure(image = None_icon)
    if num == "2":
        strike2.configure(image = Strike_icon)


def out_value():
    num = out.get()
    if num == "0":
        out1.configure(image = None_icon)
    if num == "1":
        out1.configure(image = Out_icon)
        out2.configure(image = None_icon)
    if num == "2":
        out2.configure(image = Out_icon)



root = Tk(className=' - Pitcher Expert -')

root.geometry("800x700")
#root.resizable(height = 0, width = 0)

#---------------------------------------------
# Icons made by Freepik from https://www.flaticon.com/
#---------------------------------------------

Home_Base_icon = PhotoImage(file = "img/homebase.png") 
Base_icon = PhotoImage(file = "img/base.png") 
Runner_icon = PhotoImage(file = "img/runner.png") 
None_icon = PhotoImage(file = "img/none.png")
Ball_icon = PhotoImage(file = "img/ball.png")
Strike_icon = PhotoImage(file = "img/strike.png")
Out_icon = PhotoImage(file = "img/out.png")

button_First_Base = Button(root, image = Base_icon, command = first_base_runner)
button_First_Base.place(x = 300, y = 165)

button_Second_Base = Button(root, image = Base_icon, command = second_base_runner)
button_Second_Base.place(x = 165, y = 30)

button_Third_Base = Button(root, image = Base_icon, command = third_base_runner)
button_Third_Base.place(x = 30, y = 165)

button_Home_Base = Label(root, image = Home_Base_icon)
button_Home_Base.place(x = 165, y = 300)
button_Home_Base = Button(root, text = "Recommend!", font=("Consolas Bold", 13), fg = "firebrick1")
button_Home_Base.place(x = 178, y = 330)

label_pitcher_accuracy = Label(root, text = "Pitcher \nAccuracy:", font=("Consolas Bold", 15))
label_pitcher_accuracy.place(x = 180, y = 190)
pitcher_accuracy = Scale(root, from_ = 1, to = 10, orient=HORIZONTAL, length = 120, font=("Consolas Bold", 15))
pitcher_accuracy.place(x = 170, y = 240)

label_rival_score = Label(root, text = "Rival Score:", font=("Consolas Bold", 15))
label_rival_score.place(x = 25, y = 310)
rival_score = Spinbox(root, from_ = 0, to = 20, width = 3 ,font=("Consolas Bold", 15))
rival_score.place(x = 65, y = 340)

label_our_score = Label(root, text = "Our Score:", font=("Consolas Bold", 15))
label_our_score.place(x = 310, y = 310)
our_score = Spinbox(root, from_ = 0, to = 20, width = 3 ,font=("Consolas Bold", 15))
our_score.place(x = 345, y = 340)

# -----------------------------------------------------------



# -----------------------------------------------------------

label_inning = Label(root, text = "Inning:", font=("Consolas Bold", 15))
label_inning.place(x = 30, y = 450)
inning = Spinbox(root,text = "inning" ,from_ = 1, to = 20, width = 3, font = ("Consolas Bold", 15))
inning.place(x = 140, y = 450)

label_balls = Label(root, text = "Ball:", font=("Consolas Bold", 15))
label_balls.place(x = 30, y = 500)
ball1 = Label(root, image = None_icon)
ball1.place(x = 140, y = 500)
ball2 = Label(root, image = None_icon)
ball2.place(x = 175, y = 500)
ball3 = Label(root, image = None_icon)
ball3.place(x = 210, y = 500)
ball = Spinbox(root,text = "ball" ,from_ = 0, to = 3, width = 2, font = ("Consolas Bold", 15), command = ball_value)
ball.place(x = 260, y = 500)

label_strikes = Label(root, text = "Strike:", font=("Consolas Bold", 15))
label_strikes.place(x = 30, y = 550)
strike1 = Label(root, image = None_icon)
strike1.place(x = 140, y = 550)
strike2 = Label(root, image = None_icon)
strike2.place(x = 175, y = 550)
strike = Spinbox(root,text = "strike" ,from_ = 0, to = 20, width = 2, font = ("Consolas Bold", 15), command = strike_value)
strike.place(x = 260, y = 550)

label_out = Label(root, text = "Out:", font=("Consolas Bold", 15))
label_out.place(x = 30, y = 600)
out1 = Label(root, image = None_icon)
out1.place(x = 140, y = 600)
out2 = Label(root, image = None_icon)
out2.place(x = 175, y = 600)
out = Spinbox(root,text = "out" ,from_ = 0, to = 20, width = 2, font = ("Consolas Bold", 15), command = out_value)
out.place(x = 260, y = 600)



root.mainloop()