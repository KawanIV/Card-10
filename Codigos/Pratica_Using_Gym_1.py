# importando bibliotecas
import gymnasium as gym
import random
from IPython.display import clear_output
from time import sleep
import numpy as np
from gymnasium.envs.toy_text import taxi
from gymnasium import Env

# Patch de compatibilidade para versões novas do NumPy
if not hasattr(np, "bool8"):
    np.bool8 = np.bool_  # cria um alias com o nome antigo

random.seed(1234)

# Grid personalizado com renderização customizada
class GridMaiorEnv(Env):
    metadata = {'render.modes': ['human', 'ansi', 'rgb_array'], "render_fps": 4}
    
    def __init__(self, render_mode=None):
        super().__init__()
        
        # Grid 11x11
        self.desc = np.array([
            [b"+", b"-", b"-", b"-", b"-", b"-", b"-", b"-", b"-", b"-", b"+"],
            [b"|", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b"|"],
            [b"|", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b"|"],
            [b"|", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b"|"],
            [b"|", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b"|"],
            [b"|", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b"|"],
            [b"|", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b"|"],
            [b"|", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b"|"],
            [b"|", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b"|"],
            [b"|", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b" ", b"|"],
            [b"+", b"-", b"-", b"-", b"-", b"-", b"-", b"-", b"-", b"-", b"+"]
        ], dtype='c')
        
        # Novas posições
        self.locs = [(1, 1), (9, 9)]
        
        # Ações: 0=south, 1=north, 2=east, 3=west, 4=pickup, 5=dropoff
        self.action_space = gym.spaces.Discrete(6)
        
        # Estados
        num_rows, num_cols = self.desc.shape
        self.num_states = num_rows * num_cols * len(self.locs) * len(self.locs)
        self.observation_space = gym.spaces.Discrete(self.num_states)
        
        # Render mode
        self.render_mode = render_mode
        self.window = None
        
        # Reset inicial
        self.reset()
    
    def encode(self, taxi_row, taxi_col, pass_loc, dest_idx):
        # Codificar estado similar ao Taxi original
        i = taxi_row
        i *= self.desc.shape[1]
        i += taxi_col
        i *= len(self.locs)
        i += pass_loc
        i *= len(self.locs)
        i += dest_idx
        return i
    
    def decode(self, i):
        # Decodificar estado
        out = []
        out.append(i % len(self.locs))
        i = i // len(self.locs)
        out.append(i % len(self.locs))
        i = i // len(self.locs)
        out.append(i % self.desc.shape[1])
        i = i // self.desc.shape[1]
        out.append(i)
        assert 0 <= i < self.desc.shape[0]
        return reversed(out)
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        # Estado inicial: taxi no centro, passageiro no pickup, destino 0
        taxi_row, taxi_col = 5, 5
        pass_loc = 0  # no pickup
        dest_idx = 0  # destino no dropoff 0
        
        self.state = self.encode(taxi_row, taxi_col, pass_loc, dest_idx)
        self.taxi_row, self.taxi_col, self.pass_loc, self.dest_idx = taxi_row, taxi_col, pass_loc, dest_idx
        
        if self.render_mode == "human":
            self.render()
            
        return self.state, {}
    
    def step(self, action):
        taxi_row, taxi_col, pass_loc, dest_idx = self.decode(self.state)
        reward = -1  # penalidade por passo
        terminated = False
        truncated = False
        info = {}
        
        # Movimentos
        if action == 0:  # south
            taxi_row = min(taxi_row + 1, self.desc.shape[0] - 2)
        elif action == 1:  # north
            taxi_row = max(taxi_row - 1, 1)
        elif action == 2:  # east
            taxi_col = min(taxi_col + 1, self.desc.shape[1] - 2)
        elif action == 3:  # west
            taxi_col = max(taxi_col - 1, 1)
        elif action == 4:  # pickup
            if pass_loc == 0 and (taxi_row, taxi_col) == self.locs[0]:
                pass_loc = 1  # passageiro no taxi
                reward = -1
            else:
                reward = -10
        elif action == 5:  # dropoff
            if pass_loc == 1 and (taxi_row, taxi_col) == self.locs[dest_idx]:
                terminated = True
                reward = 20
            else:
                reward = -10
        
        # Atualizar estado
        self.state = self.encode(taxi_row, taxi_col, pass_loc, dest_idx)
        self.taxi_row, self.taxi_col, self.pass_loc, self.dest_idx = taxi_row, taxi_col, pass_loc, dest_idx
        
        if self.render_mode == "human":
            self.render()
            
        return self.state, reward, terminated, truncated, info
    
    def render(self):
        if self.render_mode is None:
            return
        
        # Renderização ANSI (para texto)
        if self.render_mode == "ansi":
            output = []
            for i, row in enumerate(self.desc):
                line = []
                for j, cell in enumerate(row):
                    if (i, j) == (self.taxi_row, self.taxi_col):
                        if self.pass_loc == 1:  # passageiro no taxi
                            line.append("T")
                        else:
                            line.append("▣")
                    elif (i, j) == self.locs[0]:  # pickup
                        line.append("P")
                    elif (i, j) == self.locs[1]:  # dropoff
                        line.append("D")
                    else:
                        line.append(cell.decode())
                output.append("".join(line))
            return "\n".join(output)
        
        # Renderização humana (usando print)
        elif self.render_mode == "human":
            clear_output(wait=True)
            print("=" * 50)
            print("TAXI EM GRID MAIOR (11x11)")
            print("=" * 50)
            
            for i, row in enumerate(self.desc):
                line = []
                for j, cell in enumerate(row):
                    if (i, j) == (self.taxi_row, self.taxi_col):
                        if self.pass_loc == 1:
                            line.append("🚕")  # taxi com passageiro
                        else:
                            line.append("🚕")  # taxi vazio
                    elif (i, j) == self.locs[0]:
                        line.append("🏁")  # pickup
                    elif (i, j) == self.locs[1]:
                        line.append("🎯")  # dropoff
                    else:
                        line.append(cell.decode())
                print(" ".join(line))
            
            print(f"Passageiro: {'no taxi' if self.pass_loc == 1 else 'no pickup'}")
            print(f"Destino: {self.locs[self.dest_idx]}")
            print("=" * 50)
    
    def close(self):
        if self.window is not None:
            pass

# Registrar ambiente
try:
    gym.register(
        id='TaxiMaior-v0',
        entry_point='__main__:GridMaiorEnv',
    )
except:
    pass

# Ambiente para treinamento (modo ansi)
streets_train = gym.make('TaxiMaior-v0', render_mode="ansi")
state, info = streets_train.reset(seed=1234)

print("GRID MAIOR - VISUALIZAÇÃO:")
print(streets_train.render())
print(f"Estado inicial: {state}")
print(f"Número de estados: {streets_train.observation_space.n}")

# Q-learning
q_table = np.zeros([streets_train.observation_space.n, streets_train.action_space.n])
learning_rate = 0.1
discount_factor = 0.6
exploration = 0.1
epochs = 10000

print(f"\nINICIANDO TREINAMENTO:")
print(f"Tabela Q shape: {q_table.shape}")
print(f"Épocas: {epochs}")

for taxi_run in range(epochs):
    state, info = streets_train.reset()
    done = False
    truncated = False
    
    while not done and not truncated:
        if random.random() < exploration:
            action = streets_train.action_space.sample()
        else:
            action = int(np.argmax(q_table[state]))

        next_state, reward, done, truncated, info = streets_train.step(action)

        prev_q = q_table[state, action]
        next_max_q = np.max(q_table[next_state])
        q_table[state, action] = (1 - learning_rate) * prev_q + learning_rate * (reward + discount_factor * next_max_q)

        state = next_state

    if (taxi_run + 1) % 1000 == 0:
        print(f"Época {taxi_run + 1}/{epochs} concluída")

# Execução com visualização humana
print("\nEXECUTANDO COM VISUALIZAÇÃO HUMANA:")
streets_human = gym.make('TaxiMaior-v0', render_mode="human")

for tripnum in range(1, 6):  # reduzindo para 5 trips para demonstração
    state, info = streets_human.reset()
    done = False
    truncated = False
    step_count = 0
    max_steps = 50
    
    while not done and not truncated and step_count < max_steps:
        action = int(np.argmax(q_table[state]))
        next_state, reward, done, truncated, info = streets_human.step(action)
        
        sleep(0.5)
        state = next_state
        step_count += 1

    print(f"Trip {tripnum}: {'completo' if done else 'timeout'} em {step_count} passos")
    sleep(2.0)

streets_human.close()
