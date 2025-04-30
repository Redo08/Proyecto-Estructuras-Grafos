class Nodo:
    def __init__(self, id, nombre='', descripcion='', riesgo=1):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.riesgo = riesgo
        self.vecinos = {} # id_nodo_destino -> Arista