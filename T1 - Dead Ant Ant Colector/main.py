import numpy as np
import matplotlib.pyplot as plt
from random import randint
import threading
import time
#
n = 10
m = 10
nItens = 15
nFormigas = 5
ambiente = []
agentes = []
tempoMaximo = 2

## Matriz
## vazio = 0
## item = 1
## formiga = 2
## formiga e item = 3

def main( ):
	#print(ambiente)
	inicializa()

	tempoMaximo = 2
	while tempoMaximo > 0:
		tempoMaximo -= 1
		time.sleep(5)
		print(ambiente)


def inicializa():
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
	print(ambiente)
	for i in range( 0, len(agentes)):
		agentes[i].start()

def contaItens():
	contItens = 0
	contFormigas = 0
	for i in range(0, n):
		for j in range(0, m):
			if ( ambiente[i][j] == 1):
				contItens += 1
			else:
				if ( ambiente[i][j] >= 2):
					contFormigas += 1
	print(contItens, ' Itens\n', contFormigas, ' formigas')
	return [contItens, contItens]

#### Classe Ant
#
class Ant (threading.Thread):
	posX = 0
	posY = 0
	nextmove = [ 0,0]
	carry = False
	nIt = 15
	
	def __init__(self, threadID, pos):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.posX = pos[0]
		self.posY = pos[1]

	def run(self):
		while  len(threading.enumerate()) < nFormigas:
			continue
		print( self.threadID, ' - Iniciando formiga em posicao [', self.posX, ',', self.posY, ']')
		#print( self.threadID, ' - nThreads alive', len(threading.enumerate()))
		#print_time( self.threadID, 3, 1)
		while self.nIt > 0:	
			self.decide()
			self.move()
			self.nIt -= 1
		print( self.threadID, ' - Finalizando em posicao [', self.posX, ',', self.posY, ']')

	#Funções decisoras
	# eixoX 1 = direita, -1 = esquerda
	# eixoY 1 - baixo, -1 = cima

	def decide( self):
		contL = contI = 0
		if (ambiente[ self.posX][self.posY] == 3):	# Item na posição da formiga
			pass
		else:	# Movimento
			Lx = Ly = 1
			lx = ly = -1
			vet = np.zeros( [3,3])
			if self.posX+1 >= n:
				Lx = 0
			if self.posX-1 < 0:
				lx = 0
			if self.posY+1 >= m:
				Ly = 0
			if self.posY-1 < 0:
				ly = 0
			print( self.threadID, ' - ', lx, Lx, ly, Ly)
			#lx = self.posX + lx
			#ly = self.posY + ly
			#Lx = self.posX + Lx
			#Ly = self.posY + Ly
			self.nextmove[0] = randint(lx, Lx)
			self.nextmove[1] = randint(ly, Ly)	

	def move( self):
		#lock ambiente
		if ( ambiente[ self.posX + self.nextmove[0]][ self.posY + self.nextmove[1]] < 2 ):
			ambiente[ self.posX][ self.posY] -= 2
			self.posX += self.nextmove[0]
			self.posY += self.nextmove[1]
			print( self.threadID, ' - [', self.posX, ',', self.posY, ']')
			ambiente[ self.posX][ self.posY] += 2
		#unlockambiente

#
#### Classe Ant

print('Iniciando')
size = [n,m]
ambiente = np.zeros( size)
main()
contaItens()
print('Finalizando')