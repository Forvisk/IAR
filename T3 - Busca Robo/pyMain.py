import numpy as np


from ambiente import Ambiente
from robo import Robo
from largura import BuscaLargura
from noMovimento import NoMovimento
from dijkstra import Djikstra
from aEstrela import AEstrela

place = Ambiente('Robo-ambiente.txt')
robo = Robo(place)
#place.print()
robo.print()
place.setPesos([1,5,10,15])
place.printPeso()

runLargura = BuscaLargura( place)
runLargura.run(robo)

runDjikstra = Djikstra(place)
runDjikstra.run(robo)

runAEstrela = AEstrela(place)
runAEstrela.run(robo)

runLargura.getMenorCaminho()
runDjikstra.getMenorCaminho()
runAEstrela.getMenorCaminho()