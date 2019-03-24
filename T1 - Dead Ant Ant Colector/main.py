import numpy as np
import matplotlib.pyplot as plt
from random import randint
from classes.ant import *

n = 10
m = 10
nItens = 15
nFormigas = 5
ambiente = 0
agentes = []

## Matriz
## vazio = 0
## item = 1
## formiga = 2
## formiga e item = 3

def main( ):
	print(ambiente)
	inicializaItens()
	inicializaFormigas()

def inicializaItens( ):
	print('Iniciando os ', nItens, ' Itens')
	if (nItens < 1):
		return
	i = 0
	while True:
		x = randint(0, n-1)
		y = randint(0, m-1)
		#print(x, ',', y)
		if( ambiente[x][y] != 1):
			ambiente[x][y] = 1
			i += 1
		if( i >= nItens):
			break

def inicializaFormigas():
	print('Inicializando ', nFormigas, ' Formigas')
	if (nFormigas < 1):
		return
	i = 0
	while True:
		x = randint(0, n-1)
		y = randint(0, m-1)
		#print(x, ',', y)
		if( ambiente[x][y] == 0):
			ambiente[x][y] = 2
			agentes.append( Ant( i, [x, y]))
			i += 1
		if( i >= nFormigas):
			break



def contaItens():
	contItens = 0
	contFormigas = 0
	for i in range(0, n):
		for j in range(0, m):
			if ( ambiente[i][j] == 1):
				contItens += 1
			else:
				if ( ambiente[i][j] == 2):
					contFormigas += 1
	print(contItens, ' Itens\n', contFormigas, ' formigas')
	return [contItens, contItens]

print('Iniciando')
size = [n,m]
ambiente = np.zeros( size)
main()
print(ambiente)
contaItens()
print('Finalizando')