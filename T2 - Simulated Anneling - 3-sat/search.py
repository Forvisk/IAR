# xor == ^
import random as rd

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
	print( toGetSize)

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

def randomSearch(varList):
	bestSets = []
	bestNVerdades = 0

	global nVariaveis
	global nClausulas
	global listClaVar
	global listClaNot

	nVerdades = avalia( varList)
	#print("Set:", varList, "Resultados Verdadeiros:",nVerdades)
	if nVerdades > bestNVerdades:
		bestSets = []
		bestSets.append(varList)
		bestNVerdades = nVerdades
	elif nVerdades == bestNVerdades:
		bestSets.append(varList)

	print("Clausulas Verdadeiras:", bestNVerdades)
	for lBest in bestSets:
		print("Set:", lBest)

def SASearch(varList):
	pass

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
		if rd.randint(0,1) == 0:
			choice = False
		varList.append(choice)
	return varList

def iniTimer(seq):
	pass

def endTimer(seq):
	pass

def main(file):
	leituraArquivo(file)
	listasIniciais = []
	for i in range(NVEZES):
		listasIniciais.append(geraRandomSet())

	for i in range(NVEZES):
		iniTimer(i)
		randomSearch(listasIniciais[i])
		endTimer(i)


file = "uf20-01.cnf"
main(file)
file = "uf100-01.cnf"
main(file)
file = "uf250-01.cnf"
main(file)