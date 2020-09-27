import numpy as np
from random import randint, seed, random
from math import log, exp

class SimulatedAnnealing(object):
	"""docstring for SimulatedAnnealing"""
	def __init__(self, instanciaSat):
		super(SimulatedAnnealing, self).__init__()
		self.instanciaSat = instanciaSat
		self.nClauses = self.instanciaSat.getNClauses()
		self.nvar = self.instanciaSat.getnvariaveis()

	def run(self, solucaoInicial, kmax, tempIni, tempFim, N, typeCooling):
		temp = tempIni
		solucao = solucaoInicial
		resultadoSolucao = self.instanciaSat.avalia(solucao)

		#melhor solução até agora
		melhorSolucao = solucao
		resultadoMelhorSolucao = resultadoSolucao
		i = 0
		while temp > tempFim:
			#print(temp)
			k = 0
			while k < kmax:
				k += 1
				newSolucao = self.getVizinho(solucao)
				resultadoNewSolucao = self.instanciaSat.avalia(newSolucao)
				if(resultadoNewSolucao[1]):
					print("SA solução perfeita", end=' - ')
					return (resultadoNewSolucao, newSolucao)
					#Resultado perfeito
				delta = resultadoNewSolucao[2] - resultadoSolucao[2]
				#print( resultadoNewSolucao, resultadoSolucao, delta, temp)
				if delta < 0:
					solucao = newSolucao
					resultadoSolucao = resultadoNewSolucao
					if resultadoNewSolucao[0] > resultadoMelhorSolucao[0]:
						melhorSolucao = newSolucao
						resultadoMelhorSolucao = resultadoNewSolucao
						#print("nova Melhor solução:" + str(resultadoMelhorSolucao) + ". T= "+str(temp))
				else:
					x = random()
					f = formulaP(temp, delta)
					#print("---")
					#print(x," < ",f, " ?")
					if x < f:
						solucao = newSolucao
						resultadoSolucao = resultadoNewSolucao
						#print("Nova solução "+str(resultadoSolucao)+". T= "+str(temp))
					#print("---")
			i += 1
			temp = temperatura(tempIni, tempFim, i, N, typeCooling)
			#print(temp)
		return (resultadoMelhorSolucao, melhorSolucao)

	def getVizinho(self, solucao):
		seed()
		pos = randint(1, self.nvar)
		new = solucao.copy()
		new[pos-1] = not new[pos-1]
		return new


	def getMediaVizinhos(self, solucaoInicial, nVizinhos):
		valor = 0
		resultadoSolucaoInicial = self.instanciaSat.avalia(solucaoInicial)
		for i in range(0,nVizinhos):
			vizinho = self.getVizinho(solucaoInicial)
			resultadoVizinho = self.instanciaSat.avalia(vizinho)
			valor += 1+resultadoVizinho[0]#/self.nClauses
		media = valor / nVizinhos
		return media

def temperatura(tempIni, tempFim, i, N, typeCooling):
	if typeCooling == 0:
		return temperatura0(tempIni, tempFim ,i, N)
	elif typeCooling == 1:
		return temperatura1(tempIni, tempFim ,i, N)
	elif typeCooling == 2:
		return temperatura2(tempIni, tempFim ,i, N)
	elif typeCooling == 3:
		return temperatura3(tempIni, tempFim ,i, N)
	else:
		print("ERRO: Cooling Schedule Invalido!")
		exit(1)

# Cooling Schedule 0
def temperatura0(tempIni, tempFim ,i, N):
	temp = tempIni - i*((tempIni-tempFim)/N)
	return temp

#Cooling Schedule 1
def temperatura1(tempIni, tempFim ,i, N):
	A = (tempFim / tempIni)**(i/N)
	#print(A)
	temp = tempIni * (A)
	#print (temp)
	return temp

#Cooling Schedule 2
def temperatura2(tempIni, tempFim ,i, N):
	A = (tempIni - tempFim)*(N+1)/N
	B = tempIni - A
	temp = A / (i+1) + B
	#print (temp)
	return temp

#Cooling Schedule 3
def temperatura3(tempIni, tempFim ,i, N):
	A = log(tempIni - tempFim)/log(N)
	temp = tempIni - (i ** A)
	#print (temp)
	return temp

def formulaP(temp, delta):
	if delta == 0: delta = 1
	temp = round(temp,6)
	#print(temp)
	if temp == 0: return 1
	#constBoltzmann = 1380649 * (10**-23)	#SI J/K (Joule by Kelvin)
	constBoltzmann = 1	#Quem sou eu para dizer qual o valor
	result = exp(-delta/(temp*constBoltzmann))
	return result