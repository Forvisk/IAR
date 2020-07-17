import sys
import numpy as np
import scipy.misc as sm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import randint
import threading
import time
import imageio as img	# novo package de imagem
#
# Voo de Levy
# Como melhorar:
# Melhorar o Determinismo
ALPHA = 1	# ñao pode ser 0
KA1 = 1
KA2 = 1
RAIOVISAO = 1

NUM_ITERAC_POR_FORMIGA = 10000
SLEEP = False

DIVTAXA = ((RAIOVISAO*2+1) * (RAIOVISAO*2+1)) -1

N_TIPO_ITENS = 1	# numero de grupos de itens
D_DADO = 1 			# dimensão do dado a ser trabalhado

agentes = []
itens = []

threadLock = threading.Lock()
threadLockIteracao = threading.Lock()
numIt = 0
outputFile = "iteracoes/"+str(randint(0,1000))+'_rv'+str(RAIOVISAO)+'_nf'+str(NUM_FORMIGAS)
ambiente = []

## Matriz
## vazio = 0
## item = 2
## formiga livre = -1
## formiga livre e item = -2
## formiga carregando item = -1
## formiga carregando item sobre um item = -2
class Cenario(object):
	ambiente = []	#utiliza 
	dados = []	# se tem itens, sera usado no lugar do ambiente
	itens = []	# lista de itens
	size = [0,0]
	num_itens = 0
	num_formigas = 0

	n_tipoDados = 1
	d_dados = 1

	def __init__(self, size, num_formigas, num_itens):
		self.size = size
		self.ambiente = np.ones(size)
		self.dados = np.zeros(size)
		self.num_itens = num_itens
		self.num_formigas = num_formigas
		print('Cenario: '+str(size)+' com '+str(self.num_itens)+' itens e '+str(self.num_formigas)+' formigas.')

	def print(self):
		print('Cenario: '+str(size)+' com '+str(self.num_itens)+' itens e '+str(self.num_formigas)+' formigas.')


class Item(object):
	idItem = 0
	dado = []
	grupo = 0
	pos = []

	def __init__(self, idItem, dado, grupo):
		self.idItem = idItem
		self.dado = dado
		self.grupo = grupo
		print('Item '+str(self.idItem)+' = '+str(self.dado)+', '+str(self.grupo))

	def setPos(self,pos):
		self.pos = pos

	def printItem(self):
		print('Item '+str(self.idItem)+' = '+str(self.dado)+', '+str(self.grupo)+'\n\tpossicao '+str(self.pos))

class Animacao( object):
	def __init__(self, ax):
		ambiente[0][0] = 2
		ambiente[0][1] = -2

		self.ax = ax
		self.matrice = ax.matshow(ambiente)
		plt.colorbar(self.matrice)
		
		ambiente[0][0] = 1
		ambiente[0][1] = 1

	def update(self, i):
		self.matrice.set_array(ambiente)

def salvaImagem2():
	nIt = numIt
	imagem = ambiente * 25
	saving = outputFile+'-'+str(nIt).zfill(10)+'.png'
	#sm.imsave( saving, imagem)
	img.imwrite(saving, imagem)
	print('Main - saving',saving)

def inicializa():
	if N == 0 or M == 0:
		N = NUM_ITENS*5
		M = NUM_ITENS*5
		N += randint(0, N/3)
		M += randint(0, M/3)
	print('Iniciando os ', NUM_ITENS, ' Itens')
	if (NUM_ITENS < 1):
		return
	i = 0
	while True:
		x = randint(0, N-1)
		y = randint(0, M-1)
		#print(x, ',', y)
		if( ambiente[x][y] != 2):
			ambiente[x][y] = 2
			i += 1
		if( i >= NUM_ITENS):
			break
	print('Inicializando ', NUM_FORMIGAS, ' Formigas')
	if (NUM_FORMIGAS < 1):
		return
	i = 0
	while True:
		x = randint(0, N-1)
		y = randint(0, M-1)
		#print(x, ',', y)
		if( ambiente[x][y] > 0):
			ambiente[x][y] = -ambiente[x][y]
			agentes.append( Ant( i, [x, y]))
			i += 1
		if( i >= NUM_FORMIGAS):
			break
	#print(ambiente)
	for i in range( 0, len(agentes)):
		agentes[i].start()

def contaItens():
	contItens = 0
	contFormigas = 0
	pos = 0
	for i in range(0, N):
		for j in range(0, M):
			pos = ambiente[i][j]
			if ( pos > 1 or pos < -1):
				contItens += 1
	print('Itens', contItens,' formigas', contFormigas)
	return [contItens, contItens]

#### Classe Ant
#
class Ant (threading.Thread):
	posX = 0
	posY = 0
	nextmove = [ 0,0]
	carry = 0
	nIt = 0
	carga = -1
	
	def __init__(self, threadID, pos):
		threading.Thread.__init__(self)
		self.threadID = threadID+1
		self.posX = pos[0]
		self.posY = pos[1]
		self.haveFocus = False
		self.focus = [0,0]
		self.iteragiu = False
		self.carga = np.zeros(D_DADO)

	def run(self):
		pass

	
#### Classe Ant
def distanciaVizinhanca(pos):
	valor = 0
	nVizinhos = 0
	for ix in range(-1,2):
		x = pos[0]+ix
		if( x >= 0) and ( x < N):		
			for iy in range(-1,2):
				y = pos[1]+iy
				if (y >= 0) and (y < M):
					#print([x,y])
					if( abs(ambiente[x][y]) > 1):
						valor += 1 - distancia(pos, [x,y])/ALPHA
						nVizinhos += 1
	if nVizinhos > 0:
		valor = 1/pow(nVizinhos,2) * valor
	else:
		return 0
	if (valor <= 0):
		valor = 0 
	return valor

def distancia(pos1, pos2):
	valor = 0
	for i in range(0, D_DADO):
		valor += pow( dados[pos1[0]][pos1[1]][i] - dados[pos2[0]][pos2[1]][i], 2)
	return sqrt(valor)

def vizinhanca(ponto):
	nVizinhos = 0
	for ix in range(-1,2):
		x = ponto[0]+ix
		if( x >= 0) and ( x < N):		
			for iy in range(-1,2):
				y = ponto[1]+iy
				if (y >= 0) and (y < M):
					#print([x,y])
					if( abs(ambiente[x][y]) > 1):
						nVizinhos += 1
	return nVizinhos

def criaItens():
	i = 0
	print(NUM_ITENS)
	for i in range(1, NUM_ITENS):
		print([i,NUM_ITENS])
		itens.append( Item(i,1,1))

def lerArquivo( filename):
	nItens = 0
	file =  open( filename)
	for line in file:
		if line[0] == '#' or line[0] == '\n':
			continue
		line = line.expandtabs(1)
		dataLine = line.split(' ')
		dado = []
		#print(dataLine)
		for i in range(0,len(dataLine)-1):
			dado.append(float(dataLine[i]))
		grupo = int(dataLine[len(dataLine)-1])
		itens.append( Item(nItens, dado, grupo))
		nItens += 1
	file.close()
	if nItens > 0:
		NUM_ITENS = nItens
		print(NUM_ITENS)
		return True
	return False

def inicio( argv):
	if (len(argv) == 5):
		for i in range(1,5):
			if not argv[i].isnumeric():
				return False
		size = [int(argv[1]),int(argv[2])]
		num_itens = int(argv[3])
		num_formigas = int(argv[4])
		ambiente = Cenario( size, num_itens, num_formigas)
		criaItens()

		return True
	elif ( len(argv) == 2):
		filename = argv[1]
		if filename.split('.')[1] == 'txt':
			if not lerArquivo( filename):
				return False
			#print(NUM_ITENS)
			itens[0].printItem()
			return True
		else:
			return False

print('Iniciando')
if (len(sys.argv) > 1):
	if not inicio( sys.argv):
		print("Entrada inválida!")
else:
	print("Favor iniciar com: ")
	print("num_linhas num_colunas num_itens num_formigas")
	print("ou")
	print("nome_arquivo.txt")
ambiente.print()
print('Finalizando')