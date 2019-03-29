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
tempoExecucao = 0
tempoMaximo = 2

## Matriz
## vazio = 0
## item = 1
## formiga = 2
## formiga e item = 3

def main( ):
	#print(ambiente)
	inicializa()

	tempoExecucao = 0
	while tempoExecucao < tempoMaximo:
		tempoExecucao += 1
		time.sleep(15)
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
				if ( ambiente[i][j] > 2):
					contFormigas += 1
	print(contItens, ' Itens\n', contFormigas, ' formigas')
	return [contItens, contItens]

#### Classe Ant
#
class Ant (threading.Thread):
	code = 0
	posX = 0
	posY = 0
	nextmove = [ 1, 1]
	carry = False
	
	def __init__(self, threadID, pos):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.posX = pos[0]
		self.posY = pos[1]

	def run(self):
		print( 'Iniciando formiga ', self.threadID, ' em posicao [', self.posX, ',', self.posY, ']')
		#print_time( self.threadID, 3, 1)
		self.decide()
		self.move()
		print( 'Finalizando ', self.threadID)

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
			if self.posX+1 >= n:
				Lx = 0
			if self.posX-1 < 0:
				lx = 0
			if self.posY+1 >= m:
				Ly = 0
			if self.posY-1 < 0:
				ly = 0
			print( self.threadID, ' - ', lx, Lx, ly, Ly)

			for x in range( lx, Lx):
				for y in range( ly, Ly):
					if ( x != 0 and y != 0):
						if ()
			pass
		pass

	def move( self):
		#lock ambiente
		ambiente[ self.posX][ self.posY] -= 2
		self.posX += self.nextmove[0]
		self.posX += self.nextmove[1]
		print( '[', self.posX, ',', self.posY, ']')
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