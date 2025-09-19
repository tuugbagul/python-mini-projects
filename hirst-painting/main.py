
from turtle import Turtle, Screen
import random
tim = Turtle()

screen = Screen()
screen.colormode(255)

color_list = [(219, 254, 237), (84, 254, 155), (173, 146, 118), (254, 250, 254), (245, 39, 191), (158, 107, 56), (2, 1, 176), (151, 54, 251), (221, 254, 101)]

tim.penup()
tim.hideturtle()
tim.goto(-200,-200)


tim.speed("fastest")

def motion():
    tim.left(90)
    tim.forward(50)
    tim.left(90)
    tim.forward(500)
    tim.right(180)

for _ in range(10):
    for i in range(10):
        tim.dot(20,random.choice(color_list))
        tim.penup()
        tim.forward(50)
    motion()


"""for y in range(10):
    for x in range(10):
        tim.dot(20, random.choice(color_list))
        tim.forward(50)
    tim.backward(500)  # Satır sonuna geldiğinde geri dön
    tim.sety(tim.ycor() + 50)  # Bir sonraki satıra geç"""










screen.exitonclick()