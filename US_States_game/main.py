import turtle
import pandas as pd
from turtle import Turtle, Screen
from write import WriteName

screen = Screen()
image = "blank_states_img.gif"
screen.addshape(image)

turtle.shape(image)

states_data = pd.read_csv('50_states.csv')
states = (states_data['state']).values

x_values= states_data['x']
y_values = states_data['y']


game_is_on = True
guessed_states = []
while game_is_on:
    answer_state = screen.textinput(f"{len(guessed_states)}/"f"{len(states_data)} Guessed correctly",
                                    "What is another state?").title()
    if answer_state == 'Exit':
        missing_states = [state for state in states if state not in guessed_states]
        new_data = pd.DataFrame(missing_states)
        new_data.to_csv("states-to_learn.csv")
        break
    if answer_state in states:
        x = states_data.loc[states_data['state'] == answer_state, 'x'].values[0]
        y = states_data.loc[states_data['state'] == answer_state, 'y'].values[0]
        if answer_state not in guessed_states:
            guessed_states.append(answer_state)
            write = WriteName(x, y, answer_state)
        else:
            print(f"You already have guessed {answer_state}. Try guessing")
    else:
        print(f"{answer_state} is not one of the states in U.S. Guess another state")
    if len(guessed_states) == 50:
        game_is_on = False
        print(f'Congratulations! You have guessed {len(guessed_states)} out of {len(states)} states')


































