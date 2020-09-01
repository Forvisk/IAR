from noMovimento import NoMovimento
import numpy as np
import os
import sys
from termcolor import colored, cprint

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
				pos = listaNos[i].getPos()
				self.mExplorado[pos[0]][pos[1]] = 4
			self.mExplorado[self.posIni[0]][self.posIni[1]] = 5
			self.mExplorado[self.posFim[0]][self.posFim[1]] = 5
			i = listaNos.size-1
			listaNos[i].printNo()
			print('')
			print( 'Valor da Corrida: ' + str(self.noFinal.getDistancia()))
			print( 'Nos visitados no menor caminho: ' + str(self.noFinal.getNosCaminhados()))
			print( 'Nos Visitados no total: ' + str(self.nosVisitados))

			i = 0
			for line in self.mExplorado:
				j = 0
				for n in line:
					c = self.ambiente.getCaracter([i,j])
					if self.mExplorado[i][j] == 4:
						cprint(c[0],c[1],'on_white', end=' ')
					elif self.mExplorado[i][j] == 5:
						cprint(c[0],c[1],'on_cyan', end=' ')
					else:
						cprint(c[0],c[1], end=' ')
					j+=1
				print('')
				i+=1

	
	def printAmbiente(self):
		os.system('clear') or None
		print('Dijkstra-'+str(id(self)))
		print( 'Nos Visitados atualmente: ' + str(self.nosVisitados))
		print('Nós a expandir: '+str(self.fronteira.size))
		i = 0
		for line in self.mExplorado:
			j = 0
			for n in line:
				c = self.ambiente.getCaracter([i,j])
				if i == self.posFim[0] and j == self.posFim[1]:
					cprint(c[0],c[1], 'on_magenta', end=' ')
				else:
					highlight = ['','on_cyan','on_red', 'on_white']
					if n == 0:
						cprint(c[0],c[1], end='')
					else:
						cprint(c[0],c[1], highlight[n], end='')
				j+=1
			print('')
			i+=1
		#time.sleep(1)
		input()
