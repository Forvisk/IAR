import numpy as np

class Ambiente(object):
	mapa = []
	X = 0
	Y = 0

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
		self.Y = len(self.mapa)
		if self.Y == 0:
			print('Ambiente de entrada falho!')
			exit()
		self.X = len(self.mapa[0])
		for line in self.mapa:
			if len(line) != self.X:
				print('Ambiente de entrada falho!')
				exit()
		self.print()

	def print(self):
		print('Tamanho: '+str(self.X)+', '+str(self.Y))
		for line in self.mapa:
			for n in line:
				print(n, end=' ')
			print('')

	def getDimensoes(self):
		return (self.X, self.Y)