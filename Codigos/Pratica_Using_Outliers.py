# Importando bibliotecas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

# Datasets
DadosBrutos = pd.read_excel('C:/Users/Kawan_BPK/OneDrive - Biopark Educação/Área de Trabalho/LAMIA/Curso/Card 10/Bases/pib_worldexcel.xlsx')
# Convertendo a coluna 2024 para string e depois para float com substituição
print(DadosBrutos[2024].dtype)

# Printar head()
print("Dados Brutos","\n")
print(DadosBrutos.head(10))
print("=========="*7)
time.sleep(2)
# Printar colunas
print("Colunas Originais","\n")
print(DadosBrutos.columns)
print("=========="*7)
time.sleep(2)
# Printar informações específicas
print("Seleção de Colunas","\n")
print(DadosBrutos[['COUNTRY',2024,'INDICATOR']].head(10))
print("=========="*7)
time.sleep(2)
# Renomear coluna 2024
print("Ajustar coluna '2024' para 'PIB U$$'","\n")
DadosBrutos = DadosBrutos.rename(columns={2024: 'PIB U$$'})
print(DadosBrutos.columns)
print("=========="*7)
time.sleep(2)
print("Dados Ajustados","\n")
pib = DadosBrutos[['COUNTRY','PIB U$$']].copy()

print(pib.head(10))
print("=========="*7)
time.sleep(2)
# Gráfico
print("Histograma com Outliers","\n")
plt.hist(pib['PIB U$$'],100)
print(plt.show())
print("=========="*7)
time.sleep(2)
# Média com 'outliers'
print("Primeira Média...","\n")
print(f"Média com 'outliers': {round(pib['PIB U$$'].mean(),2)}\n")
print("=========="*7)
time.sleep(2)
print("Removendo Outliers...","\n")

def reject_outliers(data):
    # Apenas limite superior pois não há PIB negativo
    u = np.median(data)
    s = np.std(data)
    filtered = [e for e in data if (e <= u + 2 * s)]
    return filtered
    
filtered = reject_outliers(pib['PIB U$$'])
time.sleep(2)
print("Novo Histograma","\n")
plt.hist(filtered, 100)
print(plt.show())
print("=========="*7)
time.sleep(2)
print("Nova Média","\n")
print("Média recalculada: ",round(np.mean(filtered),2),"\n")
