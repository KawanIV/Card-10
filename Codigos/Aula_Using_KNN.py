print('hello world')

# importando bibliotecas
import pandas as pd
import numpy as np
from scipy import spatial
import operator

# 1.2	Activity Using KNN to predict a rating for a movie
# Início
# Criando uma lista
r_cols = ['user_id', 'movie_id', 'rating']
ratings = pd.read_csv('C:/Users/Kawan_BPK/OneDrive - Biopark Educação/Área de Trabalho/LAMIA/Curso/Card 10/Bases/u.data',sep='\t', names=r_cols, usecols=range(3))
#dois = pd.read_csv('C:/Users/Kawan_BPK/OneDrive - Biopark Educação/Área de Trabalho/LAMIA/Curso/Card 10/Bases/u.item',sep='\t', names=r_cols, usecols=range(3))

def head():
	print(ratings.head())

# Agrupando filmes por ID e calculando o total de classificações e a média dessas
def grupoporid():
	propriedades = ratings.groupby('movie_id').agg({'rating':['size', 'mean']})
	return propriedades

# O número bruto de classificações não é muito útil para calcular as distancias entre os filmes, para isso trabalhamos com um novo data frame com os números normalizados
def normalizados():
	propriedades = grupoporid()
	filmesqtdmedia = pd.DataFrame(propriedades['rating']['size'])
	filmesnormalqtdmedia = filmesqtdmedia.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
	return filmesnormalqtdmedia
# parte 1 - filme1	
def generosfilme():
	movieProperties = ratings.groupby('movie_id').agg({'rating':['size', 'mean']})
	movieNumRatings = pd.DataFrame(movieProperties['rating']['size'])
	movieNormalizedNumRatings = movieNumRatings.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
	movieDict = {}
	with open(r'C:/Users/Kawan_BPK/OneDrive - Biopark Educação/Área de Trabalho/LAMIA/Curso/Card 10/Bases/u.item') as f:
		temp = ''
		for line in f:
			fields = line.rstrip('\n').split('|')
			movieID = int(fields[0])
			name = fields[1]
			genres = fields[5:25]
			genres = list(map(int, genres))
			movieDict[movieID] = (name, genres,movieNormalizedNumRatings.loc[movieID].get('size'),movieProperties.loc[movieID].rating.get('mean'))
	return movieDict[1]
# parte 2 - distancia entre dois filmes
movieProperties = ratings.groupby('movie_id').agg({'rating':['size', 'mean']})
movieNumRatings = pd.DataFrame(movieProperties['rating']['size'])
movieNormalizedNumRatings = movieNumRatings.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
movieDict = {}
with open(r'C:/Users/Kawan_BPK/OneDrive - Biopark Educação/Área de Trabalho/LAMIA/Curso/Card 10/Bases/u.item') as f:
	temp = ''
	for line in f:
		fields = line.rstrip('\n').split('|')
		movieID = int(fields[0])
		name = fields[1]
		genres = fields[5:25]
		genres = list(map(int, genres))
		movieDict[movieID] = (name, genres,movieNormalizedNumRatings.loc[movieID].get('size'),movieProperties.loc[movieID].rating.get('mean'))
# parte 3 distancia entre filmes em relação ao toy story
def ComputeDistance(a,b):
	genresA = a[1]
	genresB = b[1]
	genresDistance = spatial.distance.cosine(genresA, genresB)
	popularityA = a[2]
	popularityB = b[2]
	popularityDistance = abs(popularityA - popularityB)
	return genresDistance + popularityDistance

def getNeighbors(movieID,K):
	distances = []
	for movie in movieDict:
		if (movie != movieID):
			dist = ComputeDistance(movieDict[movieID], movieDict[movie])
			distances.append((movie, dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for X in range(K):
		neighbors.append(distances[X][0])
	return neighbors

def abc():
	K = 10
	avgRating = 0
	neighbors = getNeighbors(1, K)
	for neighbor in neighbors:
		avgRating += movieDict[neighbor][3]
		print(movieDict[neighbor][0] + " " + str(movieDict[neighbor][3]))
	avgRating /= float(K)
	print('-----------//////---------------'*10)
	return avgRating

# Chamando as funções
print('-----------//////---------------'*10)
print(grupoporid().head())
print('-----------//////---------------'*10)
print(normalizados().head())
print('-----------//////---------------'*10)
print(generosfilme())
print('-----------//////---------------'*10)
print(ComputeDistance(movieDict[2], movieDict[4]))
print('-----------//////---------------'*10)
print(abc())
