import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import threading

class Animation(threading.Thread):
	"""docstring for animation"""
	def __init__(self, ambiente, i):
		threading.Thread.__init__(self)
		self.threadId = i
		self.ambiente = np.array(ambiente.getMatriz())
		self.running = True
		self.fig, self.ax = plt.subplots()
		self.mat = self.ax.matshow(self.ambiente)
		ani = animation.FuncAnimation(self.fig, self.update, interval=500, save_count=50)
		plt.show()

	def run(self):
		'''aux = self.ambiente[0][0]
		aux2 = self.ambiente[0][1]
		self.ambiente[0][0] = 0
		self.ambiente[0][1] = np.amax(self.ambiente)+1'''
		#self.ambiente[0][0] = aux
		#self.ambiente[0][1] = aux2

		while self.running:
			continue


	def atualiza(self, pos, estado):
		self.ambiente[pos[0]][pos[1]] = estado
		self.update(estado)

	def update(self, data):
		self.mat.set_data(self.ambiente)
		return self.mat

	def stop(self):
		self.running = False

	def setInicio(self, pos):
		self.ambiente[pos[0]][pos[1]] = 0
		self.update(0)

	def setFim(self, pos):
		self.ambiente[pos[0]][pos[1]] = 0
		self.update(0)



		