import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn.model_selection import cross_val_score
from sklearn import datasets
from sklearn import svm

iris = datasets.load_iris()

# A divisão dos dados entre treino e teste é fácil com a função train_test_split da biblioteca cross_validation:

# Dividir os dados de iris em treino/teste onde 40% serão reservados para testagem
X_train, X_test, Y_train, Y_test = train_test_split(iris.data, iris.target, test_size=0.4, random_state=0)

print(X_train,'\n')
print(X_test,'\n')
print(Y_train,'\n')
print(Y_test,'\n')

# Vamos construir um modelo SVC para predizer a classificação das iris usando os dados de treino
clf = svm.SVC(kernel='linear', C=1).fit(X_train, Y_train)

print(clf,'\n')
# Agora vamos mensurar a performance com os dados de teste
clf.score(X_test, Y_test)
print('Usando modelo linear sem k-fold:',clf.score(X_test, Y_test),'\n')

# É fácil aplicar o método de validação cruzada K-Fold; vamos usar k = 5:

# Nós iserimos na função cross_val_score, todo o dataset, os seus valores reais e o numero de folds(grupos/clusters) 
scores = cross_val_score(clf, iris.data, iris.target, cv=5)

# Imprimimos a acurácia de cada 'fold'
print('Usando modelo linear e k(5):',scores,'\n')

# E a média da acuracia entre os 5 'folds'
print('Média de modelo linear e k(5):',scores.mean(),'\n')

# Com o resultado bom vamos reconstruir usando uma função polinomial para prever as classificações
# Build an SVC model for predicting iris classifications using training data
clf = svm.SVC(kernel='poly',C=1).fit(X_train, Y_train)
scores = cross_val_score(clf,iris.data, iris.target,cv=5)
print('Usando modelo polinomial e k(5):',scores,'\n')
print('Média de modelo polinomial e k(5):',scores.mean(),'\n')
# Agora mensuramos a performance com os dados de teste
clf = svm.SVC(kernel='poly',C=1).fit(X_train, Y_train)
print('Usando modelo polinomial sem k-fold:',(clf.score(X_test, Y_test)),'\n')
print("O modelo linear com k-fold, apesar de ser mais simples, consegue ter mais performance que o modelo polinomial com e sem k-fold")


