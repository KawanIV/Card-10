# importando bibliotecas
import gym
import random
import time
from IPython.display import clear_output
from time import sleep
import numpy as np

# Patch de compatibilidade para versões novas do NumPy
if not hasattr(np, "bool8"):
    np.bool8 = np.bool_  # cria um alias com o nome antigo

random.seed(1234)

streets = gym.make("Taxi-v2").env
streets.render()

initial_state = streets.encode(2,3,2,0)
streets.s = initial_state
streets.render()

streets.P[initial_state]

q_table = np.zeros([streets.observation_space.n,streets.action_space.n])
learning_rate = 0.1
discount_factor = 0.6
exploration = 0.1
epochs = 10000

for taxi_run in range(epochs):
	state = streets.reset()
	done = False
	while not done:
		random_value = random.uniform(0,1)
		if (random_value < exploration):
			action = streets.action_space.sample()
		else:
			action = np.argmax(q_table[state])
			
		next_state, reward, done, info = streets.step(action)
		
		prev_q = q_table[state, action]
		next_max_q = np.max(q_table[next_state])
		new_q = (1 - learning_rate)*prev_q + learning_rate * (reward + discount_factor * next_max_q)
		q_table[state, action] = new_q
		
		state = next_state
		
q_table[initial_state]

for tripnum in range(1,11):
	state = streets.reset()
	done = False
	
	while not done:
		action = np.argmax(q_table)
		next_state, reward, done, info = streets.step(action)
		clear_output(wait=True)
		print("Trip number" + str(tripnum))
		print(streets.render(mode='ansi'))
		sleep(.5)
		state = next_state
	
	sleep(2)  
