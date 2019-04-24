import numpy as np
import scipy.misc as sm
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
NUM_ITERAC_POR_FORMIGA = 100000
NUM_ITENS = (N*M*PORCENT_ITENS)/100
NUM_FORMIGAS = 10
RAIOVISAO = 5
NUM_ITERACAO = NUM_FORMIGAS * NUM_ITERAC_POR_FORMIGA
SLEEP = False

ambiente = []
agentes = []
threadLock = threading.Lock()
threadLockIteracao = threading.Lock()
numIt = 0
outputFile = "iteracoes/"+str(randint(0,1000))+'_rv'+str(RAIOVISAO)+'_nf'+str(NUM_FORMIGAS)

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

def salvaImagem():
	outputFile = "iteracoes/"+str(randint(0,1000))+'_rv'+str(RAIOVISAO)+'_nf'+str(NUM_FORMIGAS)
	nIt = numIt
	imagem = ambiente*25
	saving = outputFile+'-'+str(nIt).zfill(10)+'.png'
	sm.imsave( saving, imagem)
	while nIt < NUM_ITERACAO:
		time.sleep(10)
		threadLockIteracao.acquire()
		nIt = numIt
		imagem = ambiente*25
		saving = outputFile+'-'+str(nIt).zfill(10)+'.png'
		sm.imsave( saving, imagem)
		threadLockIteracao.release()
		print('Main - saving',saving)
	print('Finalizando Save')

def salvaImagem2():
	nIt = numIt
	imagem = ambiente * 25
	saving = outputFile+'-'+str(nIt).zfill(10)+'.png'
	sm.imsave( saving, imagem)
	print('Main - saving',saving)

def main():
	fig, ax = plt.subplots()
	ani = Animacao(ax)
	#print(ambiente)
	inicializa()
	
	ani = animation.FuncAnimation(fig, ani.update, frames=1, interval=1000)
	plt.show()
	#salvaImagem()
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
		while numIt < NUM_ITERACAO:
			print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry,'-0pos',[self.posX, self.posY])
			if self.decide():
				if self.haveFocus:
					self.moveToFocus()
				else:
					self.decideMove()
				self.move()
			if SLEEP:
				time.sleep(0.001)
			print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry,'-zpos',[self.posX, self.posY])
			threadLockIteracao.acquire()
			self.nIt = numIt

			if self.nIt % 500 == 0:
				threadLock.acquire()
				salvaImagem2()
				threadLock.release()

			numIt += 1
			print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10))
			threadLockIteracao.release()
		print( 'Ant', repr(self.threadID).zfill(3), 'X- Finalizando em posicao',[self.posX, self.posY])

	def decide( self):
		print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10),'decide')
		if (ambiente[ self.posX][self.posY] == 3 and self.carry == 0 and not self.iteragiu):	# Item na posição da formiga
			if self.sobreItem():
				self.iteragiu = False
				return True
			else:
				self.iteragiu = True
		elif(ambiente[ self.posX][self.posY] == 4 and self.carry == 2  and not self.iteragiu):
			if self.carregandoItem():
				self.iteragiu = False
				return True
			else:
				self.iteragiu = True
		else:	# Movimento
			self.iteragiu = False
			return True
		return False

	def sobreItem( self):
		if (self.posX != self.focus[0] and self.posY != self.focus[1]) and self.haveFocus:
			#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-sobreItem-pos', [self.posX, self.posY],' com foco em',self.focus)
			return False
		self.haveFocus = False
		contL = contI = 0
		lx = max( -1, -self.posX)
		ly = max( -1, -self.posY)
		Lx = min( 1, N-1 - self.posX)
		Ly = min( 1, M-1 - self.posY)
		#print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-', [ self.posX, self.posY],'; Lim x', [lx,Lx], '; LimY',[ly,Ly])
		for x in range( self.posX+lx, self.posX+Lx+1):
			for y in range( self.posY+ly, self.posY+Ly+1):
				#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-',[x,y])
				if ( x != self.posX or y != self.posY):
					if (ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
						contI += 1
					else:
						contL += 1
		taxa = (contI) / 8
		#print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, ' - livre', contL, '; itens', contI, '; taxa', taxa)
		contrataxa = randint(0,100)/100
		if(  contrataxa >= taxa):
			print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10),'sobreItem - threadLock')
			threadLock.acquire()
			if( ambiente[self.posX][self.posY] == 3):
				ambiente[self.posX][self.posY] = 4
				self.carry = 2
			threadLock.release()
			#print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry,'-sobreItem-pos', [self.posX, self.posY], '- pega item -', contrataxa, '>',taxa, '; L:', contL, '; I:', contI)
			return False
		else:
			#print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry,'-sobreItem-pos', [self.posX, self.posY], '- não pega item -', contrataxa, '<',taxa, '; L:', contL, '; I:', contI)
			return True
		
	def carregandoItem(self):
		if (self.posX != self.focus[0] and self.posY != self.focus[1]) and self.haveFocus:
			#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-carregandoItem-pos', [self.posX, self.posY],' com foco em',self.focus)
			return False
		self.haveFocus = False
		contL = contI = 0
		#print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, 'carregando item')
		contL = contI = 0
		lx = max( -1, -self.posX)
		ly = max( -1, -self.posY)

		Lx = min( 1, N-1 - self.posX)
		Ly = min( 1, M-1 - self.posY)
		#print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-', [ self.posX, self.posY],'; Lim x', [lx,Lx], '; LimY',[ly,Ly])
		for x in range( self.posX+lx, self.posX+Lx+1):
			for y in range( self.posY+ly, self.posY+Ly+1):
				#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-',[x,y])
				if ( x != self.posX or y != self.posY):
					if (ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
						contI += 1
					else:
						contL += 1
		taxa = 1-((contI) / 8)
		contrataxa = randint(0,100)/100

		if(  contrataxa > taxa):
			print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10),'carregandoItem - threadLock')
			threadLock.acquire()
			if( ambiente[self.posX][self.posY] == 4):
				ambiente[self.posX][self.posY] = 3
				self.carry = 0
			threadLock.release()
			#print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry,'-carregandoItem-pos:', [self.posX, self.posY], '- solta item -', contrataxa, '>',taxa, '; L:', contL, '; I:', contI)
			return False
		else:
			#print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry,'-carregandoItem-pos:', [self.posX, self.posY], '- não solta item -', contrataxa, '<',taxa, '; L:', contL, '; I:', contI)
			return True

	def moveToFocus(self):
		print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10),'moveToFocus')
		movX = self.focus[0]-self.posX
		movY = self.focus[1]-self.posY
		if movX == 0 and movY == 0:
			self.haveFocus = False
			self.decideMove()
		#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-moveToFocus-',[movX,movY],'=',self.focus, '-',[self.posX,self.posY])
		if( movX < 0):
			movX = -1
		elif( movX > 0):
			movX = 1
		if( movY < 0):
			movY = -1
		elif( movY > 0):
			movY = 1
		if ambiente[self.posX+movX][self.posY+movY] < 2:
			self.nextmove = [movX, movY]
			#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-moveToFocus- pos:',[self.posX,self.posY],'indo a encontro da posição', self.focus)
		else:
			if randint(0,3) > 0:
				self.nextmove = [0,0]
				self.decideMove()
				self.haveFocus = False
				print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-moveToFocus-pos', [ self.posX, self.posY],'perde o foco da posição',self.focus)
		
	def decideMove(self):
		print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10),'decideMove')
		contL = 0
		contI = 0
		lx = max( -RAIOVISAO, -self.posX)
		ly = max( -RAIOVISAO, -self.posY)
		Lx = min( RAIOVISAO, N-1 - self.posX)
		Ly = min( RAIOVISAO, M-1 - self.posY)
		posItens = []
		posVazios = []
		for x in range( self.posX+lx, self.posX+Lx+1):
			for y in range( self.posY+ly, self.posY+Ly+1):
				#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-',[x,y])
				if ( x != self.posX or y != self.posY):
					if (ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
						posItens.append([x,y])
						contI += 1
					else:
						posVazios.append([x,y])
						contL += 1
		#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-decideMove-pos', [ self.posX, self.posY], ';itens',contI,posItens)
		#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-decideMove-pos', [ self.posX, self.posY], ';vazios',contL,posVazios)
		lx = max( lx, -1)
		Lx = min( Lx, 1)
		ly = max( ly, -1)
		Ly = min( Ly, 1)
		#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-', [ self.posX, self.posY], ' - ', [lx, Lx], ';', [ly,Ly])
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
		if self.haveFocus:
			return
		if (len( posItens) > 0 and self.carry == 0):	#Item solitario na area de visão e formiga livre
			self.getFocus(contI, posItens)
		elif( len( posVazios) > 0 and self.carry == 2):
			self.getFocus(contL, posVazios)
			
	def move( self):
		print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10),'move - threadLock')
		threadLock.acquire() #lock ambiente
		k1 = self.posX + self.nextmove[0]
		k2 = self.posY + self.nextmove[1]
		#print('Ant',repr(self.nIt).zfill(10), self.carry, ':it', repr(self.nIt).zfill(10), self.carry, ':', k1, k2)
		if (k1 >= N or k2 >= M):
			return
			#print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-move- se move de', [self.posX, self.posY], ' para ', [k1, k2], 'se batendo na parede')
		elif(ambiente[ k1][ k2] < 2 ):
			#( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-move- se move de', [self.posX, self.posY], ' para ', [k1, k2], '(', [self.nextmove[0],self.nextmove[1]], ')')
			ambiente[ self.posX][ self.posY] -= (2 + self.carry)
			self.posX = k1
			self.posY = k2
			ambiente[ self.posX][ self.posY] += (2 + self.carry)
		threadLock.release()	#unlockambiente

	def getFocus(self, cont, vetorPontos):
		print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10),'getFocus')
		taxa = cont/((RAIOVISAO*RAIOVISAO + RAIOVISAO)*2)
		contrataxa = randint(0,100)/100

		if( contrataxa > taxa):
			#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-getFocus-', contrataxa,'>', taxa, '; taxa=', cont,'/', ((RAIOVISAO*RAIOVISAO + RAIOVISAO)*2))
			return
		nVizinhos = []
		i=0
		for item in vetorPontos:
			nVizinhos.append(vizinhanca(item))
			i += 1
		number = nVizinhos[0]
		for i in range(0, cont):
			if(nVizinhos[i] < number and self.carry == 0) or ( nVizinhos[i] > number and self.carry == 2):
				number = nVizinhos[i]
		pontosEscolhidos = []
		for i in range(0, cont):
			if nVizinhos[i] == number:
				pontosEscolhidos.append(vetorPontos[i])
		qualFoco = randint(0,len(pontosEscolhidos)-1)
		#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-getFocus-pos', [ self.posX, self.posY], pontosEscolhidos,':',qualFoco,';nv',number)
		taxa = number/8
		contrataxa = randint(0,100)/100
		#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-getFocus-',contrataxa,taxa)
		if contrataxa > taxa and self.carry == 0:
			self.focus = pontosEscolhidos[qualFoco]
			self.haveFocus = True
			#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-decideMove-pos', [ self.posX, self.posY], 'indo a encontro de um item na posição', self.focus)
			self.moveToFocus()
		elif contrataxa < taxa and self.carry == 2:
			self.focus = pontosEscolhidos[qualFoco]
			self.haveFocus = True
			#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-getFocus-pos', [ self.posX, self.posY], 'indo a encontro de um espaço vazio na posição', self.focus)
			self.moveToFocus()

		
		#Levy Flight
		#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-getFocus- indo para a posição', self.focus, 'com', menorV,'vizinhos')
	
#
#### Classe Ant

def vizinhanca(ponto):
	nVizinhos = 0
	for ix in range(-1,2):
		x = ponto[0]+ix
		if( x >= 0) and ( x < N):		
			for iy in range(-1,2):
				y = ponto[1]+iy
				if (y >= 0) and (y < M):
					#print([x,y])
					if(ambiente[x][y] % 2 == 1):
						nVizinhos += 1
	return nVizinhos

print('Iniciando')
size = [N,M]
ambiente = np.zeros( size)
#print([N,M], N*M, NUM_ITENS) #OK
numIt = 0
main()
contaItens()
print('Finalizando')