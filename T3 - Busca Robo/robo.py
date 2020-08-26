import numpy as np

class Robo(object):
	posIni = [-1,-1]
	"""docstring for Robo"""
	def __init__(self, ambiente):
		go = False
		while( not go):
			print('Coordenadas iniciais do robô "x y":')
			read = input()
			self.posIni = np.fromstring(read, dtype = int, sep = ' ')
			if len(self.posIni) != 2:
				print('Entrada errada, insira dois inteiros como no formato abaixo\n21 36')
				self.posIni = [-1,-1]
			else:
				go = True
			dimesoes = ambiente.getDimensoes()
			if self.posIni[0] >= dimesoes[0] or self.posIni[1] >= dimesoes[1] or self.posIni[0] < 0 or self.posIni[1] < 0:
				print('Ponto inicial fora do mapa, favor respeitar os limites.')
				go = False

	def print(self):
		print('Posição inicial do robo:' + str(self.posIni))


