from instanciaSAT import InstanciaSAT


instancia1 = InstanciaSAT('uf20-01.cnf')
instancia1.print()

solucaoInicial1 = instancia1.geraSolucao()
print('---')
print(solucaoInicial1)
print(solucaoInicial1.size)