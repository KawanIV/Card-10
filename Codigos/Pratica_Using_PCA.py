print('hello world')

# importando bibliotecas
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from itertools import cycle

# importando dataset
vendas = pd.read_excel('C:/Users/Kawan_BPK/OneDrive - Biopark Educação/Área de Trabalho/LAMIA/Curso/Card 10/Bases/OpGanhasMensais.xlsx')
# head
print(vendas.head())

#clunas numéricas
colunas_numericas = ['Vendas', 'Dias Fechamento', 'Taxa de conversão', 'Qtd Oport Emitida', 'Qtd Oport Ganha']
X = vendas[colunas_numericas].values

# Normalizar os dados 
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Aplicar PCA
pca = PCA(n_components=2, whiten=True)
X_pca = pca.fit_transform(X_scaled)

print(f"\nComponentes do PCA:\n{pca.components_}")
print(f"\nVariância explicada por cada componente: {pca.explained_variance_ratio_}")
print(f"Variância total explicada: {sum(pca.explained_variance_ratio_):.4f}")

# inserindo meses
colors = cycle('rgbcmyk')
meses = vendas['Mês de fechamento'].values

# gráfico
plt.figure()
for i, c, mes in zip(range(len(meses)), colors, meses):
    plt.scatter(X_pca[i, 0], X_pca[i, 1], c=c,label=mes, s=100)
    plt.text(X_pca[i, 0], X_pca[i, 1], mes, fontsize=9, ha='center', va='bottom')

plt.ylabel('PC2 : ↑ Meses mais eficientes')
plt.xlabel('PC1 : → Meses com mehor performance')
plt.legend()
plt.show()
