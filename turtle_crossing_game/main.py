import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
car = CarManager()
scoreboard = Scoreboard()

screen.listen()

screen.onkey(player.move_player, "Up")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()

    car.create_car()
    car.move_car()

   #Detecting collision
    for single_car in car.all_cars:
       if player.distance(single_car) < 25:
           scoreboard.game_over()
           game_is_on = False

    if player.ycor() > 280:
        player.goto(0,-280)
        scoreboard.increase_score()
        car.increase_speed()

screen.exitonclick()

