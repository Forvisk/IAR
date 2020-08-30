import numpy as np

class Robo(object):
	"""docstring for Robo"""
	def __init__(self, ambiente):
		go = False
		while( not go):
			print('Coordenadas iniciais do robô "x y":')
			read = input()
			self.posIni = np.fromstring(read, dtype = int, sep = ' ')
			if len(self.posIni) != 2:
				print('Entrada errada, insira dois inteiros como no formato abaixo\n21 36')
			else:
				go = True
			dimesoes = ambiente.getDimensoes()
			if self.posIni[0] >= dimesoes[0] or self.posIni[1] >= dimesoes[1] or self.posIni[0] < 0 or self.posIni[1] < 0:
				print('Ponto inicial fora do mapa, favor respeitar os limites.')
				go = False
		go = False
		while( not go):
			print('Coordenadas de destino do robô "x y":')
			read = input()
			self.posFim = np.fromstring(read, dtype = int, sep = ' ')
			if len(self.posFim) != 2:
				print('Entrada errada, insira dois inteiros como no formato abaixo\n21 36')
			else:
				go = True
			dimesoes = ambiente.getDimensoes()
			if self.posFim[0] >= dimesoes[0] or self.posFim[1] >= dimesoes[1] or self.posFim[0] < 0 or self.posFim[1] < 0:
				print('Ponto final fora do mapa, favor respeitar os limites.')
				go = False

	def print(self):
		print('Posição inicial do robo:' + str(self.posIni))
		print('Destino do robo:' + str(self.posFim))

	def getInicio(self):
		return self.posIni

	def getFim(self):
		return self.posFim


