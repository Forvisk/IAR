from instanciaSAT import InstanciaSAT
from randomSearch import RandomSearch
from simulatedAnnealing import SimulatedAnnealing

def runInstancia(filename):
	instancia = InstanciaSAT(filename)
	#instancia1.print()

	print(" ------ Solução Inicial ",filename," ------")
	solucaoInicial = instancia.geraSolucao()
	print(instancia.avalia(solucaoInicial),end="\n\n")

	print(" ------- Inicio instancia RandomSearch  ",filename," ------- ")
	rS = RandomSearch( instancia)
	runsRS1 = []
	for i in range(0,10):
		print("RS run ", i)
		runsRS1.append(rS.run(solucaoInicial, 1000))
	print(" ------- Fim instancia RandomSearch  ",filename," ------- ",end="\n\n")

	print("------- Inicio instancia Simulated Annealing  ",filename," ------- ")
	SA = SimulatedAnnealing( instancia)
	temperaturaInicial = SA.getMediaVizinhos(solucaoInicial, 3)
	#print(temperaturaInicial)
	runSA1 = []
	for i in range(0,10):
		print("SA run ",i)
		runSA1.append(SA.run(solucaoInicial, 100, temperaturaInicial, 0.01, 40))
	print("------- Fim instancia Simulated Annealing  ",filename," ------- ",end="\n\n")

	print("Solucões RandomSearch cenário: ",filename)
	n = 0
	for i in runsRS1:
		print("Solução ",n,": ",i)
		n+=1
	print("")
	n=0
	print("Solucões SA cenário: ",filename)
	for i in runSA1:
		print("Solução ",n,": ",i)
		n+=1

runInstancia("uf20-01.cnf")
runInstancia("uf100-01.cnf")
runInstancia("uf250-01.cnf")