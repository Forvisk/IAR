from noMovimento import NoMovimento
import numpy as np
import os

class AEstrela(object):
	"""docstring for AEstrela"""
	end = False
	nosVisitados = 0
	nIt = 0
	nNos = 0
	def __init__(self, ambiente):
		self.ambiente = ambiente
		self.size = self.ambiente.getDimensoes()
		self.mExplorado = np.zeros(self.size, dtype=int)

	def run(self, robo):
		#os.system('clear')
		self.posIni = robo.getInicio()
		self.posFim = robo.getFim()

		noInicial = NoMovimento(self.posIni, self.ambiente, [], self.nNos)
		self.listaNos = np.array([noInicial])
		self.nNos += 1

		self.fronteira = np.array([noInicial])
		#self.explorado = np.empty(0, dtype=object)
		self.gScore = np.full(self.size, np.inf)
		self.setGScore(self.posIni, 0)

		self.fScore = np.full(self.size, np.inf)
		self.setFScore(self.posIni, self.heuristc(self.posIni))

		while( self.fronteira.size > 0):
			atual = self.getMenorFScore()
			ind = atual[0]
			no = atual[1]
			pos = no.getPos()
			self.nosVisitados += 1
			if (pos[0] == self.posFim[0] and pos[1] == self.posFim[1]):
				self.end = True
				self.fronteira = np.empty(0, dtype=object)
				self.noFinal = no
			else:
				self.setAtual(pos)
				self.expande(no)
				self.fronteira = np.delete(self.fronteira, ind, 0)
				self.setNosAmbiente(pos)
		print('---------Fim A*---------')
		
	def expande(self, no):
		pos = no.getPos()
		moves = []
		if( pos[0]-1 >= 0):
			m = np.array( [pos[0]-1, pos[1]], dtype=int)
			moves.append(m)
		if( pos[0]+1 < self.size[0]):
			m = np.array( [pos[0]+1, pos[1]], dtype=int)
			moves.append(m)
		if( pos[1]-1 >= 0):
			m = np.array( [pos[0], pos[1]-1], dtype=int)
			moves.append(m)
		if( pos[1]+1 < self.size[1]):
			m = np.array( [pos[0], pos[1]+1], dtype=int)
			moves.append(m) 

		for m in moves:
			tentGS = self.getGScore(pos) + self.ambiente.getPeso(m)
			if tentGS < self.getGScore(m):
				self.setGScore(m, tentGS)
				self.setFScore(m, tentGS+self.heuristc(m))
				new = NoMovimento(m, self.ambiente, [no], self.nNos)
				self.nNos += 1
				self.fronteira = np.append(self.fronteira, new)
				self.listaNos = np.append(self.listaNos, new)
				self.setNosAmbiente(m)
				no.addProximo(new)

	def setNosAmbiente(self, pos):
		#print(pos)
		if self.mExplorado[pos[0]] [pos[1]] > 0:
			self.mExplorado[pos[0]] [pos[1]] = 3
		else:
			self.mExplorado[pos[0]] [pos[1]] = 1

	def setAtual(self, pos):
		self.mExplorado[pos[0]] [pos[1]] = 2
		self.printAmbiente()

	def getMenorFScore(self):
		it = ind = 0
		peso = np.inf
		for i in self.fronteira:
			pos = i.getPos()
			if peso > self.getFScore(pos):
				peso = self.getFScore(pos)
				ind = it
				no = i
			it += 1
		return [ind, no]

	def setGScore(self, pos, val):
		self.gScore[pos[0]][pos[1]] = val

	def getGScore(self, pos):
		return self.gScore[pos[0]][pos[1]]

	def setFScore(self, pos, val):
		self.fScore[pos[0]][pos[1]] = val

	def getFScore(self, pos):
		return self.fScore[pos[0]][pos[1]]

	def heuristc(self, pos):
		#Irei utilizar a distância em linha 'reta' entre o ponto pos e o destino
		#linha 'reta' é distância Manhattan (4-way)
		dist = 0
		atu = np.array(pos)
		nNos = 1
		#go = True
		#print(atu,end='')
		while( True):
			if atu[0] != self.posFim[0]:
				dif = self.posFim[0] - atu[0]
				if dif < 0:
					pasX = -1
				else:
					pasX = 1
				atu[0] += pasX
				dist += self.ambiente.getPeso(atu)
				nNos+=1
				#print('->'+str(atu),end='')
			if atu[1] != self.posFim[1]:
				dif = self.posFim[1] - atu[1]
				if dif < 0:
					pasY = -1
				else:
					pasY = 1
				atu[1] += pasY
				dist += self.ambiente.getPeso(atu)
				nNos+=1
				#print('->'+str(atu),end='')

			if atu[0] == self.posFim[0] and atu[1] == self.posFim[1]:
				#print('h(pos)='+str(dist/nNos))
				return dist/nNos

	def getMenorCaminho(self):
		if self.end:
			print('Resultado Busca A*')
			no = self.noFinal
			go = True
			first = True
			while (go):
				if first:
					listaNos = np.array([no])
					first = False
				else:
					listaNos = np.append(listaNos, no)
				ant = no.getAnterior()
				if len(ant) > 0:
					no = ant[0]
				else:
					go = False
			listaNos = np.flip(listaNos)
			for i in range(0, listaNos.size-1):
				listaNos[i].printNo()
				print('->', end='')
			i = listaNos.size-1
			listaNos[i].printNo()
			print('')
			print( 'Valor da Corrida: ' + str(self.noFinal.getDistancia()))
			print( 'Nos visitados no menor caminho: ' + str(self.noFinal.getNosCaminhados()))
			print( 'Nos Visitados no total: ' + str(self.nosVisitados))

	def printAmbiente(self):
		os.system('clear') or None
		print('A*-'+str(id(self)))
		print( 'Nos Visitados atualmente: ' + str(self.nosVisitados))
		print('Nós a expandir: '+str(self.fronteira.size))
		for line in self.mExplorado:
			for n in line:
				print('{:>2}'.format(n), end=' ')
			print('')