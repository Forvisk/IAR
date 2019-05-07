# xor == ^
from random import randint, seed
from math import exp

NVEZES = 10
nVariaveis = 0
nClausulas = 0
listClaVar = []
listClaNot = []

def leituraArquivo(file):

	global nVariaveis
	global nClausulas
	global listClaVar
	global listClaNot


	nVariaveis = 0
	nClausulas = 0
	listClaVar = []
	listClaNot = []

	f = open(file, "r")

	while f.read(1) == "c":
		#print (f.readline())
		f.readline()

	l = f.readline()
	toGetSize = l.split()
	#print( toGetSize)

	nVariaveis = int(toGetSize[1])
	nClausulas = int(toGetSize[2])

	for i in range(nClausulas):
		l = f.readline()
		li = l.split()
		lint = [int(li[0]), int(li[1]), int(li[2])]
		lnot = [False, False, False]
		for i in range(0,3):
			if lint[i] < 0:
				lnot[i] = True
			lint[i] = abs(lint[i])
		listClaVar.append(lint)
		listClaNot.append(lnot)
		
	#print( listClaVar)
	#print( listClaNot)
		
	f.close()

def randomSearch( varList):
	global nClausulas
	bestSets = []
	bestNVerdades = 0

	nVerdades = avalia( varList)
	#print("Set:", varList, "Resultados Verdadeiros:",nVerdades)
	if nVerdades > bestNVerdades:
		bestSets = []
		bestSets.append(varList)
		bestNVerdades = nVerdades
	elif nVerdades == bestNVerdades:
		bestSets.append(varList)

	print("RS - Clausulas Verdadeiras:", bestNVerdades, "de", nClausulas)
	#for lBest in bestSets:
	#	print("Set:", lBest)

def geraTinicial( varList):
	Inicial = avalia(varList)
	nCustosV = []
	k=0
	while k <= 0:
		for i in range(10):
			vizinho = geraVizinho(varList)
			nCustosV.append(Inicial - avalia(vizinho))
		k = max(nCustosV)
	#gera temperatura aqui
	#print(k)
	return k

def SASearch( varList):
	global nClausulas
	SAmax = 10
	nk = 0
	T = Tinicial = geraTinicial( varList)
	cvvarList = bestNVerdades = avalia( varList)
	bestSet = varList
	print("SA- bestSet inicial",bestNVerdades, "Tinicial",Tinicial)
	taxa = 0.9
	while T > 0.001:
		itT = 0
		while itT < SAmax:
			nk += 1
			itT += 1
			vizinho = geraVizinho(varList)
			cvVizinhos = avalia(vizinho)

			delta = cvVizinhos - cvvarList
			#print("SA-",cvVizinhos,cvvarList)
			if delta > 0:#ideia e maximizar
				varList = vizinho
				cvvarList = cvVizinhos
				#print("SA- Novo varList", cvvarList)
				if cvVizinhos > bestNVerdades:
					#print("SA- Novo bestSet", cvVizinhos, ">", bestNVerdades)
					bestSet = vizinho
					bestNVerdades = cvVizinhos

			else:
				r = randint(0,100)/100
				ex = delta/T
				#print("SA: -r=",-r,";",delta,"/",T,"=",ex)
				if -r >= exp(ex):
					#print("SA",r,"<",exp(ex))
					varList = vizinho
					cvvarList = cvVizinhos
					#print("SA- Novo varList", cvvarList)
		T = round(T * taxa,10)
		#print("SA- temperatura:",T)

	print("SA - Clausulas Verdadeiras:", bestNVerdades, "de", nClausulas)
	#print("Set:", bestSet)


def geraVizinho( varList):
	global nVariaveis
	bTroca = randint(0,nVariaveis-1)
	varList[bTroca] = not varList[bTroca]
	return varList

def avalia( varList):
	global nClausulas
	global listClaVar
	global listClaNot

	nVerdades = 0
	for i in range(0,nClausulas):
		if( (varList[listClaVar[i][0]-1] ^ listClaNot[i][0]) or
			(varList[listClaVar[i][1]-1] ^ listClaNot[i][1]) or
			(varList[listClaVar[i][2]-1] ^ listClaNot[i][2])):
			nVerdades += 1

	return nVerdades
	
def geraRandomSet():
	varList = []
	for i in range(0, nVariaveis):
		choice = True
		if randint(0,1) == 0:
			choice = False
		varList.append(choice)
	return varList

def iniTimer(seq):
	pass

def endTimer(seq):
	pass

def main(file):
	print(file)
	leituraArquivo(file)
	listasIniciais = geraRandomSet()

	for i in range(NVEZES):
		#print("Estado Inicial",i,":",listasIniciais)
		iniTimer(i)
		randomSearch(listasIniciais)
		endTimer(i)
		iniTimer(i)
		SASearch(listasIniciais)
		endTimer(i)


file = "uf20-01.cnf"
main(file)
file = "uf100-01.cnf"
main(file)
file = "uf250-01.cnf"
main(file)