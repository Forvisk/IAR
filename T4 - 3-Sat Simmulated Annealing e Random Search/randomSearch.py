import numpy as np
from random import randint, seed

class RandomSearch(object):
	"""docstring for RandomSearch"""

	def __init__(self, instanciaSat):
		super(RandomSearch, self).__init__()

		self.instanciaSat = instanciaSat
		self.nclauses = self.instanciaSat.getNClauses()
		self.nvar = self.instanciaSat.getnvariaveis()
		print (self.nclauses)

	def run(self, solucaoInicial):
		#self.instanciaSat.print()
		melhorSolucao = solucaoInicial
		resultado = self.instanciaSat.avalia(melhorSolucao)
		nIt = 0
		while (nIt < 1000):
			novaSolucao = self.geraSolucao(solucaoInicial)
			novoResultado = self.instanciaSat.avalia(novaSolucao)
			if novoResultado[0] > resultado[0]:
				#print("Melhor solucao: " +str(resultado)+" < "+str(novoResultado))
				resultado = novoResultado
				melhorSolucao = novaSolucao
			nIt += 1
		return (resultado, melhorSolucao)


	def geraSolucao(self, solucaoAnterior):
		seed()
		pos = randint(1, self.nvar)
		new = solucaoAnterior.copy()
		new[pos-1] = not new[pos-1]
		#print("Flip "+str(pos-1)+" to "+str(new[pos-1])+".")
		return new


		
