from instanciaSAT import InstanciaSAT
from randomSearch import RandomSearch
from simulatedAnnealing import SimulatedAnnealing

def runInstancia(filename):
	instancia = InstanciaSAT(filename)
	nRuns = 10
	coolingSchedules = [0,1,2,3]
	#coolingSchedules = [3]
	#instancia1.print()

	print(" ------ Solução Inicial ",filename," ------")
	solucaoInicial = instancia.geraSolucao()
	print(instancia.avalia(solucaoInicial),end="\n\n")

	print(" ------- Inicio instancia RandomSearch  ",filename," ------- ")
	rS = RandomSearch( instancia)
	runsRS1 = []
	for i in range(0,nRuns):
		print("RS run ", i, end=' - ')
		runsRS1.append(rS.run(solucaoInicial, 2000))
		print(runsRS1[i][0])
	print(" ------- Fim instancia RandomSearch  ",filename," ------- ",end="\n\n")

	SA = SimulatedAnnealing( instancia)
	temperaturaInicial = SA.getMediaVizinhos(solucaoInicial, 3)
	#print(temperaturaInicial)
	runCoolingSchedule = []
	for typeCooling in coolingSchedules:
		print(" ------- Inicio instancia Simulated Annealing ",filename," ------- ")
		print(" ------- Cooling Schedule ", typeCooling," ------- ")
		runSA1 = []
		for i in range(0,nRuns):
			print("SA run ",i, "Cooling Schedule ", typeCooling, end=' - ')
			runSA1.append(SA.run(solucaoInicial, 100, temperaturaInicial, 0.01, 40, typeCooling))
			print(runSA1[i][0])
		print(" ------- Fim instancia Simulated Annealing  ",filename," ------- ",end="\n\n")
		runCoolingSchedule.append(runSA1)


	print(" ---- RESULTADOS ---- ")
	outputFilename = filename+".resultados.txt"
	f = open(outputFilename, "w")
	f.write("Resultados "+filename+";\n")
	rini = str(instancia.avalia(solucaoInicial))
	rrini = str(solucaoInicial)
	f.write("Solução Inicial;\n"+rini+";\t;"+rrini+";\n")
	print("")
	f.write("\n")
	print("Solucões RandomSearch cenário: ",filename)
	f.write("Resultados RandomSearch;\n")
	n = 0
	for i in runsRS1:
		print("Solução ",n,": ",i[0]," ",i[1])
		res = str(i[0])
		vecRes = str(i[1])
		f.write("SA;r"+str(n)+";"+str(typeCooling)+";"+res+";\t;"+vecRes+";\n")
		sconvergencia = str(i[2])
		f.write("Convergencia: ")
		f.write(sconvergencia+"\n")
		#f.write(vecRes+";")
		n+=1
	print("")
	f.write("\n")
	print("Solucões SA cenário: ",filename)
	f.write("Resultados Simulated Annealing;\n")
	v = 0
	for typeCooling in coolingSchedules:
		f.write("Cooling Schedule "+str(typeCooling)+";\n")
		print("Cooling Schedule ", typeCooling)
		n=0
		for i in runCoolingSchedule[v]:
			print("Solução ",n,": ",i[0]," ",i[1])
			res = str(i[0])
			vecRes = str(i[1])
			f.write("SA;r"+str(n)+";"+str(typeCooling)+";"+res+";\t;"+vecRes+";\n")
			#f.write(vecRes+";")
			f.write("Convergencia: ")
			sconvergencia = str(i[2])
			f.write(sconvergencia+"\n")
			n+=1
		v+=1
	f.close()

runInstancia("uf20-01.cnf")
runInstancia("uf100-01.cnf")
runInstancia("uf250-01.cnf")