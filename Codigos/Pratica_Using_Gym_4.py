# Importando Bibliotecas

import gymnasium as gym
import numpy as np
import time

# Criando ambiente ansi
env = gym.make("FrozenLake-v1", map_name="8x8", is_slippery=False)

# Tabela do qlearning para 8x8
tabela_q = np.zeros([64,4]) #8x8 = 64, 4 é que o personagem realiza 4 ações

# Variáveis
aprendizado = 0.3
desconto = 0.95
exploracao = 0.2
praticas = range(1500)


print("Iniciando o treinamento...")
# Treinamento
for treino in praticas:
	estado, _ = env.reset()
	feito = False
	#Enquanto feito for falso
	while not feito:
		# Ações...
		if np.random.random() < exploracao: # Se o numero randomico for menor que o numero de exploracao
			acao = env.action_space.sample() # Ação aleatório
		else:
			acao = np.argmax(tabela_q[estado]) # Ação é a melhor ação
			
		#Executar ação
		prox_estado, recompensa, feito, _, _ = env.step(acao)
		
		if feito and recompensa == 0:
			recompensa = -1  # Punição por cair no buraco
		elif not feito:
			recompensa = -0.01  # Pequena punição por demorar
		
		# Atualizando tabelaq
		tabela_q[estado, acao] = (1 - aprendizado)*tabela_q[estado, acao] + aprendizado*(recompensa + desconto*np.max(tabela_q[prox_estado]))
		
		estado = prox_estado
print("Treino completado...","Iniciando testes...")
#Testes

# mudar render para human e conseguir ver o resultado
envtest = gym.make("FrozenLake-v1",map_name="8x8",is_slippery=False, render_mode="human")
estado, _ = envtest.reset()
feito = False
passos = 0

while not feito and passos < 20:
	acao = np.argmax(tabela_q[estado])
	estado, recompensa, feito, _, _ = envtest.step(acao)
	passos += 1
	
	if feito:
		if recompensa > 0:
			print("Completado!")
		else:
			print("Deu ruim")
	else:
		print(f"Passo {passos}")
env.close()
envtest.close()
