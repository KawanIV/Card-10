print('hello world')

# importando bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import matplotlib.lines as mlines

# Início
# Criando uma lista
sorvetes = pd.read_excel('C:/Users/Kawan_BPK/OneDrive - Biopark Educação/Área de Trabalho/LAMIA/Curso/Card 10/Bases/excel_vendas_sorveteria.xlsx')


def plan():
	print(sorvetes.head())
	
def plan2():
	# Preparar os dados
	sorvetes['Tamanho'] = sorvetes['Tamanho'].astype(str).str.upper()
	precos = sorvetes[['Preço']].values
	preco_min = np.min(precos)
	preco_max = np.max(precos)
	# Normalizar os dados
	sorvetes['PreçoNormalizado'] = sorvetes['Preço'].apply(lambda x: (x - preco_min) / (preco_max - preco_min))
	# Dados para o kmeans
	k = sorvetes[['PreçoNormalizado']].values
	# Aplicar o kmeans
	kmeans = KMeans(n_clusters=6,random_state=42,n_init=10)
	sorvetes['Grupos'] = kmeans.fit_predict(k)
	# Grupos
	CorGrupos = {0: 'red',1:'blue',2:'green',3: 'orange', 4: 'purple',5: 'brown'}
	sorvetes['Cor'] = sorvetes['Grupos'].map(CorGrupos)
	# Gráfico
	plt.figure(figsize=(12,8))
	# Plotar os pontos coloridos por cluster
	for grupos in range(6):
		subset = sorvetes[sorvetes['Grupos'] == grupos]
		plt.scatter(subset['Tamanho'],subset['Preço'],
					c=subset['Cor'], label=f'Cluster {grupos}',
					s=100, alpha=0.7, edgecolors='black')
					
	# CORREÇÃO CRÍTICA: Converter centróides normalizados para escala original
	centroids = kmeans.cluster_centers_
	centroids_originais = centroids * (preco_max - preco_min) + preco_min				

	# Adicionar linhas verticais nos centróides dos clusters_
	for i, centroide in enumerate(centroids_originais):
		plt.axhline(y=centroide[0], color='black', linestyle='--', alpha=0.8, 
					label=f'Limite Cluster {i+1}' if i == 0 else "")
	# Adicionar rótulos e título
	plt.xticks([0, 1, 2], ['PEQUENO', 'MÉDIO', 'GRANDE'])
	plt.ylabel('Preço (R$)')
	plt.xlabel('')
	plt.title('K-Means de Sorvetes por Preço - Colorido por TAMANHO')
	plt.legend()
	plt.grid(True, alpha=0.3)
	
	# Mostrar o gráfico
	plt.tight_layout()
	plt.show()

## Chamando as funções
print('-----------//////---------------'*10)
print(plan())
print('-----------//////---------------'*10)
print(plan2())
