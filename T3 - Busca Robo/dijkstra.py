from noMovimento import NoMovimento
import numpy as np
import os

class Djikstra(object):
	end = False
	nosVisitados = 0
	nIt = 0
	nNos = 0
	"""docstring for Djikstra"""
	def __init__(self, ambiente):
		self.ambiente = ambiente
		self.size = self.ambiente.getDimensoes()
		self.mExplorado = np.zeros(self.size, dtype=int)

	def run(self, robo):
		self.posIni = robo.getInicio()
		self.posFim = robo.getFim()

		noInicial = NoMovimento(self.posIni, self.ambiente, [], self.nNos)
		self.listaNos = np.array([noInicial])
		self.nNos += 1

		self.fronteira = np.array([noInicial])
		self.explorado = np.empty(0, dtype=object)
		while(self.fronteira.size > 0):
			prioritNo = self.getPrioritNo()
			ind = prioritNo[0]
			no = prioritNo[1]
			pos = no.getPos()
			self.nosVisitados += 1
			if (pos[0] == self.posFim[0] and pos[1] == self.posFim[1]):
				self.end = True
				self.fronteira = np.empty(0, dtype=object)
				self.noFinal = no
			else:
				self.explorado = np.append(self.explorado, no)
				self.setAtual(pos)
				self.expande(no)
				self.fronteira = np.delete(self.fronteira, ind, 0)
				self.setNosAmbiente(pos)
		print('-------Fim Busca de Custo Uniforme-------')

	def expande(self, no):
		pos = no.getPos()
		moves = []
		if( pos[0]-1 >= 0):
			m = np.array( [pos[0]-1, pos[1]], dtype=int)
			if( not self.foiExplorado( m)):
				moves.append(m)
		if( pos[0]+1 < self.size[0]):
			m = np.array( [pos[0]+1, pos[1]], dtype=int)
			if( not self.foiExplorado( m)):
				moves.append(m)
		if( pos[1]-1 >= 0):
			m = np.array( [pos[0], pos[1]-1], dtype=int)
			if( not self.foiExplorado( m)):
				moves.append(m)
		if( pos[1]+1 < self.size[1]):
			m = np.array( [pos[0], pos[1]+1], dtype=int)
			if( not self.foiExplorado( m)):
				moves.append(m) 
		for m in moves:
			new = NoMovimento(m, self.ambiente, [no], self.nNos)
			self.nNos += 1
			self.fronteira = np.append(self.fronteira, new)
			self.listaNos = np.append(self.listaNos, new)
			self.setNosAmbiente(m)
			no.addProximo(new)

	def getPrioritNo(self):
		peso = np.inf
		it = ind = 0
		for i in self.fronteira:
			if peso > i.getDistancia():
				peso = i.getDistancia()
				no = i
				ind = it
			it+= 1
		return [ind, no]

	def setNosAmbiente(self, pos):
		#print(pos)
		if self.mExplorado[pos[0]] [pos[1]] > 0:
			self.mExplorado[pos[0]] [pos[1]] = 3
		else:
			self.mExplorado[pos[0]] [pos[1]] = 1

	def setAtual(self, pos):
		self.mExplorado[pos[0]] [pos[1]] = 2
		self.printAmbiente()

	def endAtual(self, pos):
		self.mExplorado[pos[0]] [pos[1]] = 3

	def foiExplorado(self, pos):
		if self.mExplorado[pos[0]][pos[1]] > 0:
			return True
		return False

	def getMenorCaminho(self):
		if self.end:
			print('Resultado busca de Custo Uniforme (Dijkstra)')
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
		print('Dijkstra-'+str(id(self)))
		print( 'Nos Visitados atualmente: ' + str(self.nosVisitados))
		print('Nós a expandir: '+str(self.fronteira.size))
		for line in self.mExplorado:
			for n in line:
				print('{:>2}'.format(n), end=' ')
			print('')