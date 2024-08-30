import pandas as pd, turtle

states_data = pd.read_csv('50_states.csv')
states = (states_data['state']).values

x_values= states_data['x']
y_values = states_data['y']

guessed_states = ['Texas', 'Alaska', 'Utah', 'Iowa']

for state in states_data.state:
    if state not in guessed_states:
        print(states_data['state'])