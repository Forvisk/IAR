import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import randint
import threading
import time
#
# Voo de Levy
# Como melhorar:
# Melhorar o Determinismo

N = 50
M = 50
PORCENT_ITENS = 40
NUM_ITERAC_POR_FORMIGA = 1000
NUM_ITENS = (N*M*PORCENT_ITENS)/100
NUM_FORMIGAS = 10
RAIOVISAO = 5
NUM_ITERACAO = NUM_FORMIGAS * NUM_ITERAC_POR_FORMIGA

ambiente = []
agentes = []
threadLock = threading.Lock()
threadLockIteracao = threading.Lock()
numIt = 0

## Matriz
## vazio = 0
## item = 1
## formiga livre = 2
## formiga livre e item = 3
## formiga carregando item = 4
## formiga carregando item sobre um item = 5

class Animacao( object):
	def __init__(self, ax):
		ambiente[0][0] = 4

		self.ax = ax
		self.matrice = ax.matshow(ambiente)
		plt.colorbar(self.matrice)
		
		ambiente[0][0] = 0

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
	
	def __init__(self, threadID, pos):
		threading.Thread.__init__(self)
		self.threadID = threadID+1
		self.posX = pos[0]
		self.posY = pos[1]
		self.haveFocus = False
		self.focus = [0,0]
		self.iteragiu = False


	def run(self):
		global numIt
		while  len(threading.enumerate()) < NUM_FORMIGAS:
			continue
		print( 'Ant', repr(self.threadID).zfill(3), '0- Iniciando formiga em posicao [', self.posX, ',', self.posY, ']')
		#while self.nIt < NUM_ITERACAO:
		while numIt < NUM_ITERACAO:
			if self.decide():
				if self.haveFocus and (self.posX != self.focus[0] and self.posY != self.focus[1]):
					self.moveToFocus()
				else:
					self.haveFocus = False
					self.decideMove()
				self.move()
			time.sleep(0.25)
		#	self.nIt += 1
			threadLockIteracao.acquire()
			numIt += 1
			self.nIt = numIt
			threadLockIteracao.release()
		print( 'Ant', repr(self.threadID).zfill(3), 'X- Finalizando em posicao [', self.posX, ',', self.posY, ']')

	def decide( self):
		if (ambiente[ self.posX][self.posY] == 3 and self.carry == 0 and not self.iteragiu):	# Item na posição da formiga
			print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), ' sobre item e vazio')
			if self.sobreItem():
				self.iteragiu = False
				return True
			else:
				self.haveFocus = False
				self.iteragiu = True
		elif(ambiente[ self.posX][self.posY] == 4 and self.carry == 2  and not self.iteragiu):
			print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), ' carregando item')
			if self.carregandoItem():
				self.iteragiu = False
				return True
			else:			
				self.haveFocus = False
				self.iteragiu = True
		else:	# Movimento
			self.iteragiu = False
			return True
		return False

	def sobreItem( self):
		contL = contI = 0
		lx = max( -1, -self.posX)
		ly = max( -1, -self.posY)

		Lx = min( 1, N-1 - self.posX)
		Ly = min( 1, M-1 - self.posY)
		#print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), '-', [ self.posX, self.posY],'; Lim x', [lx,Lx], '; LimY',[ly,Ly])
		for x in range( self.posX+lx, self.posX+Lx+1):
			for y in range( self.posY+ly, self.posY+Ly+1):
				#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), '-',[x,y])
				if ( x != self.posX or y != self.posY):
					if (ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
						#print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), 'em', [self.posX, self.posY], 'item em',[x,y])
						contI += 1
					else:
						#print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), 'em', [self.posX, self.posY], 'vazio em',[x,y])
						contL += 1
		taxa = (contI) / (contL+contI)
		#print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), ' - livre', contL, '; itens', contI, '; taxa', taxa)
		contrataxa = randint(0,100)/100
		if(  contrataxa >= taxa):
			threadLock.acquire()
			ambiente[self.posX][self.posY] -= 1
			self.carry = 2
			ambiente[self.posX][self.posY] += 2
			threadLock.release()
			print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), [self.posX, self.posY], ' - pega item - ', contrataxa, '>',taxa, '- L:', contL, '; I', contI)
			return False
		else:
			print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), [self.posX, self.posY], ' - não pega item - ', contrataxa, '<',taxa, '- L:', contL, '; I', contI)
			return True
		#self.nIt = NUM_ITERACAO
		
	def carregandoItem(self):
		print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), 'carregando item')
		contL = contI = 0
		lx = max( -1, -self.posX)
		ly = max( -1, -self.posY)

		Lx = min( 1, N-1 - self.posX)
		Ly = min( 1, M-1 - self.posY)
		#print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), '-', [ self.posX, self.posY],'; Lim x', [lx,Lx], '; LimY',[ly,Ly])
		for x in range( self.posX+lx, self.posX+Lx+1):
			for y in range( self.posY+ly, self.posY+Ly+1):
				#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), '-',[x,y])
				if ( x != self.posX or y != self.posY):
					if (ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
						#print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), 'em', [self.posX, self.posY], 'item em',[x,y])
						contI += 1
					else:
						#print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), 'em', [self.posX, self.posY], 'vazio em',[x,y])
						contL += 1
		taxa = 1-((contI) / (contL+contI))
		#print( 'Ant', repr(self.nIt).zfill(3), ':it', repr(self.nIt).zfill(3), ' - livre', contL, '; itens', contI, '; taxa', taxa)
		contrataxa = randint(0,100)/100
		if(  contrataxa > taxa):
			threadLock.acquire()
			ambiente[self.posX][self.posY] += 1
			self.carry = 0
			ambiente[self.posX][self.posY] -= 2
			threadLock.release()
			print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), [self.posX, self.posY], ' - solta item - ', contrataxa, '>',taxa, '- L:', contL, '; I', contI)
			return False
		else:
			print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), [self.posX, self.posY], ' - não solta item - ', contrataxa, '<',taxa, '- L:', contL, '; I', contI)
			return True

	def moveToFocus(self):
		#self.decideMove()
		movX = self.focus[0]-self.posX
		movY = self.focus[1]-self.posY
		if( movX < 0):
			movX = -1
		elif( movX > 0):
			movX = 1
		if( movY < 0):
			movY = -1
		elif( movY > 0):
			movY = 1
		if ambiente[self.posX+movX][self.posY+movY] != 2 or ambiente[self.posX+movX][self.posY+movY] != 3 or ambiente[self.posX+movX][self.posY+movY] != 5:
			self.nextmove = [movX, movY]
			print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), '- indo a encontro de um item na posição', self.focus)
	
	def decideMove(self):
		contL = contI = 0
		
		#print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), ' - ', [[-RAIOVISAO, self.posX * -1], [RAIOVISAO, N-1 - self.posX]], '-', [ [-RAIOVISAO, self.posY * -1], [RAIOVISAO, M-1 - self.posY]])
		#Limites da Matriz Considerados
		lx = max( -RAIOVISAO, -self.posX)
		ly = max( -RAIOVISAO, -self.posY)

		Lx = min( RAIOVISAO, N-1 - self.posX)
		Ly = min( RAIOVISAO, M-1 - self.posY)
		#print( 'Ant', repr(self.nIt).zfill(3), ':it', repr(self.nIt).zfill(3), '- ', [ self.posX, self.posY],' - min', [RAIOVISAO, N-1 - self.posX], '- min', [ RAIOVISAO, M-1 - self.posY])
		# Verifica os Itens e suas posições
		posItens = []
		posVazios = []
		for i in range(lx, Lx):
			for j in range( ly, Ly):
				estadoLocal = ambiente[ self.posX+i][ self.posY+j]
				if( self.carry == 0):
					if (estadoLocal % 2) == 1 and (i != 0 or j != 0):
						#posItens.append( [self.posX+i,self.posY+j])
						posItens.append( [i,j])
						contI += 1
					else:
						contL += 1
				else:
					if (estadoLocal % 2) == 0 and (i != 0 or j != 0):
						#posItens.append( [self.posX+i,self.posY+j])
						posVazios.append( [i,j])
						contL += 1
					else:
						contI += 1


		lx = max( lx, -1)
		Lx = min( Lx, 1)
		ly = max( ly, -1)
		Ly = min( Ly, 1)
		#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), '-', [ self.posX, self.posY], ' - ', [lx, Lx], ';', [ly,Ly])
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
		
		if (contI > 0 and self.carry == 0):	#Item solitario na area de visão e formiga livre
			taxa = contI/((RAIOVISAO*RAIOVISAO + RAIOVISAO)*2)
			contrataxa = randint(0,100)/100
			if( contrataxa > taxa):
				#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), '-', contrataxa,'>', taxa, '; taxa=', contI,'/', ((RAIOVISAO*RAIOVISAO + RAIOVISAO)*2))
				return
			#Procurando Item para ir atras
			#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), '-', contrataxa, '<=', taxa, '; taxa=', contI,'/', ((RAIOVISAO*RAIOVISAO + RAIOVISAO)*2))	
			nVizinhos = np.zeros(contI)
			i=0
			for item in posItens:
				#verifica vizinhança de cada item
				if(item[1]-1 > 0):
					y = item[1]-1
					x = item[0]
					if(ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
						nVizinhos[i] += 1
				if(item[1]+1 <= M):
					y = item[1]+1
					x = item[0]
					if(ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
						nVizinhos[i] += 1
				if( item[0]-1 > 0):
					x = item[0]-1
					y = item[1]
					
					if(ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
						nVizinhos[i] += 1
					if( item[1]-1 > 0):
						y = item[1]-1
						if(ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
							nVizinhos[i] += 1
					if( item[1]+1 <= M):
						y = item[1]+1
						if(ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
							nVizinhos[i] += 1
				if( item[0]+1 <= N):
					x = item[0]+1
					y = item[1]
					if(ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
						nVizinhos[i] += 1
					if( item[1]-1 > 0):
						y = item[1]-1
						if(ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
							nVizinhos[i] += 1
					if( item[1]+1 <= M):
						y = item[1]+1
						if(ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
							nVizinhos[i] += 1
				i += 1
			#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), '-', posItens, '-', nVizinhos)

			menorV = 50
			for i in range(0, contI):
				if(nVizinhos[i] < menorV):
					menorV = nVizinhos[i]
			menoresV = []
			for i in range(0, contI):
				if nVizinhos[i] == menorV:
					menoresV.append(posItens[i])
			#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), '-', menoresV, '-', menorV)
			qualFoco = randint(0,len(menoresV)-1)
			self.focus = [menoresV[qualFoco][0]+self.posX, menoresV[qualFoco][1]+self.posY]
			self.haveFocus = True
			#Levy Flight
			print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), '- indo a encontro de um item na posição', self.focus, 'com', menorV,'vizinhos')
		elif(contL > 0 and self.carry == 2):
			taxa = contL/((RAIOVISAO*RAIOVISAO + RAIOVISAO)*2)
			contrataxa = randint(0,100)/100
			if( contrataxa < taxa):
				#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), '-', contrataxa,'>', taxa, '; taxa=', contI,'/', ((RAIOVISAO*RAIOVISAO + RAIOVISAO)*2))
				return
			#Procurando Item para ir atras
			#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), '-', contrataxa, '<=', taxa, '; taxa=', contI,'/', ((RAIOVISAO*RAIOVISAO + RAIOVISAO)*2))	
			nVizinhos = np.zeros(contL)
			i=0
			for vazios in posVazios:
				#verifica vizinhança de cada item
				if(vazios[1]-1 > 0):
					y = vazios[1]-1
					x = vazios[0]
					if(ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
						nVizinhos[i] += 1
				if(vazios[1]+1 <= M):
					y = vazios[1]+1
					x = vazios[0]
					if(ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
						nVizinhos[i] += 1
				if( vazios[0]-1 > 0):
					x = vazios[0]-1
					y = vazios[1]
					
					if(ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
						nVizinhos[i] += 1
					if( vazios[1]-1 > 0):
						y = vazios[1]-1
						if(ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
							nVizinhos[i] += 1
					if( vazios[1]+1 <= M):
						y = vazios[1]+1
						if(ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
							nVizinhos[i] += 1
				if( vazios[0]+1 <= N):
					x = vazios[0]+1
					y = vazios[1]
					if(ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
						nVizinhos[i] += 1
					if( vazios[1]-1 > 0):
						y = vazios[1]-1
						if(ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
							nVizinhos[i] += 1
					if( vazios[1]+1 <= M):
						y = vazios[1]+1
						if(ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
							nVizinhos[i] += 1
				i += 1
			#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), '-', posItens, '-', nVizinhos)

			maiorV = 0
			for i in range(0, contL):
				if(nVizinhos[i] > maiorV):
					maiorV = nVizinhos[i]
			maioresV = []
			for i in range(0, contL):
				if nVizinhos[i] == maiorV:
					maioresV.append(posVazios[i])
			#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), '-', menoresV, '-', menorV)
			qualFoco = randint(0,len(maioresV)-1)
			self.focus = [maioresV[qualFoco][0]+self.posX, maioresV[qualFoco][1]+self.posY]
			self.haveFocus = True
			#Levy Flight
			print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), '- indo a encontro de um espaço vazio na posição', self.focus, 'com', maiorV,'vizinhos')

	def move( self):
		threadLock.acquire() #lock ambiente
		k1 = abs(self.posX + self.nextmove[0])
		k2 = abs(self.posY + self.nextmove[1])
		print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), 'se move de', [self.posX, self.posY], ' para ', [k1, k2], '(', [self.nextmove[0],self.nextmove[1]], ')')
		#print('Ant',repr(self.nIt).zfill(3), ':it', repr(self.nIt).zfill(3), ':', k1, k2)
		if (k1 >= N or k2 >= M):
			print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(3), 'se move de', [self.posX, self.posY], ' para ', [k1, k2], 'se batendo na parede')
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
#print([N,M], N*M, NUM_ITENS) #OK
numIt = 0
main()
contaItens()
print('Finalizando')