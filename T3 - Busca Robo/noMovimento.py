import numpy as np

class NoMovimento:
	"""docstring for NoMovimento"""
	pos = [-1,-1]
	caminhado = 0
	nosCaminhados = 0
	#anterior = []

	def __init__(self, pos, ambiente, anterior, indice):
		self.indice = indice
		self.pos = np.array(pos)
		if len(anterior) != 0:
			self.anterior = np.array(anterior)
			self.caminhado = anterior[0].getDistancia() + ambiente.getPeso(self.pos)
			self.nosCaminhados = anterior[0].getNosCaminhados() + 1
		else:
			#self.caminhado = ambiente.getPeso(self.pos)
			self.anterior = np.empty(0, dtype=object)
			self.caminhado = 0
		self.proximos = np.empty(0, dtype=object)

	def print(self):
		print(id(self))
		print(self.pos)
		print('Caminhado '+str(self.caminhado))

	def printNo(self):
		print(self.pos, end='')

	def getPos(self):
		return self.pos

	def getIndice(self):
		return self.indice

	def getDistancia(self):
		return self.caminhado

	def getNosCaminhados(self):
		return self.nosCaminhados

	def getProximos(self):
		return self.proximos

	def getAnterior(self):
		return self.anterior

	def substituiAnterior(self, new):
		difCaminhado = self.caminhado - new.getDistancia()
		difNosCaminhados = self.nosCaminhados - new.getNosCaminhados()
		for n in self.proximos:
			new.addProximo(n)
			n.atualizaAnterior(new, difCaminhado, difNosCaminhados)
		self.proximos = []

	def addProximo(self, no):
		self.proximos = np.append(self.proximos, [no])

	def atualizaAnterior(self, new, difCaminhado, difNosCaminhados):
		self.anterior = np.array([new])
		self.caminhado -= difCaminhado
		self.nosCaminhados -= difNosCaminhados
		for n in self.proximos:
			n.atualizaCaminhoNo(difCaminhado, difNosCaminhados)


	def atualizaCaminhoNo(self, difCaminhado, difNosCaminhados):
		self.caminhado -= difCaminhado
		self.nosCaminhados -= difNosCaminhados
		for n in self.proximos:
			n.atualizaCaminhoNo(difCaminhado, difNosCaminhados)