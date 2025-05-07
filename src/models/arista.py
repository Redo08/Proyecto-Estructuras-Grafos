class Arista:
    def __init__(self, origen, destino, peso=1, nodo_control = None):
        self.origen = origen
        self.destino = destino #Id del nodo destino
        self.peso = peso
        self.nodos_control = [nodo_control] # => Id nodo_control: Nodo(tipo=1)