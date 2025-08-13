print('hello world')

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

streets = gym.make("Taxi-v3", render_mode='ansi').env
streets.reset()

initial_state = streets.encode(2, 3, 2, 0)
streets.s = initial_state
print(streets.render())
print(streets.P[initial_state])

# Q-table inicial
q_table = np.zeros([streets.observation_space.n, streets.action_space.n])

learning_rate = 0.1
discount_factor = 0.6
exploration = 0.1
epochs = 500000  # Aumentado para realmente treinar

# Treinamento
for taxi_run in range(epochs):
    state = streets.reset()
    if isinstance(state, tuple):
        state = state[0]
    state = int(state)
    
    done = False
    
    while not done:
        if random.uniform(0, 1) < exploration:
            action = streets.action_space.sample()
        else:
            action = np.argmax(q_table[state])
            
        step_result = streets.step(action)
        next_state = step_result[0]
        reward = step_result[1]
        done = step_result[2] if len(step_result) > 2 else False
        
        prev_q = q_table[state, action]
        next_max_q = np.max(q_table[int(next_state)])
        new_q = (1 - learning_rate) * prev_q + learning_rate * (reward + discount_factor * next_max_q)
        q_table[state, action] = new_q
        
        state = int(next_state)

print(q_table[initial_state])

# Fase de teste
for tripnum in range(1, 11):
	state = streets.reset()
	if isinstance(state, tuple):
		state = state[0]
	state = int(state)
	
	done = False
	step_count = 0
	max_steps = 100  # limite de passos para evitar loop infinito
	actions_taken = []  # Armazena as ações da viagem
	
	while not done and step_count < max_steps:
		action = np.argmax(q_table[state])
		actions_taken.append(action)  # Guarda a ação
		
		step_result = streets.step(action)
		if len(step_result) == 5:
			next_state, reward, terminated, truncated, info = step_result
			done = bool(terminated or truncated)
		else:
			next_state, reward, done, info = step_result
			done = bool(done)
	
		if isinstance(next_state, tuple):
			next_state = next_state[0]
		next_state = int(next_state)
	
		clear_output(wait=True)
		print("Trip number " + str(tripnum))
		sleep(.5)
	
		state = next_state
		step_count += 1
	
	sleep(1)
    
	# === Reprodução da viagem no modo gráfico ===
	np.random.seed(1234)
	print(f"\n=== Reproduzindo viagem {tripnum} ===\n")
	replay_env = gym.make("Taxi-v3", render_mode='human').env
	
	# --- Alteração crítica --- #
	replay_env.reset()  # OBRIGATÓRIO para o PyGame (mas aleatoriza o estado)
	replay_env.s = initial_state  # SOBRESCREVE o estado aleatório com o seu estado fixo
	# ------------------------ #
	
	for action in actions_taken:
		replay_env.step(action)
		sleep(0.5)  # velocidade da reprodução
	
	replay_env.close()

