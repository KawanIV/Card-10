import gymnasium as gym
import numpy as np

# Criar ambiente para treino (ansi = mais rápido)
env = gym.make("FrozenLake-v1", map_name="8x8", is_slippery=False, render_mode="ansi")

# Q-learning
q_table = np.zeros([64, 4])  # 16 estados, 4 ações
alpha = 0.1   # taxa de aprendizado
gamma = 0.1   # fator de desconto
epsilon = 0.9 # exploração

# Treinar
print("Treinando...")
for episode in range(10000):
    state, _ = env.reset()
    done = False
    
    while not done:
        # Escolher ação
        if np.random.random() < epsilon:
            action = env.action_space.sample()  # ação aleatória
        else:
            action = np.argmax(q_table[state])  # melhor ação
            
        # Executar ação
        next_state, reward, done, _, _ = env.step(action)
        
        # Atualizar Q-table
        q_table[state, action] = (1 - alpha) * q_table[state, action] + \
                                alpha * (reward + gamma * np.max(q_table[next_state]))
        
        state = next_state

print("Treino completo!")

# Testar
env_test = gym.make("FrozenLake-v1", map_name="8x8", is_slippery=False, render_mode="human")

state, _ = env_test.reset()
done = False
steps = 0

print("Executando política aprendida:")
while not done and steps < 20:
    action = np.argmax(q_table[state])
    state, reward, done, _, _ = env_test.step(action)
    steps += 1
    
    if done:
        if reward > 0:
            print("✅ Chegou no objetivo!")
        else:
            print("❌ Caiu no buraco!")
    else:
        print(f"Passo {steps}")

env.close()
env_test.close()
