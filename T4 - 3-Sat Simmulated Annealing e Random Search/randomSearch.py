import numpy as np

class RandomSearch(object):
	"""docstring for RandomSearch"""

	def __init__(self, instanciaSat):
		super(RandomSearch, self).__init__()

		self.instanciaSat = instanciaSat

	def run(self, solucaoInicial):
		melhorSolucao = solucaoInicial
		resultado = self.avalia(melhorSolucao)
		nIt = 0
		while (nIt < 100):
			novaSolucao = self.geraSolucao(solucaoInicial)
			novoResultado = self.avalia(novaSolucao)
			if novoResultado > resultado:
				resultado = novoResultado
				melhorSolucao = novaSolucao
			nIt += 1
		return (resultado, melhorSolucao)

	def avalia(self, solucao):
		pass

	def geraSolucao(self):
		pass
