# Importando as bibliotecas
import time
import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn.model_selection import cross_val_score
from sklearn import datasets
from sklearn import svm

# Carregando o dataset wine
wine = datasets.load_wine()

# Visualizar o nome das 'colunas'
print("Colunas","\n")
print(wine.feature_names[:],'\n')
print("=========="*7)
time.sleep(2)
# Visualizar o nome das 'classes'
print("Classes","\n")
print(wine.target_names[:],'\n')
print("=========="*7)
time.sleep(2)
# Visualizar uma amostra dos dados
print("Amostra","\n")
print(wine.data[:5],'\n')
print("=========="*7)
time.sleep(2)

# Dividir os dados em treino/teste
X_train, X_test, Y_train, Y_test = train_test_split(wine.data, wine.target, test_size=0.4, random_state=0)

# printar esses dados
print("Dados de Treino e Amostra","\n")
print(X_train,'\n')
print(X_test,'\n')
print(Y_train,'\n')
print(Y_test,'\n')
print("=========="*7)
time.sleep(2)

# Construir modelo SVC para predizer a classificação dos vinhos
clf = svm.SVC(kernel='linear',C=1).fit(X_train, Y_train)

# Printar o modelo SVC
print("Modelo SVC","\n")
print(clf,'\n')
print("=========="*7)
time.sleep(2)

# Mensurar a performance com os dados de teste
print("Performance com os Dados de Teste","\n")
clf.score(X_test, Y_test)
print('Modelo linear sem k-fold:',clf.score(X_test, Y_test),'\n')
print("=========="*7)
time.sleep(2)

# Aplicando a validação cruzada K-Fold = 5:
scores = cross_val_score(clf, wine.data, wine.target, cv=5)

# Imprimimos a acurácia de cada 'fold' e a média entre todos eles
print("Performance de cada fold e a média entre eles","\n")
print('Usando modelo linear e k(5):',scores,'\n')
print('Média de modelo linear e k(5):',scores.mean(),'\n')
print("=========="*7)
time.sleep(2)
