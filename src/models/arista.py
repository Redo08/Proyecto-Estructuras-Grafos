class Arista:
    def __init__(self, destino, peso=1, riesgo=1, accidentalidad=1, popularidad=1, dificultad=1):
        self.destino = destino #Id del nodo destino
        self.peso = peso
        self.riesgo = riesgo
        self.accidentalidad = accidentalidad
        self.popularidad = popularidad
        self.dificultad = dificultad