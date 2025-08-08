print('hello world')

# importando bibliotecas
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from itertools import cycle

# importando dataset
iris = load_iris()

numSamples, numFeatures = iris.data.shape

print(f'{numSamples}\n{numFeatures}\n{list(iris.target_names)}\n') 

X = iris.data
pca = PCA(n_components=2, whiten=True).fit(X)
X_pca = pca.transform(X)

print(pca.components_,'\n')

print(pca.explained_variance_ratio_,'\n')
print(sum(pca.explained_variance_ratio_),'\n')

# imprimindo
colors = cycle('rgb')
target_ids = range(len(iris.target_names))
plt.figure()
for i, c, label in zip(target_ids, colors, iris.target_names):
    plt.scatter(X_pca[iris.target == i, 0], X_pca[iris.target == i, 1],
               c=c, label=label)
plt.legend()
plt.show()  

