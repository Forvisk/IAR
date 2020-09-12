from instanciaSAT import InstanciaSAT
from randomSearch import RandomSearch


print("\n----- Inicio instancia1 -------")
instancia1 = InstanciaSAT('uf20-01.cnf')
instancia1.print()

solucaoInicial1 = instancia1.geraSolucao()
print('---')
#print(solucaoInicial1)
print(instancia1.avalia(solucaoInicial1))
#print(solucaoInicial1.size)

rS = RandomSearch( instancia1)
print(rS.run(solucaoInicial1))

print("----- Fim instancia1 -------")
print("\n----- Inicio instancia2 -------")
instancia2 = InstanciaSAT('uf100-01.cnf')
instancia2.print()
#Instancia 2
solucaoInicial2 = instancia2.geraSolucao()
print('---')
#print(solucaoInicial2)
print(instancia2.avalia(solucaoInicial2))
#print(solucaoInicial1.size)

rS2 = RandomSearch( instancia2)
print(rS2.run(solucaoInicial2))