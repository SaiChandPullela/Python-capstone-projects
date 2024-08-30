from turtle import Turtle

class WriteName(Turtle):

    def __init__(self, x, y, name):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.x = x
        self.y = y
        self.name = name
        self.write_city_name()


    def write_city_name(self):
        self.goto(self.x, self.y)
        self.write(self.name)
# import pandas as pd
#
# states_data = pd.read_csv('50_states.csv')
# states = (states_data['state']).values
#
# choice = input('enter')
# if choice in states:
#     print('yes')
# else:
#     print('no')

