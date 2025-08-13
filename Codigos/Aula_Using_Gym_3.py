# importando bibliotecas
import gym
import random
from IPython.display import clear_output
from time import sleep
import numpy as np

# Patch de compatibilidade para versões novas do NumPy
if not hasattr(np, "bool8"):
    np.bool8 = np.bool_  # cria um alias com o nome antigo

random.seed(1234)

# 1) Não use .env aqui; preserve os wrappers do Gym v3
streets = gym.make("Taxi-v3", render_mode="ansi")

# 2) SEMPRE reset antes de render/step
state, info = streets.reset(seed=1234)
print(streets.render())

# 3) Para mexer em atributos específicos do ambiente base, use .unwrapped
initial_state = streets.unwrapped.encode(2, 3, 2, 0)
streets.unwrapped.s = initial_state
print(streets.render())

# Se quiser inspecionar a dinâmica
_ = streets.unwrapped.P[initial_state]

# Q-learning
q_table = np.zeros([streets.observation_space.n, streets.action_space.n])
learning_rate = 0.1
discount_factor = 0.6
exploration = 0.1
epochs = 10000

for taxi_run in range(epochs):
    state, _ = streets.reset()
    done = False
    while not done:
        if random.random() < exploration:
            action = streets.action_space.sample()
        else:
            action = int(np.argmax(q_table[state]))

        next_state, reward, terminated, truncated, info = streets.step(action)
        done = terminated or truncated

        prev_q = q_table[state, action]
        next_max_q = np.max(q_table[next_state])
        q_table[state, action] = (1 - learning_rate) * prev_q + learning_rate * (reward + discount_factor * next_max_q)

        state = next_state

print(q_table[initial_state])

# Execução da política aprendida
for tripnum in range(1, 11):
    state, _ = streets.reset()
    done = False
    while not done:
        action = int(np.argmax(q_table[state]))  # (corrige bug comum: era np.argmax(q_table))
        next_state, reward, terminated, truncated, info = streets.step(action)
        done = terminated or truncated

        clear_output(wait=True)
        print(f"Trip number {tripnum}")
        print(streets.render())
        sleep(0.5)

        state = next_state

    sleep(1.5)
