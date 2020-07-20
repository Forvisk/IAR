import sys
import numpy as np
import scipy.misc as sm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import randint
import threading
import time
import imageio as img	# novo package de imagem
import math
from skimage import img_as_ubyte
#
# Voo de Levy
# Como melhorar:
# Melhorar o Determinismo
ALPHA = 20	# ñao pode ser 0
KA1 = 1
KA2 = 1
RAIOVISAO = 1

NUM_FORMIGAS = 25
N = 0
M = 0
NUM_ITENS = 0

NUM_ITERAC_POR_FORMIGA = 100000
SLEEP = False
NUM_ITERACAO = NUM_FORMIGAS * NUM_ITERAC_POR_FORMIGA


DIVTAXA = ((RAIOVISAO*2+1) * (RAIOVISAO*2+1)) -1

N_TIPO_ITENS = 1	# numero de grupos de itens
D_DADO = 1 			# dimensão do dado a ser trabalhado

agentes = []
itens = []

ambiente = []
itensAmbiente = []

threadLock = threading.Lock()
threadLockIteracao = threading.Lock()
numIt = 0

outputFile = "error"
outputVector = []

## Matriz
## vazio = 1
## item > 1
## formiga = -1
## formiga livre e item < -1
## formiga carregando item = -1
## formiga carregando item sobre um item < -1

class Item(object):
	idItem = 0
	dado = []
	grupo = 0
	pos = []

	def __init__(self, idItem, dado, grupo):
		self.idItem = idItem
		self.dado = dado
		self.grupo = grupo
		#print('Item '+str(self.idItem)+' = '+str(self.dado)+', '+str(self.grupo))

	def setPos(self,pos):
		self.pos = pos

	def getGrupo(self):
		return self.grupo

	def getDado(self):
		return self.dado

	def printItem(self):
		print('Item '+str(self.idItem)+' = '+str(self.dado)+', '+str(self.grupo)+'\n\tpossicao '+str(self.pos))

	def distancia(self, carga):
		global D_DADO
		valor = 0
		for i in range(0, D_DADO):
			valor += pow( self.dado[i] - carga[i], 2)
		#print('Distancia ', self.dado, ' e ', carga, ' - ',valor)
		return math.sqrt(valor)

class Animacao( object):
	def __init__(self, ax):
		global N_TIPO_ITENS
		global outputFile 
		global ambiente
		outputFile = "iteracoes/"+str(randint(0,1000))+'_rv'+str(RAIOVISAO)+'_nf'+str(NUM_FORMIGAS)
		ambiente[0][0] = N_TIPO_ITENS+1
		ambiente[0][1] = -(N_TIPO_ITENS+1)

		self.ax = ax
		self.matrice = ax.matshow((ambiente))
		plt.colorbar(self.matrice)
		
		ambiente[0][0] = 1
		ambiente[0][1] = 1

	def update(self, i):
		global ambiente
		self.matrice.set_array(ambiente)

def salvaImagem2(nIt):
	global N_TIPO_ITENS
	imagem = np.zeros([N,M,3]).astype(np.uint8)
	for x in range(0, N):
		for y in range(0,M):
			if abs(ambiente[x][y]) > 1:
				imagem[x][y][0] = int((abs(ambiente[x][y]) -1) * (200/N_TIPO_ITENS))
				imagem[x][y][1] = 255-255/int((abs(ambiente[x][y]) -1))
				imagem[x][y][2] = int((abs(ambiente[x][y]) -1) * (20/N_TIPO_ITENS))
			else:
				imagem[x][y] = [0,0,0]
	saving = outputFile+'-'+str(nIt).zfill(10)+'.png'
	#sm.imsave( saving, imagem)
	img.imwrite(saving, imagem, '.png')
	print('Main - saving',saving)

def contaItens():
	global ambiente
	contItens = 0
	contFormigas = 0
	pos = 0
	for i in range(0, N):
		for j in range(0, M):
			pos = ambiente[i][j]
			if ( abs(pos) > 1):
				contItens += 1
			if (pos < 0):
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
	carga = -1
	idCarga = -1
	
	def __init__(self, threadID, pos):
		threading.Thread.__init__(self)
		self.threadID = threadID+1
		self.posX = pos[0]
		self.posY = pos[1]
		self.haveFocus = False
		self.focus = [0,0]
		self.iteragiu = False
		self.carga = np.zeros(D_DADO)
		self.idCarga = -1

	def run(self):
		global numIt
		global NUM_ITERACAO
		global NUM_ITERAC_POR_FORMIGA
		global SLEEP
		while  len(threading.enumerate()) < NUM_FORMIGAS:
			continue
		print( 'Ant', repr(self.threadID).zfill(3), '0- Iniciando formiga em posicao [', self.posX, ',', self.posY, ']')
		while numIt < NUM_ITERACAO or self.idCarga >= 0 :
			if self.decide():
				if self.haveFocus:
					self.moveToFocus()
				else:
					self.decideMove()
				self.move()
			if SLEEP:
				time.sleep(0.001)

			threadLockIteracao.acquire()
			#print("Iteracao ",numIt)
			self.nIt = numIt
			numIt += 1
			threadLockIteracao.release()
			if self.nIt < NUM_ITERACAO:
				if self.nIt % (NUM_ITERAC_POR_FORMIGA/2) == 0:
					threadLock.acquire()
					threadLockIteracao.acquire()
					salvaImagem2(self.nIt)
					threadLockIteracao.release()
					threadLock.release()
			
		print( 'Ant', repr(self.threadID).zfill(3), 'X- Finalizando em posicao',[self.posX, self.posY])

	def decide( self):
		#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10),'decide')
		if ( abs(ambiente[ self.posX][self.posY]) > 1 and self.idCarga == -1 and not self.iteragiu):	# Item na posição da formiga
			if self.sobreItem():
				self.iteragiu = False
				return True
			else:
				self.iteragiu = True
		elif( abs(ambiente[ self.posX][self.posY]) == 1 and self.idCarga >= 0  and not self.iteragiu):	# Espaço vazio e formiga com carga
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
		#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10),'sobreItem')
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
					if (abs(ambiente[x][y]) > 1):
					#if (ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
						contI += 1
					else:
						contL += 1
		
		# PEGA ITEM
		taxa = (contI) / DIVTAXA
		contrataxa = randint( 0, 99)/100

		item = int(itensAmbiente[self.posX][self.posY])
		pegaItem = False
		valor = distanciaVizinhanca([self.posX, self.posY], itens[item].getDado())

		itemd = itens[int(itensAmbiente[self.posX][self.posY])].getDado()
		print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10),'sobreItem ', valor, self.carga, itemd,contrataxa)
		if valor <= 1:
			valor = 1
		elif valor != 0:
			valor = 1/pow(valor,2)
		else:
			valor = 0

		if( valor > contrataxa):
			pegaItem = True
		if( pegaItem):
			item = int(itensAmbiente[self.posX][self.posY])
			self.carga = itens[item].getDado()
			self.idCarga = item
			itens[item].setPos([-1,-1])
			ambiente[self.posX][self.posY] = -1

			return False
		else:
			return True
	
	def carregandoItem(self):
		#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10),'carregandoItem')
		if (self.posX != self.focus[0] and self.posY != self.focus[1]) and self.haveFocus:
			#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-carregandoItem-pos', [self.posX, self.posY],' com foco em',self.focus)
			return False
		self.haveFocus = False
		contL = contI = 0
		contL = contI = 0
		lx = max( -1, -self.posX)
		ly = max( -1, -self.posY)

		Lx = min( 1, N-1 - self.posX)
		Ly = min( 1, M-1 - self.posY)
		for x in range( self.posX+lx, self.posX+Lx+1):
			for y in range( self.posY+ly, self.posY+Ly+1):
				if ( x != self.posX or y != self.posY):
					if ( abs(ambiente[x][y]) > 1):
						contI += 1
					else:
						contL += 1
		# Alterada a taxa para ser relacionado ao raio da visão
		#	LARGA ITEM
		#taxa = 1-((contI) / 8)
		#taxa = 1-((contI) / DIVTAXA)
		contrataxa = randint(0,99)/100
		soltaItem = False
		valor = distanciaVizinhanca([self.posX, self.posY], self.carga)
		print( 'Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10),'carregandoItem ', valor, self.carga,contrataxa)
		
		if valor >= 1:
			valor = 1
		else:
			valor = pow(valor, 4)
		if( valor > contrataxa):
			soltaItem = True
		if( soltaItem):
			item = self.idCarga
			ambiente[self.posX][self.posY] = itens[item].getGrupo() *-1
			itensAmbiente[self.posX][self.posY] = item
			self.carga = []
			self.idCarga = -1
			return False
		else:
			return True

	def moveToFocus(self):
		movX = self.focus[0]-self.posX
		movY = self.focus[1]-self.posY
		if movX == 0 and movY == 0:
			self.haveFocus = False
			self.decideMove()
		if( movX < 0):
			movX = -1
		elif( movX > 0):
			movX = 1
		if( movY < 0):
			movY = -1
		elif( movY > 0):
			movY = 1
		if ambiente[self.posX+movX][self.posY+movY] > 0:
			self.nextmove = [movX, movY]
		else:
			if randint(0,3) > 0:
				self.nextmove = [0,0]
				self.decideMove()
				self.haveFocus = False
				#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10), self.carry, '-moveToFocus-pos', [ self.posX, self.posY],'perde o foco da posição',self.focus)
	
	def decideMove(self):
		#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10),'decideMove')
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
				if ( x != self.posX or y != self.posY):
					if (ambiente[x][y] == 1 or ambiente[x][y] == 3 or ambiente[x][y] == 5):
						posItens.append([x,y])
						contI += 1
					else:
						posVazios.append([x,y])
						contL += 1
		lx = max( lx, -1)
		Lx = min( Lx, 1)
		ly = max( ly, -1)
		Ly = min( Ly, 1)
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
		if (len( posItens) > 0 and self.idCarga < 0):	#Item solitario na area de visão e formiga livre
			self.getFocus(contI, posItens)
		elif( len( posVazios) > 0 and self.idCarga >= 0):
			self.getFocus(contL, posVazios)
			
	def move( self):
		#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10),'move')
		threadLock.acquire() #lock ambiente
		k1 = self.posX + self.nextmove[0]
		k2 = self.posY + self.nextmove[1]
		if (k1 >= N or k2 >= M):
			return
		elif(ambiente[ k1][ k2] > 0 ):
			ambiente[ self.posX][ self.posY] *= -1
			self.posX = k1
			self.posY = k2
			ambiente[ self.posX][ self.posY] *= -1
		threadLock.release()	#unlockambiente

	def getFocus(self, cont, vetorPontos):
		#print('Ant', repr(self.threadID).zfill(3), ':it', repr(self.nIt).zfill(10),'getFocus')
		taxa = cont/((RAIOVISAO*RAIOVISAO + RAIOVISAO)*2)
		contrataxa = randint(0,100)/100

		if( contrataxa > taxa):
			return
		nVizinhos = []
		i=0
		for item in vetorPontos:
			nVizinhos.append(vizinhanca(item))
			i += 1
		number = nVizinhos[0]
		for i in range(0, cont):
			if(nVizinhos[i] < number and self.idCarga < 0) or ( nVizinhos[i] > number and self.idCarga >= 0):
				number = nVizinhos[i]
		pontosEscolhidos = []
		for i in range(0, cont):
			if nVizinhos[i] == number:
				pontosEscolhidos.append(vetorPontos[i])
		qualFoco = randint(0,len(pontosEscolhidos)-1)
		
		#taxa = number/8
		taxa = number/DIVTAXA
		contrataxa = randint(0,100)/100

		if contrataxa > taxa and self.idCarga < 0:
			self.focus = pontosEscolhidos[qualFoco]
			self.haveFocus = True
			self.moveToFocus()
		elif contrataxa < taxa and self.idCarga >= 0:
			self.focus = pontosEscolhidos[qualFoco]
			self.haveFocus = True
			self.moveToFocus()
	
#### Classe Ant
def distanciaVizinhanca(pos, carga):
	global ambiente
	global itensAmbiente
	global agentes
	global ALPHA
	global RAIOVISAO
	valor = 0
	nVizinhos = 0
	D = 1
	lx = max( -RAIOVISAO, -pos[0])
	ly = max( -RAIOVISAO, -pos[1])
	Lx = min( RAIOVISAO, N-1 - pos[0])
	Ly = min( RAIOVISAO, M-1 - pos[1])
	for ix in range( lx,Lx):
		x = pos[0]+ix
		if( x >= 0) and ( x < N):		
			for iy in range( ly, Ly):
				y = pos[1]+iy
				if (y >= 0) and (y < M):
					#print([x,y])
					if( abs(ambiente[x][y]) > 1):
						item = int(itensAmbiente[x][y])
						d = itens[item].distancia(carga)
						D = max(d,D)
						if D == 0:
							D = 1
						v = 1 - d/D
						#print( itens[item].getDado(), carga, d, v)
						if v > 0:
							valor += v
						nVizinhos += 1
	#print(nVizinhos, valor)
	if nVizinhos > 0 and valor > 0:
		valor = 1/pow(nVizinhos,2) * valor
		return valor
	else:
		return 0

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

def criaAmbiente():
	global N
	global M
	global ambiente
	global itensAmbiente
	size = [N,M]
	ambiente = np.ones( size)
	itensAmbiente = np.zeros(size)

def posicionaItens():
	global N
	global M
	global ambiente
	global itensAmbiente
	global NUM_ITENS
	global itens
	for i in range(0,NUM_ITENS-1):
		passa = True
		while passa:
			x = randint(0, N-1)
			y = randint(0, M-1)
			#print([x,y])
			if itensAmbiente[x][y] == 0:
				ambiente[x][y] = itens[i].getGrupo()
				itensAmbiente[x][y] = i
				itens[i].setPos([x,y])
				passa = False
		#itens[i].printItem()
	pass

def criaItens():
	global NUM_ITENS
	i = 0
	#print(NUM_ITENS)
	for i in range(1, NUM_ITENS):
		#print([i,NUM_ITENS])
		itens.append( Item(i,1,1))

def lerArquivo( filename):
	global NUM_ITENS
	global N
	global M
	global N_TIPO_ITENS
	global D_DADO
	global agentes

	nItens = 0
	file =  open( filename)
	for line in file:
		if line[0] == '#' or line[0] == '\n' or line[0] == '':
			continue
		line = line.expandtabs(1)
		#print(line)
		dataLine = line.split(' ')
		dado = []
		#print(dataLine)
		for i in range(0,len(dataLine)-1):
			dado.append(float(dataLine[i]))
		grupo = int(dataLine[len(dataLine)-1])
		itens.append( Item(nItens, dado, grupo))
		N_TIPO_ITENS = max(N_TIPO_ITENS, grupo)
		nItens += 1
	file.close()
	if nItens > 0:
		NUM_ITENS = nItens
		D_DADO = len( itens[0].getDado())
		print(NUM_ITENS)
		return True
	return False

def inicio( argv):
	global N
	global M
	global NUM_ITENS
	global NUM_FORMIGAS
	global ambiente
	global agentes
	global outputFile
	if (len(argv) == 5):
		for i in range(1,5):
			if not argv[i].isnumeric():
				return False
		N = int(argv[1])
		M = int(argv[2])
		NUM_ITENS = int(argv[3])
		NUM_FORMIGAS = int(argv[4])
		criaItens()

		#return True
	elif ( len(argv) == 2):
		filename = argv[1]
		if filename.split('.')[1] == 'txt':
			if not lerArquivo( filename):
				return False
			print(NUM_ITENS)
			#itens[0].printItem()
			tam = int(math.sqrt(NUM_ITENS*10/4))
			N = tam
			M = tam
			NUM_FORMIGAS = int( NUM_ITENS/20)
			#return True
		else:
			return False
	outputFile = "iteracoes/"+str(randint(0,1000))+'_rv'+str(RAIOVISAO)+'_nf'+str(NUM_FORMIGAS)+'_ni'+str(NUM_ITENS)
	criaAmbiente()
	posicionaItens()
	iniciaFormigas()
	main()
	contaItens()
	return True

def iniciaFormigas():
	global agentes
	global N
	global M
	global NUM_FORMIGAS
	i = 0
	while True:
		x = randint(0, N-1)
		y = randint(0, M-1)
		#print(x, ',', y)
		if( ambiente[x][y] >= 0):
			ambiente[x][y] = -1 * ambiente[x][y]
			agentes.append( Ant( i, [x, y]))
			i += 1
		if( i >= NUM_FORMIGAS):
			break
	for i in range( 0, len(agentes)):
		agentes[i].start()

def main():
	global agentes
	fig, ax = plt.subplots()
	ani = Animacao(ax)
	
	ani = animation.FuncAnimation(fig, ani.update, frames=1, interval=1000)
	plt.show()

	for t in agentes:
		t.join()

# main()
print('Iniciando')
if (len(sys.argv) > 1):
	if not inicio( sys.argv):
		print("Entrada inválida!")
else:
	print("Favor iniciar com: ")
	print("num_linhas num_colunas num_itens num_formigas")
	print("ou")
	print("nome_arquivo.txt")
print("Size:["+str(N)+", "+str(M)+"]. Formigas:"+str(NUM_FORMIGAS))
print("Itens:"+str(NUM_ITENS)+". Dimensão dados:"+str(D_DADO)+". Grupos:"+str(N_TIPO_ITENS))
#print(ambiente)
#print(itensAmbiente)
contaItens()
print('Finalizando')