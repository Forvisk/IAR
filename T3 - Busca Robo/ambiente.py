import numpy as np

class Ambiente(object):
	mapa = []
	peso = []
	caminhado = []
	size = [0,0]

	def __init__(self, filename):

		with open(filename) as f:
			read_data = f.readlines()
			#print(read_data)
			for line in read_data:
				#print(line)
				lineData = np.fromstring(line, dtype = int, sep = ' ')
				self.mapa.append(lineData)
		f.close()
		#print(self.mapa)

		#checking if ambiente é ok
		self.size[0] = len(self.mapa)
		if self.size[0] == 0:
			print('Ambiente de entrada falho!')
			exit()
		self.size[1] = len(self.mapa[0])
		for line in self.mapa:
			if len(line) != self.size[1]:
				print('Ambiente de entrada falho!')
				exit()
		#self.print()
		self.caminhado = np.zeros(self.size)

	def print(self):
		print('Tamanho: '+str(self.size[0])+', '+str(self.size[1]))
		for line in self.mapa:
			for n in line:
				print('{:>2}'.format(n), end=' ')
			print('')

	def printPeso(self):
		print('Tamanho: '+str(self.size[0])+', '+str(self.size[1]))
		for line in self.peso:
			for n in line:
				print('{:>2}'.format(n), end=' ')
			print('')

	def setPesos(self, vetorPeso):
		for i in range(0, self.size[0]):
			new = []
			for j in range(0, self.size[1]):
				new.append(vetorPeso[(self.mapa[i][j])])
			self.peso.append(new)

	def getDimensoes(self):
		return (self.size)

	def getPeso(self, pos):
		return self.peso[pos[0]][pos[1]]