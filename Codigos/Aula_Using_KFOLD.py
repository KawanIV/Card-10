import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn.model_selection import cross_val_score
from sklearn import datasets
from sklearn import svm

iris = datasets.load_iris()

# A single train/test split is made easy with the train_test_split function in the cross_validation library:

# Split the Iris data into train/test data sets with 40% reserved for testing
X_train, X_test, Y_train, Y_test = train_test_split(iris.data, iris.target, test_size=0.4, random_state=0)

print(X_train,'\n')
print(X_test,'\n')
print(Y_train,'\n')
print(Y_test,'\n')

# Build an SVC model for predicting iris classifications using training data
clf = svm.SVC(kernel='linear', C=1).fit(X_train, Y_train)

print(clf,'\n')
# Now measure its performance with the test data
clf.score(X_test, Y_test)
print('Usando modelo linear sem k-fold:',clf.score(X_test, Y_test),'\n')

# K-Fold cross validation is just as easy; let's use a K of 5:

# We give cross_val_score a model, the entire data set and its "real" values, and the number of folds:
scores = cross_val_score(clf, iris.data, iris.target, cv=5)

# Print the accuracy for each fold:
print('Usando modelo linear e k(5):',scores,'\n')

# And the mean accuracy of all 5 folds:
print('Média de modelo linear e k(5):',scores.mean(),'\n')

# Com o resultado bom vamos reconstruir usando uma função polinomial para prever as classificações
# Build an SVC model for predicting iris classifications using training data
clf = svm.SVC(kernel='poly',C=1).fit(X_train, Y_train)
scores = cross_val_score(clf,iris.data, iris.target,cv=5)
print('Usando modelo polinomial e k(5):',scores,'\n')
print('Média de modelo polinomial e k(5):',scores.mean(),'\n')
# Now measure its performance with the test data
clf = svm.SVC(kernel='poly',C=1).fit(X_train, Y_train)
print('Usando modelo polinomial sem k-fold:',(clf.score(X_test, Y_test)),'\n')



