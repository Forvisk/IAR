from noMovimento import NoMovimento
import numpy as np
import os

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
		self.size = ambiente.getDimensoes()
		self.percorrido = np.zeros(self.size, dtype = int)
		self.nosAmbiente = np.full(self.size, -1)

	def run(self, robo):
		posIni = robo.getInicio()
		posFim = robo.getFim()
		noInicial = NoMovimento(posIni, self.ambiente, [], self.nNos)

		self.listaNos = np.array([noInicial])
		self.nNos += 1
		self.nextExpandir = np.array([noInicial])
		#print(self.nextExpandir)
		self.setNosAmbiente( 0, posIni, False)

		#while (self.nextExpandir.size > 0):
		while (True and self.it < self.nextExpandir.size):
			#print(self.nextExpandir.size)
			self.nosVisitados += 1
			#no = self.nextExpandir[0]
			no = self.nextExpandir[self.it]
			#print(no)
			#no.print()
			pos = no.getPos()
			if (pos[0] == posFim[0] and pos[1] == posFim[1]):
				self.setNosAmbiente(no.getIndice(), pos, False)
				self.noFinal = no
				self.end = True
				self.nextExpandir = np.empty(1)
				print('---Fim Busca em Largura---')
				return
			else:
				if(self.getPercorrido(no.pos) == 1):
					self.expand(no)
				self.removeAtual(no)
				'''
				for i in self.nextExpandir:
					i.print()
				'''
				#self.nextExpandir = np.delete(self.nextExpandir, 0, 0)
			self.it += 1
		print('---Fim Busca em Largura---')

	def expand(self, no):
		posNo = no.getPos()
		self.setAtual(posNo)
		#print('Expandindo o nó ', end='')
		#no.print()
		nextMove = np.array([], dtype=object)
		ant = no.getAnterior()
		if ant.size > 0:
			posAnt = ant[0].getPos()
		else:
			posAnt = np.array([-1,-1])

		if ((posNo[0]-1) >= 0):
			pos = np.array([posNo[0]-1 , posNo[1]])
			if not self.comparaPos(pos, posAnt):
				new = NoMovimento(pos, self.ambiente, [no], self.nNos)
				nextMove = np.append(nextMove ,[new])
				self.listaNos = np.append(self.listaNos, new)
				self.nNos += 1

		if ((posNo[0]+1) < self.size[0]):
			pos = np.array([posNo[0]+1 , posNo[1]])
			if not self.comparaPos(pos, posAnt):
				new = NoMovimento(pos, self.ambiente, [no], self.nNos)
				nextMove = np.append(nextMove ,[new])
				self.listaNos = np.append(self.listaNos, new)
				self.nNos += 1

		if (posNo[1]-1 >= 0):
			pos = np.array([posNo[0] , posNo[1]-1])
			if not self.comparaPos(pos, posAnt):
				new = NoMovimento(pos, self.ambiente, [no], self.nNos)
				nextMove = np.append(nextMove ,[new])
				self.listaNos = np.append(self.listaNos, new)
				self.nNos += 1

		if (posNo[1]+1 < self.size[1]):
			pos = np.array([posNo[0], posNo[1]+1])
			if not self.comparaPos(pos, posAnt):
				new = NoMovimento(pos, self.ambiente, [no], self.nNos)
				nextMove = np.append(nextMove ,[new])
				self.listaNos = np.append(self.listaNos, new)
				self.nNos += 1

		#print('Nos criados: ')
		for new in nextMove:
			#new.print()
			if self.getPercorrido(new.getPos()) > 0:
				self.nConflitos += 1
				conflito = self.comflitoNosAmbiente( new)
				if conflito[0]:
					#print('Substituido!')
					if not conflito[1]:
						self.nextExpandir = np.append(self.nextExpandir, [new])
					self.setNosAmbiente(new.getIndice(), new.getPos(), True)
					no.addProximo(new)
				#print('Fim conflito')
			else:
				self.nextExpandir = np.append(self.nextExpandir, [new])
				self.setNosAmbiente(new.getIndice(), new.getPos(), False)
				no.addProximo(new)
		#print('--------------------------------------')

	def setNosAmbiente(self, no, pos, jaPassado):
		'''if jaPassado:
			self.percorrido[pos[0]][pos[1]] = 3
		else:
			self.percorrido[pos[0]][pos[1]] = 1'''
		self.percorrido[pos[0]][pos[1]] += 1
		self.nosAmbiente[pos[0]][pos[1]] = no
		self.printAmbiente()

	def setAtual(self, pos):
		#self.percorrido[pos[0]][pos[1]] = 2
		self.percorrido[pos[0]][pos[1]] += 1

	def removeAtual( self, no):
		pos = no.getPos()
		#self.percorrido[pos[0]][pos[1]] = 3
		self.percorrido[pos[0]][pos[1]] += 1

	def getNosAmbiente(self, pos):
		ind = self.nosAmbiente[pos[0]][pos[1]]
		return self.listaNos[ind]

	def getPercorrido( self, pos):

		return self.percorrido[pos[0]][pos[1]]

	def comflitoNosAmbiente(self, newNo):
		#retorna verdadeiro se o no expandido subistitui o nó local
		pos = newNo.getPos()
		#print(pos)
		ret = [False, False]
		noLocal = self.getNosAmbiente(pos)

		#print('Conflito entre:')
		#newNo.print()
		#noLocal.print()

		if newNo.getDistancia() < noLocal.getDistancia():
			ret[0] = True
		elif  (newNo.getDistancia() == noLocal.getDistancia()):
			if newNo.getNosCaminhados() < noLocal.getNosCaminhados():
				ret[0] = True

		if ret:
			subs = noLocal.getProximos()
			if len(subs) > 0:
				ret[1] = True
				noLocal.substituiAnterior(newNo)
			'''
			else:
				for i in range(0 , self.nextExpandir.size):
					if self.nextExpandir[i].getIndice == noLocal.getIndice():
						self.nextExpandir = np.delete(self.nextExpandir, i, 0)
						break	
				'''
		return ret

	def getMenorCaminho(self):
		if self.end:
			
			#print(self.noFinal)
			no = self.noFinal
			#no.print()
			go = True
			first = True
			while (go):
				#no.print()
				if first:
					listaNos = np.array([no])
					print(listaNos)
					first = False
				else:
					listaNos = np.append(listaNos, no)
					#print(listaNos)
				ant = no.getAnterior()
				if len(ant) > 0:
					no = ant[0]
				else:
					go = False
			listaNos = np.flip(listaNos)
			print(listaNos)
			print(listaNos.size)
			for i in range(0, listaNos.size-1):
				listaNos[i].printNo()
				print('->', end='')
			i = listaNos.size-1
			listaNos[i].printNo()
			print('')
			print( 'Valor da Corrida: ' + str(self.noFinal.getDistancia()))
			print( 'Nos visitados no menor caminho: ' + str(self.noFinal.getNosCaminhados()))
			print( 'Nos Visitados no total: ' + str(self.nosVisitados))
			print( 'Numero de conflitos: ' + str(self.nConflitos))

	def printAmbiente(self):
		os.system('clear') or None
		print(id(self))
		print( 'Nos Visitados atualmente: ' + str(self.nosVisitados))
		print('Nós a expandir:')
		'''
		for n in self.nextExpandir:
			n.print()
		'''	
		for line in self.percorrido:
			for n in line:
				print('{:>2}'.format(n), end=' ')
			print('')
			
	def comparaPos(self, pos1, pos2):
		if pos1[0] == pos2[0]:
			if pos1[1] == pos2[1]:
				return True
		return False