import numpy as np
from ambiente import Ambiente
from robo import Robo
from largura import BuscaLargura
from noMovimento import NoMovimento

place = Ambiente('Robo-ambiente.txt')
robo = Robo(place)
#place.print()
robo.print()
place.setPesos([1,5,10,15])
place.printPeso()

runLargura = BuscaLargura( place)
runLargura.run(robo)
runLargura.getMenorCaminho()
'''
noInicial = NoMovimento(robo.getInicio(), place, [])
noAtual = [noInicial]
noProximo = []
inicio = robo.getInicio()
size = place.getDimensoes()
nextMove = []
N = 0
if inicio[0]-1 >= 0:
	nextMove.append([inicio[0]-1,inicio[1]])
if inicio[0]+1 < size[0]:
	nextMove.append([inicio[0]+1 ,inicio[1]])
if inicio[1]-1 >= 0:
	nextMove.append([inicio[0],inicio[1]-1])
if inicio[1]+1 < size[1]:
	nextMove.append([inicio[0],inicio[1]+1])

for no in noAtual:
	for move in nextMove:
		print(move)
		noProximo.append (NoMovimento(move, place, [no]))

for no in noProximo:
	no.print()
	'''