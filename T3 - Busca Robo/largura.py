from noMovimento import NoMovimento
import numpy as np
import os
import sys
from termcolor import colored, cprint

class BuscaLargura(object):
	'''
	percorrido = []
	nosAmbiente = []
	ambiente = 0
	'''
	"""docstring for BuscaLargura"""
	end = False
	nosVisitados = 0
	nConflitos = 0
	it = 0
	nNos = 0

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
			no = self.fronteira[0]
			pos = no.getPos()
			self.nosVisitados += 1
			if (pos[0] == self.posFim[0] and pos[1] == self.posFim[1]):
				self.end = True
				#self.fronteira = np.empty(0, dtype=object)
				self.noFinal = no
				self.fronteira = np.delete(self.fronteira, 0, 0)
			else:
				if not self.end:
					self.explorado = np.append(self.explorado, no)
					self.setAtual(pos)
					self.expande(no)
					self.fronteira = np.delete(self.fronteira, 0, 0)
					self.setNosAmbiente(pos)
				elif (pos[0] == self.posFim[0] and pos[1] == self.posFim[1]):
					self.explorado = np.append(self.explorado, no)
					self.setAtual(pos)
					self.expande(no)
					self.fronteira = np.delete(self.fronteira, 0, 0)
					self.setNosAmbiente(pos)
				else:
					self.fronteira = np.delete(self.fronteira, 0, 0)
		#self.animation.stop()
		#self.animation.join()
		print('---Fim Busca em Largura---')
	
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
			if self.foiExplorado(m):
				#print('conflito')
				if self.setConflito(new):
					self.fronteira = np.append(self.fronteira, new)
					self.listaNos = np.append(self.listaNos, new)
					self.setNosAmbiente(m)
					no.addProximo(new)
			else:
				self.fronteira = np.append(self.fronteira, new)
				self.listaNos = np.append(self.listaNos, new)
				self.setNosAmbiente(m)
				no.addProximo(new)

	def setNosAmbiente(self, pos):
		#print(pos)
		if self.mExplorado[pos[0]] [pos[1]] > 1:
			self.mExplorado[pos[0]] [pos[1]] = 3
		else:
			self.mExplorado[pos[0]] [pos[1]] = 1
		#self.animation.atualiza(pos, 0)

	def setAtual(self, pos):
		self.mExplorado[pos[0]] [pos[1]] = 2
		self.printAmbiente()
		#self.animation.atualiza(pos, 16)

	def foiExplorado(self, pos):
		if self.mExplorado[pos[0]][pos[1]] > 0:
			return True
		return False

	def setConflito(self, new):
		pos = new.getPos()
		ret = False
		for i in self.listaNos():
			posOld = i.getPos()
			if pos[0] == posOld[0] and pos[1] == posOld[1] and i.ativo():
				if i.getDistancia() > new.getDistancia():
					i.substituiAnterior(new)
					if i.getAnterior.size == 0:
						ret = True
					#else: print('Já Expandido')
					
		return ret

	def getMenorCaminho(self):
		if self.end:
			print('Resultado Busca em Largura')
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
		print('Largura-'+str(id(self)))
		print( 'Nos Visitados atualmente: ' + str(self.nosVisitados))
		print('Nós a expandir: '+str(self.fronteira.size))
		i = 0
		for line in self.mExplorado:
			j = 0
			for n in line:
				c = self.ambiente.getCaracter([i,j])
				if (i == self.posFim[0] and j == self.posFim[1]):
					cprint(c[0],c[1], 'on_magenta', end=' ')
				else:
					highlight = ['','on_cyan','on_red', 'on_white']
					if n == 0:
						cprint(c[0],c[1], end=' ')
					else:
						cprint(c[0],c[1], highlight[n], end=' ')
				j+=1
			print('')
			i+=1
