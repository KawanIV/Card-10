#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import time

# dataset
incomes = np.random.normal(27000, 15000,10000)
incomes = np.append(incomes,[1000000000])

# gráfico
plt.hist(incomes,50)
plt.show()

# anotação
print("Observe como um valor grande distroce o gráfico...")
print('-----------------'*7,'\n')
time.sleep(3)

print('Média de rendimento: ',round(incomes.mean(),2),'\n')
print("Observe como o valor da média é extremamente alto, desse forma, ele não reflete a média de rendimento das pessoas.")
print('-----------------'*7,'\n')
time.sleep(3)

print("Agora aplicaremos uma técnica para filtrar os bilionários para fora do cálculo","\n")
time.sleep(3)

def reject_outliers(data):
	u = np.median(data)
	s = np.std(data)
	filtered = [e for e in data if (u - 2 * s < e < u + 2 * s)]
	return filtered
	
filtered = reject_outliers(incomes)

plt.hist(filtered, 50)
plt.show()

print('-----------------'*7,'\n')
time.sleep(5)

print("Recalculamos a média...",'\n')
time.sleep(5)
print("Média recalculada: ",round(np.mean(filtered),2),"\n")
print("Agora o valor da média reflete de forma mais fiel a média de rendimentos das pessoas...","\n")
print('-----------------'*7,'\n')
