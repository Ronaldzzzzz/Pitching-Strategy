from tkinter import * 
from PIL import ImageTk
from experta.fact import Fact
import main

introduction = "Hello! This is an expert system that to help you to select the pitching strategy based on the situation!\n"
introduction += "Please click the image/button/radio button to tell me the information I need, and then clike \"Recommend!\" button.\n"
introduction += "NOTE: Please pretent all the batters are Right-Handed Hitter."

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

def chase_value():
    print(var.get())

def execute():
    engine.reset()
    engine.declare(Fact(outs=1))
    engine.declare(Fact(strikes=2))
    engine.declare(Fact(balls=3))

    engine.declare(Fact(batter_order=9))

    engine.declare(Fact(late_innings = 'yes'))

    engine.declare(Fact(our_scored=0))
    engine.declare(Fact(rival_scored=5))

    engine.declare(Fact(batter_chased='no'))

    engine.declare(Fact(runner_1='no'))
    engine.declare(Fact(runner_2='no'))
    engine.declare(Fact(runner_3='no'))
    
    engine.declare(Fact(pitching_accuracy=10))
    engine.run()
    pitching, pitching_json = engine.printPitching()
    print(pitching)
    description.delete("1.0", "end")
    description.insert(END, pitching_json)


root = Tk(className=' - Pitcher Expert -')
root.geometry("900x700")
#root.resizable(height = 0, width = 0)

# for Radio button
var = IntVar()
var.set(1)

pitch_position = [[(30, 30), (45, 40), (125, 40), (210, 40), (220, 25)],
                  [(30, 120), (45, 120), (125, 125), (200, 120), (220, 120)],
                  [(35, 210), (45, 210), (125, 220), (210, 210), (220, 210)]]

font_format = ("Consolas Bold", 15)

# -----------------------------------------------------------
# Icons made by Freepik from https://www.flaticon.com/
# -----------------------------------------------------------

Home_Base_icon = PhotoImage(file = "img/homebase.png") 
Base_icon = PhotoImage(file = "img/base.png") 
Runner_icon = PhotoImage(file = "img/runner.png") 
None_icon = PhotoImage(file = "img/none.png")
Ball_icon = PhotoImage(file = "img/ball.png")
Strike_icon = PhotoImage(file = "img/strike.png")
Out_icon = PhotoImage(file = "img/out.png")
zone = PhotoImage(file = "img/zone.png")
batter = PhotoImage(file = "img/batter.png")
baseball = PhotoImage(file = "img/baseball.png")
baseball2 = ImageTk.PhotoImage(file="img/baseball.png")

# -----------------------------------------------------------
# Base area layout
# -----------------------------------------------------------
button_First_Base = Button(root, image = Base_icon, command = first_base_runner)
button_First_Base.place(x = 300, y = 165)

button_Second_Base = Button(root, image = Base_icon, command = second_base_runner)
button_Second_Base.place(x = 165, y = 30)

button_Third_Base = Button(root, image = Base_icon, command = third_base_runner)
button_Third_Base.place(x = 30, y = 165)

button_Home_Base = Label(root, image = Home_Base_icon)
button_Home_Base.place(x = 165, y = 300)
button_Home_Base = Button(root, text = "Recommend!", font=("Consolas Bold", 13), fg = "firebrick1", command = execute)
button_Home_Base.place(x = 710, y = 400)

label_pitcher_accuracy = Label(root, text = "Pitcher \nAccuracy:", font = font_format)
label_pitcher_accuracy.place(x = 180, y = 190)
pitcher_accuracy = Scale(root, from_ = 1, to = 10, orient=HORIZONTAL, length = 120, font = font_format)
pitcher_accuracy.place(x = 170, y = 240)

label_rival_score = Label(root, text = "Rival Score:", font = font_format)
label_rival_score.place(x = 25, y = 310)
rival_score = Spinbox(root, from_ = 0, to = 20, width = 3 ,font = font_format)
rival_score.place(x = 65, y = 340)

label_our_score = Label(root, text = "Our Score:", font = font_format)
label_our_score.place(x = 310, y = 310)
our_score = Spinbox(root, from_ = 0, to = 20, width = 3 ,font = font_format)
our_score.place(x = 345, y = 340)

# -----------------------------------------------------------
# Batter Info layout
# -----------------------------------------------------------
label_batter_order = Label(root, text = "Batter Order:", font = font_format)
label_batter_order.place(x = 450, y = 30)
order = Spinbox(root, from_ = 1, to = 9, width = 3, font = font_format)
order.place(x = 620, y = 30)

label_batter_chase = Label(root, text = "How's this batter?", font = font_format)
label_batter_chase.place(x = 450, y = 90)
chase1 = Radiobutton(root, text = "Disciplined", variable = var, value = 1, font = font_format, command = chase_value)
chase1.place(x = 450, y = 120)
chase2 = Radiobutton(root, text = "Chase Last Pitching", variable = var, value = 2, font = font_format, command = chase_value)
chase2.place(x = 450, y = 150)

# -----------------------------------------------------------
# Ball/Strike layout
# -----------------------------------------------------------

label_inning = Label(root, text = "Inning:", font = font_format)
label_inning.place(x = 30, y = 450)
inning = Spinbox(root, from_ = 1, to = 20, width = 3, font = font_format)
inning.place(x = 140, y = 450)

label_balls = Label(root, text = "Ball:", font = font_format)
label_balls.place(x = 30, y = 500)
ball1 = Label(root, image = None_icon)
ball1.place(x = 140, y = 500)
ball2 = Label(root, image = None_icon)
ball2.place(x = 175, y = 500)
ball3 = Label(root, image = None_icon)
ball3.place(x = 210, y = 500)
ball = Spinbox(root,text = "ball" ,from_ = 0, to = 3, width = 2, font = font_format, command = ball_value)
ball.place(x = 260, y = 500)

label_strikes = Label(root, text = "Strike:", font=font_format)
label_strikes.place(x = 30, y = 550)
strike1 = Label(root, image = None_icon)
strike1.place(x = 140, y = 550)
strike2 = Label(root, image = None_icon)
strike2.place(x = 175, y = 550)
strike = Spinbox(root,text = "strike" ,from_ = 0, to = 20, width = 2, font = font_format, command = strike_value)
strike.place(x = 260, y = 550)

label_out = Label(root, text = "Out:", font=font_format)
label_out.place(x = 30, y = 600)
out1 = Label(root, image = None_icon)
out1.place(x = 140, y = 600)
out2 = Label(root, image = None_icon)
out2.place(x = 175, y = 600)
out = Spinbox(root,text = "out" ,from_ = 0, to = 20, width = 2, font = font_format, command = out_value)
out.place(x = 260, y = 600)

# -----------------------------------------------------------
# Result layout
# -----------------------------------------------------------

image_batter = Label(root, image = batter)
image_batter.place(x = 700, y = 240)

image_baseball = Label(root, image = baseball2)
image_baseball.place(x = 500, y = 250)

image_zone = Canvas(root, width = 250, height = 250)
image_zone.place(x = 450, y = 200)
image_zone.create_image(125, 125, image=zone)
image_zone.create_image(pitch_position[1][2], image=baseball2)

description = Text(root, height = 9, width = 43, font = font_format, wrap = WORD)
description.place(x = 370, y = 450)
description.insert(END, introduction)


engine = main.PitchingStrategy()
root.mainloop()
