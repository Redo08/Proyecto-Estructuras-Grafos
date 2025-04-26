class Grafo:
    def __init__(self):
        self.nodos = []  # Lista de posiciones (x, y)
        self.adyacencia = {}  # Diccionario {nodo: [vecinos]}

    def agregar_nodo(self, posicion):
        """Añade un nuevo nodo en la posición dada"""
        indice = len(self.nodos)
        self.nodos.append(posicion)
        self.adyacencia[indice] = []

    def agregar_arista(self, nodo1, nodo2):
        """Añade una arista entre dos nodos si no existe"""
        if nodo1 != nodo2 and nodo2 not in self.adyacencia[nodo1]:
            self.adyacencia[nodo1].append(nodo2)
            self.adyacencia[nodo2].append(nodo1)  # Grafo no dirigido

    def obtener_nodo_en_posicion(self, posicion):
        """Devuelve el índice del nodo en la posición dada, si existe"""
        for i, nodo in enumerate(self.nodos):
            if ((nodo[0] - posicion[0]) ** 2 + (nodo[1] - posicion[1]) ** 2) ** 0.5 < 10:
                return i
        return None