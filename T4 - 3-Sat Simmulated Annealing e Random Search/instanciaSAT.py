import numpy as np
from random import randint, seed

class InstanciaSAT(object):
	"""docstring for InstanciaSAT"""
	nVariaveis = 0
	varByClause = 0

	def __init__(self, filename):
		super(InstanciaSAT, self).__init__()

		self.filename = filename
		clauses = []
		with open(self.filename) as f:
			readData = f.readlines()
			state = 0
			for line in readData:
				if state == 0:
					if 'clause length' in line:
						dadosL = line.split(sep=' ')
						#print(dadosL)
						self.varByClause = int(dadosL[7])
					if line[0] == 'p':
						state += 1
						dadosP = line.split(sep=' ')
						#print(dadosP)
						self.nVariaveis = int(dadosP[2])
						self.nClausulas = int(dadosP[4])
				elif state == 1:
					if self.varByClause == 0:
						print("Erro na leitura do Arquivo!\nArquivo inválido!")
						exit()
					#print(line)
					if line[0] != '%':
						lineData = np.fromstring(line, dtype = int, sep = ' ')
						#print(lineData)
						clause = np.empty(0, dtype = int)
						for i in range(0, self.varByClause):
							clause = np.append(clause, lineData[i])
						#print(clause)
						clauses.append(clause)
					else: break
		f.close()
		#print(clauses)
		if self.nClausulas != len(clauses):
			print('Erro na leitura do Arquivo!')
			print(str(self.nClausulas)+' =/= '+str(len(clauses)))
			exit()
		self.clauses = np.array(clauses, dtype = int)

	def geraSolucao(self):
		solucao = np.empty(0, dtype = bool)
		i = 0
		while i < self.nVariaveis:
			seed()
			if randint(0,100) % 2 == 0:
				solucao = np.append(solucao, True)
			else:
				solucao = np.append(solucao, False)
			i+= 1
		#print(solucao)
		return solucao

	def getNClauses(self):
		return self.nClausulas

	def getnvariaveis(self):
		return self.nVariaveis

	def avalia(self, solucao):
		nota = 0
		resultado = True
		for c in self.clauses:
			resultClause = False
			for v in c:
				if v > 0:
					resultClause = resultClause or solucao[v-1]
					#print(solucao[v-1],end=' ')
				elif v < 0:
					resultClause = resultClause or (not solucao[(-v)-1])
					#print("not"+str(solucao[(-v)-1]),end=' ')
			if resultClause:
				nota += 1
			resultado = (resultado and resultClause)
			#print(' = '+str(resultClause))
			#print(resultado)
		return (nota, resultado)


	def print(self):
		print('Arquivo de entrada: '+self.filename)
		print('Numero de variaveis: '+str(self.nVariaveis))
		print('Numero de clausulas: '+str(self.nClausulas), end='.')
		print(' Variaveis por Clausula: '+str(self.varByClause))
		print(self.clauses)