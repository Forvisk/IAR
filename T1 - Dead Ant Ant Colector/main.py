import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import randint
import threading
import time
#
N = 20
M = 20
NUM_ITENS = 50
NUM_FORMIGAS = 20
RAIOVISAO = 5
NUM_ITERACAO = 500

ambiente = []
agentes = []
tempoMaximo = 2
threadLock = threading.Lock()


## Matriz
## vazio = 0
## item = 1
## formiga livre = 2
## formiga livre e item = 3
## formiga carregando item = 4
## formiga carregando item sobre um item = 5

class Animacao( object):
	def __init__(self, ax):
		x = ambiente[0][0]
		y = ambiente[0][1]
		z = ambiente[0][2]
		c = ambiente[0][3]
		v = ambiente[0][4]
		ambiente[0][0] = 5
		ambiente[0][1] = 4
		ambiente[0][2] = 3
		ambiente[0][3] = 2
		ambiente[0][4] = 1

		self.ax = ax
		self.matrice = ax.matshow(ambiente)
		plt.colorbar(self.matrice)
		ambiente[0][0] = x
		ambiente[0][1] = y
		ambiente[0][2] = z
		ambiente[0][3] = c
		ambiente[0][4] = v

	def update(self, i):
		self.matrice.set_array(ambiente)

def main():
	fig, ax = plt.subplots()
	ani = Animacao(ax)
	#print(ambiente)
	inicializa()
	#plt.colorbar(matrice)
	ani = animation.FuncAnimation(fig, ani.update, frames=19, interval=1)
	plt.show()
	#time.sleep(5)
	for t in agentes:
		t.join()
	#print(ambiente)

def inicializa():
	print('Iniciando os ', NUM_ITENS, ' Itens')
	if (NUM_ITENS < 1):
		return
	i = 0
	while True:
		x = randint(0, N-1)
		y = randint(0, M-1)
		#print(x, ',', y)
		if( ambiente[x][y] != 1):
			ambiente[x][y] = 1
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
		if( ambiente[x][y] == 0):
			ambiente[x][y] = 2
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
			if ( pos == 1 or pos == 3 or pos == 4):
				contItens += 1
			elif ( pos == 5):
				contItens += 2
			if( pos >= 2):
				contFormigas += 1
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
	iteragiu = False
	
	def __init__(self, threadID, pos):
		threading.Thread.__init__(self)
		self.threadID = threadID+1
		self.posX = pos[0]
		self.posY = pos[1]

	def run(self):
		while  len(threading.enumerate()) < NUM_FORMIGAS:
			continue
		print( 'Ant', self.threadID, ' - Iniciando formiga em posicao [', self.posX, ',', self.posY, ']')
		#print( self.threadID, ' - nThreads alive', len(threading.enumerate()))
		#print_time( self.threadID, 3, 1)
		while self.nIt < NUM_ITERACAO:	
			#print( 'Ant',self.threadID, ': esta em [', self.posX, ',', self.posY, ']')
			if self.decide():
				self.move()
			time.sleep(0.25)
			self.nIt += 1
		print( 'Ant', self.threadID, '- Finalizando em posicao [', self.posX, ',', self.posY, ']')

	#Funções decisoras
	# eixoX 1 = direita, -1 = esquerda
	# eixoY 1 - baixo, -1 = cima

	def decide( self):
		if ( not self.iteragiu and ambiente[ self.posX][self.posY] == 3 and self.carry == 0):	# Item na posição da formiga
			#print('Ant', self.threadID, ':it', repr(self.nIt).zfill(3), ' sobre item e vazio')
			if self.sobreItem():
				self.decideMove
				self.iteragiu = False
				return True
			else:
				self.iteragiu = True
		elif( not self.iteragiu and ambiente[ self.posX][self.posY] == 4 and self.carry == 2):
			#print('Ant', self.threadID, ':it', repr(self.nIt).zfill(3), ' carregando item')
			if self.carregandoItem():
				self.decideMove()
				self.iteragiu = False
				return True
			else:
				self.iteragiu = True
		else:	# Movimento
			#print('Ant', self.threadID, ':it', repr(self.nIt).zfill(3), ' se movendo')
			self.decideMove()
			self.iteragiu = False
			return True

	def sobreItem( self):
		contL = contI = 0
		lx = max( -1, -self.posX)
		ly = max( -1, -self.posY)

		Lx = min( 1, N-1 - self.posX)
		Ly = min( 1, M-1 - self.posY)
		#print( 'Ant', self.threadID, ':it', repr(self.nIt).zfill(3),, '- ', [ self.posX, self.posY],' - x', [self.posX+lx, self.posX+Lx], '- y', [ self.posY+ly, self.posY+Ly])
		for x in range( lx, min(Lx+1,N)):
			for y in range( ly, min(Ly+1,M)):
				if (ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
					contI += 1
				else:
					contL += 1
		taxa = (contI) / (contL+1)
		#print( 'Ant', self.threadID, ':it', repr(self.nIt).zfill(3), ' - livre', contL, '; itens', contI, '; taxa', taxa)
		contrataxa = randint(0,100)/100
		if(  contrataxa >= taxa):
			print( 'Ant', self.threadID, ':it', repr(self.nIt).zfill(3), [self.posX, self.posY], ' - pega item - ', contrataxa, '>',taxa, '- L:', contL, '; I', contI)
			threadLock.acquire()
			ambiente[self.posX][self.posY] -= 1
			self.carry = 2
			ambiente[self.posX][self.posY] += 2
			threadLock.release()

			return False
		else:
			print( 'Ant', self.threadID, ':it', repr(self.nIt).zfill(3), [self.posX, self.posY], ' - não pega item - ', contrataxa, '<',taxa, '- L:', contL, '; I', contI)
			return True
		#self.nIt = NUM_ITERACAO
		
	def carregandoItem(self):
		contL = contI = 0
		lx = max( -1, -self.posX)
		ly = max( -1, -self.posY)

		Lx = min( 1, N-1 - self.posX)
		Ly = min( 1, M-1 - self.posY)
		#print( 'Ant', self.threadID, ':it', repr(self.nIt).zfill(3), '- ', [ self.posX, self.posY],' - x', [self.posX+lx, self.posX+Lx], '- y', [ self.posY+ly, self.posY+Ly])
		for x in range( lx, min(Lx+1,N)):
			for y in range( ly, min(Ly+1,M)):
				if (ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
					contI += 1
				else:
					contL += 1
		taxa = 1-((contI+1) / (contL+1))
		#print( 'Ant', self.threadID, ':it', repr(self.nIt).zfill(3), ' - livre', contL, '; itens', contI, '; taxa', taxa)
		contrataxa = min( randint(0,100)/100, randint(0,100)/100)
		if(  contrataxa >= taxa):
			print( 'Ant', self.threadID, ':it', repr(self.nIt).zfill(3), [self.posX, self.posY], ' - solta item - ', contrataxa, '>=',taxa, '- L:', contL, '; I', contI)
			threadLock.acquire()
			ambiente[self.posX][self.posY] += 1
			self.carry = 0
			ambiente[self.posX][self.posY] -= 2
			threadLock.release()
			return False
		else:
			print( 'Ant', self.threadID, ':it', repr(self.nIt).zfill(3), [self.posX, self.posY], ' - não solta item - ', contrataxa, '<',taxa, '- L:', contL, '; I', contI)
			return True

	def decideMove(self):
		contL = contI = 0
		#Lx = Ly = RAIOVISAO
		#lx = ly = -RAIOVISAO
		vet = np.zeros( [3,3])
		
		#print( 'Ant', self.threadID, ':it', repr(self.nIt).zfill(3),, ' - ', [[-RAIOVISAO, self.posX * -1], [RAIOVISAO, N-1 - self.posX]], '-', [ [-RAIOVISAO, self.posY * -1], [RAIOVISAO, M-1 - self.posY]])
		#Limites da Matriz Considerados
		lx = max( -RAIOVISAO, -self.posX)
		ly = max( -RAIOVISAO, -self.posY)

		Lx = min( RAIOVISAO, N-1 - self.posX)
		Ly = min( RAIOVISAO, M-1 - self.posY)
		#print( 'Ant', self.threadID, ':it', repr(self.nIt).zfill(3), '- ', [ self.posX, self.posY],' - min', [RAIOVISAO, N-1 - self.posX], '- min', [ RAIOVISAO, M-1 - self.posY])
		# Verifica os Itens e suas posições
		posItens = []
		for i in range(lx, Lx):
			for j in range( ly, Ly):
				if (i != 0 and j != 0):
					if (ambiente[ self.posX+i][self.posY+j] == 1):
						#posItens.append( [self.posX+i,self.posY+j])
						posItens.append( [i,j])
						contI += 1

		lx = max( lx, -1)
		Lx = min( Lx, 1)
		ly = max( ly, -1)
		Ly = min( Ly, 1)
		print('Ant', self.threadID, ':it', repr(self.nIt).zfill(3), '-', [ self.posX, self.posY], ' - ', [lx, Lx], ';', [ly,Ly])
		self.nextmove = [0,0]
		while (self.nextmove[0] == 0 and self.nextmove[1] == 0):
			if (lx >= Lx):
				self.nextmove[0] = 0
			else:
				self.nextmove[0] = randint(lx, Lx)
			if (ly >= Ly):
				self.nextmove[1] = 0
			else:
				self.nextmove[1] = randint(ly, Ly)
		#'''
		if (contI > 0):	#Item na area de visão
			#print('Ant', self.threadID, ':it', repr(self.nIt).zfill(3), ': proximo movimento ', self.nextmove)
			#print( 'Ant', self.threadID, ':it', repr(self.nIt).zfill(3),, '-', [self.posX, self.posY], '-', posItens, '; nitens', contI)
			for pi in posItens:
				if( pi[0] < 0):
					if( pi[1] < 0):
						vet[0][0] += 1
					elif(pi[1] == 0):
						vet[0][1] += 1
					else:	#elif( pi[1] > 0)):
						vet[0][2] += 1
				elif( pi[0] == 0):
					if( pi[1] < 0):
						vet[1][0] += 1
					elif(pi[1] == 0):
						vet[1][1] += 1
					else:	#elif( pi[1] > 0)
						vet[1][2] += 1
				else: #elif( pi[0] > 0):
					if( pi[1] < 0):
						vet[2][0] += 1
					elif(pi[1] == 0):
						vet[2][1] += 1
					else:	#elif( pi[1] > 0)
						vet[2][2] += 1
				#print( 'Ant', ':it', repr(self.nIt).zfill(3), self.threadID, ' - vet', vet)
			if( contI > 0):
				q = randint(-contI, contI)
				if ( q > 0):
					i = j = 0
					#print('Ant', ':it', repr(self.nIt).zfill(3),, self.threadID, '-', contL, ';', q)
					while q > 0:
						if( i >= 3):
							i = 0
							break
						if( j >= 3):
							j = 0

						q -= vet[i,j]
						if( q > 0):
							i += 1
							j += 1
					#print('Ant', ':it', repr(self.nIt).zfill(3), self.threadID, '-', i, j)
					if( j == 3):
						j = 0
					print('Ant', self.threadID, ':it', repr(self.nIt).zfill(3), '- indo a encontro de um item no quadrante', [i-1, j-1])
					self.nextmove = [i-1, j-1]
					#'''
	
	def move( self):
		threadLock.acquire() #lock ambiente
		k1 = abs(self.posX + self.nextmove[0])
		k2 = abs(self.posY + self.nextmove[1])
		print( 'Ant', self.threadID, ':it', repr(self.nIt).zfill(3), 'se move de', [self.posX, self.posY], ' para ', [k1, k2], '(', [self.nextmove[0],self.nextmove[1]], ')')
		#print('Ant',self.threadID, ':it', repr(self.nIt).zfill(3),, ':', k1, k2)
		if (k1 >= N or k2 >= M):
			print( 'Ant', self.threadID, ':it', repr(self.nIt).zfill(3), 'se move de', [self.posX, self.posY], ' para ', [k1, k2], 'se batendo na parede')
		elif ( ambiente[ k1][ k2] < 2 ):
			ambiente[ self.posX][ self.posY] -= (2 + self.carry)
			#self.posX = abs(self.posX + self.nextmove[0])
			#self.posY = abs(self.posY + self.nextmove[1])
			self.posX = k1
			self.posY = k2
			ambiente[ self.posX][ self.posY] += (2 + self.carry)
		
		threadLock.release()	#unlockambiente

#
#### Classe Ant

print('Iniciando')
size = [N,M]
ambiente = np.zeros( size)
main()
contaItens()
print('Finalizando')