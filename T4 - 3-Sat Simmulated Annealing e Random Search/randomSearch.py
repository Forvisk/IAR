import numpy as np
from random import randint, seed

class RandomSearch(object):
	"""docstring for RandomSearch"""

	def __init__(self, instanciaSat):
		super(RandomSearch, self).__init__()

		self.instanciaSat = instanciaSat
		self.nclauses = self.instanciaSat.getNClauses()
		self.nvar = self.instanciaSat.getnvariaveis()
		#print (self.nclauses)

	def run(self, solucaoInicial, k):
		#self.instanciaSat.print()
		melhorSolucao = solucaoInicial
		resultado = self.instanciaSat.avalia(melhorSolucao)
		convergencia = []
		nIt = 0
		self.flipAnt = 0
		while (nIt < k):
			#novaSolucao = self.geraSolucao(solucaoInicial)
			novaSolucao = self.instanciaSat.geraSolucao()
			novoResultado = self.instanciaSat.avalia(novaSolucao)
			convergencia.append([nIt, novoResultado[0]])
			if novoResultado[1]:
				print("RS solução perfeita", end=' - ')
				#Melhor solução possivel
				return (novoResultado, novaSolucao, convergencia)
			if novoResultado[0] > resultado[0]:
				#print("Melhor solucao: " +str(resultado)+" < "+str(novoResultado))
				convergencia.append([nIt, novoResultado[0]])
				resultado = novoResultado
				melhorSolucao = novaSolucao
			nIt += 1
		return (resultado, melhorSolucao, convergencia)


	def geraSolucao(self, solucaoAnterior):
		seed()
		pos = randint(1, self.nvar)
		while pos == self.flipAnt:
			pos = randint(1, self.nvar)
		#print(pos)
		self.flipAnt = pos
		new = solucaoAnterior.copy()
		new[pos-1] = not new[pos-1]
		#print("Flip "+str(pos-1)+" to "+str(new[pos-1])+".")
		return new


		
