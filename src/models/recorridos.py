class Recorridos:
    def __init__(self, grafo, usuario):
        self.grafo = grafo
        self.usuario = usuario
        self.distancias, self.caminos = self.menor_distancia() #Sacamos las menores distancias y el camino de estas

### ==== Floyd-Warshall y utilidades ====
    def menor_distancia(self):
        """
        Find all-pairs shortest paths using Floyd-Warshall algorithm. As well as the paths

        Returns:
            dict: Dictionary of dictionaries with shortest distances between all pairs of nodes.
            dict: Dictionary of dictionaries with the routes between the nodes
        """
        # Saca los nodos
        nodes = list(self.grafo.nodos.keys())
        
        #Inicia la matriz con infinito
        distances = {u: {v: float('inf') for v in nodes} for u in nodes}
        
        #Matriz de camino
        next_node = {u: {v: None for v in nodes} for u in nodes}
        
        for u in nodes:
            #Pone valores en si mismos a 0
            distances[u][u] = 0
            #Saca las distancias directas entre nodos vecinos
            for v, arista in self.grafo.nodos[u].vecinos.items():
                distances[u][v] = arista.peso
                next_node[u][v] = v

        # El k es nodo intermedio, verifica cada nodo como posible intermedio
        for k in nodes:
            #El i y j son par de nodos, y se verifica que distancia es menor, si la directa, o si tomando un intermedio
            for i in nodes:
                for j in nodes:
                    if distances[i][k] + distances[k][j] < distances[i][j]:
                        distances[i][j] = distances[i][k] + distances[k][j]
                        next_node[i][j] = next_node[i][k]

        return distances, next_node

    def reconstruccion_camino(self, inicio, fin, matriz):
        """Recibe un nodo inicio y un fin, y va recorriendo la matriz de caminos hasta encontrar el fin

        Args:
            inicio (string): Es el id del nodo inicio
            fin (string): Es el id del nodo final
            matriz (dictionary): La matriz de caminos del floyd_warshall
            
        returns:
            list: Lista de nodos que representan el camino desde el nodo inicial hasta el final.
        """
        if matriz[inicio][fin] is None:
            return [] # No hay camino
        
        camino = [inicio]
        while inicio != fin:
            inicio = matriz[inicio][fin]
            camino.append(inicio)
            
        return camino
    
### ==== Rutas básicas ====
    def camino_menor_distancia(self, inicio, fin):
        """
        Devuelve el camino de menor distancia entre dos nodos, si es válido.
        Incluye los nodos intermedios (tipo 1) por separado.

        Args:
            inicio (string): ID del nodo de inicio.
            fin (string): ID del nodo de fin.
            
        Returns:
            tuple: (camino_completo (list), distancia_total (float), nodos_control(list))
        """
        # Validación de tipo de nodo
        if self.grafo.nodos[inicio].tipo == 1 or self.grafo.nodos[fin].tipo == 1: #Si son puntos de control
            raise ValueError("Error, El nodo de inicio y fin no pueden ser puntos de control")
                
        # Si no hay camino, retornamos vacío
        if self.distancias[inicio][fin] == float('inf'):
            raise ValueError("Error: No existe camino entre los 2 nodos indicados")
        
        # Reconstruir camino completo
        camino = self.reconstruccion_camino(inicio, fin, self.caminos)
        
        # Filtrar nodos de tipo 1 (Puntos de control)
        nodos_control = [n for n in camino[1:-1] if self.grafo.nodos[n].tipo == 1]
        
        distancia_total = self.distancias[inicio][fin]
        
        return camino, distancia_total, nodos_control

    def camino_mas_apropiado_experiencia(self):
        """
        Encuentra el camino más apropiado para el usuario según su experiencia.
        Considera todos los pares de nodos tipo 0 (válidos para inicio y fin).

        Returns:
            tuple: (camino (list), distancia_total (float), penalización (int), nodos_control (list))
        """
        #Sacamos todos los nodos validos
        nodos_validos = [n for n in self.grafo.nodos if self.grafo.nodos[n].tipo == 0]
        mejor_camino = []
        mejor_distancia = float('inf')
        mejor_penalizacion = float('inf')
        mejor_nodos_control = []
        
        for inicio in nodos_validos:
            for fin in nodos_validos:
                if inicio != fin:
                    camino, distancia, nodos_control = self.camino_menor_distancia(inicio, fin)
                    if camino:
                        penalizacion = self.evaluar_camino(camino)
                        if penalizacion < mejor_penalizacion or \
                            (penalizacion == mejor_penalizacion and distancia < mejor_distancia):
                            
                            mejor_camino = camino
                            mejor_distancia = distancia
                            mejor_penalizacion = penalizacion
                            mejor_nodos_control = nodos_control
                            
        return mejor_camino, mejor_distancia, mejor_penalizacion, mejor_nodos_control

### ==== Evaluación de experiencia ====
    def evaluar_camino(self, camino):
        criterios = self.valores_segun_experiencia()
        penalizaciones = 0

        for nodo_id in camino[1:-1]:  # Omitir inicio y fin
            nodo = self.grafo.nodos[nodo_id]
            if nodo.tipo == 1:  # Solo si es un nodo de control
                if nodo.riesgo not in criterios['riesgo']:
                    penalizaciones += 1
                if nodo.accidentalidad not in criterios['accidentalidad']:
                    penalizaciones += 1
                if nodo.dificultad not in criterios['dificultad']:
                    penalizaciones += 1
                if nodo.popularidad not in criterios['popularidad']:
                    penalizaciones += 1                    

        return penalizaciones # Menor penalización -> mejor camino

    def valores_segun_experiencia(self):
        experiencia = self.usuario.experiencia
        if experiencia == 1:
            return {
                'riesgo': {1,2},
                'accidentalidad': {1,2},
                'dificultad': {1, 2},
                'popularidad': {4, 5}
            }
        elif experiencia == 2:
            return {
                'riesgo': {1, 2, 3, 4},
                'accidentalidad': {1, 2, 3, 4},
                'dificultad': {3, 4},
                'popularidad': {2, 3, 4, 5}
            }
        elif experiencia == 3:
            return {
                'riesgo': {1, 2, 3, 4, 5},
                'accidentalidad': {1, 2, 3, 4, 5},
                'dificultad': {1, 2, 3, 4, 5},
                'popularidad': {1, 2, 3, 4, 5}
            }
        else:
            raise ValueError(f"Nivel de experiencia {experiencia} no válido. Debe ser 1, 2 o 3.")

