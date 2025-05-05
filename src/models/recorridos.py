import heapq
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
    
    def dijkstra_por_riesgo(self, inicio, fin):
        visitados = set()
        heap = [(0, 0, inicio, [])] #Suma riesgo, cantidad_puntos_control, nodo_actual, camino
        
        while heap:
            riesgo_acum, puntos_control, actual, camino = heapq.heappop(heap)
        
            if actual in visitados:
                continue
            
            camino = camino + [actual]
            visitados.add(actual)
            
            # Si termina el recorrido
            if actual == fin:
                #Calcular riesgo promedio
                promedio = riesgo_acum / puntos_control if puntos_control > 0 else 0
                nodos_control = [n for n in camino if self.grafo.nodos[n].tipo == 1]
                return camino, promedio, nodos_control
            
            for vecino_id, arista in self.grafo.nodos[actual].vecinos.items():
                if vecino_id not in visitados:
                    vecino = self.grafo.nodos[vecino_id]
                    nuevo_riesgo = riesgo_acum
                    nuevo_pc = puntos_control
                    
                    if vecino.tipo == 1: #Si es un punto de control suammos su riesgo
                        nuevo_riesgo += int(vecino.riesgo)
                        nuevo_pc +=1
                        
                    heapq.heappush(heap, (nuevo_riesgo, nuevo_pc, vecino_id, camino))
                    
        return [], float('inf'), []
    
    def recalcular_usuario(self, usuario):
        self.usuario = usuario
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
            print("Error, El nodo de inicio y fin no pueden ser puntos de control")
            return [], float('inf'), []

                
        # Si no hay camino, retornamos vacío
        if self.distancias[inicio][fin] == float('inf'):
            print("Error: No existe camino entre los 2 nodos indicados")
            return [], float('inf'), []
        
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

    def camino_menos_peligroso(self):
        """Encuentra el camino menos peligroso usando Dijkstra sumando riesgo de los puntos de control
        
        Returns:
            tuple: (camino(list), promedio_riesgo (float), nodos_control (list))
        """
        nodos_validos = [n for n in self.grafo.nodos if self.grafo.nodos[n].tipo == 0]
        mejor_camino = []
        mejor_promedio_riesgo = float('inf')
        mejor_nodos_control = []
        
        for inicio in nodos_validos:
            for fin in nodos_validos:
                if inicio != fin:
                    camino, riesgo_promedio, nodos_control, = self.dijkstra_por_riesgo(inicio, fin)
                    if camino and riesgo_promedio < mejor_promedio_riesgo:
                        mejor_camino = camino
                        mejor_promedio_riesgo = riesgo_promedio
                        mejor_nodos_control = nodos_control
                        
        return mejor_camino, mejor_promedio_riesgo, mejor_nodos_control
    
    def camino_por_distancia_riesgo_dificultad_deseada(self):
        """
        Da el camino que esta más cerca de la distancia deseada por el usuario, y que no excede su
        riesgo ni dificultad

        Returns:
            tuple: (camino (list), distancia_total (float), diferencia (float), nodos_control (list))
        """
        
        distancia_deseada = self.usuario.distancia_max
        dificultad_max = self.usuario.dificultad_max
        riesgo_max = self.usuario.riesgo_max
        
        nodos_validos = [n for n in self.grafo.nodos if self.grafo.nodos[n].tipo == 0]
        mejor_camino = []
        mejor_distancia = float('inf')
        mejor_diferencia = float('inf')
        mejor_nodos_control = []
        
        for inicio in nodos_validos:
            for fin in nodos_validos:
                if inicio != fin:
                    camino, distancia, nodos_control = self.camino_menor_distancia(inicio, fin)
                    if camino:
                        # Validar si todos los nodos cumplen con los requisitos de riesgo y dificultad
                        valido = True
                        for nodo_id in nodos_control:
                            nodo = self.grafo.nodos[nodo_id]
                            if int(nodo.riesgo) > riesgo_max or int(nodo.dificultad) > dificultad_max:
                                valido = False
                                break
                            
                        if valido:
                            diferencia = abs(distancia_deseada - distancia)
                            if diferencia < mejor_diferencia:
                                mejor_camino = camino
                                mejor_distancia = distancia
                                mejor_diferencia = diferencia
                                mejor_nodos_control = nodos_control
                                
        return mejor_camino, mejor_distancia, mejor_diferencia, mejor_nodos_control
    
    def camino_distancia_dificultad_experiencia(self):
        """
        Sugiere una ruta considerando la distancia y la dificultad del usuario deseadas además
        de poner los otros valores por defecto respecto al nivel de experiencia
        
        Returns:
            tuple : (camino (list), distancia_total (float), penalización_total (int), diferencia_distancia (float), nodos_control (list))
        """
        
        distancia_deseada = self.usuario.distancia_max
        dificultad_max = self.usuario.dificultad_max
        criterios = self.valores_segun_experiencia()
        
        #Sacamos los nodos iterables (Tipo 0)
        nodos_validos = [n for n in self.grafo.nodos if self.grafo.nodos[n].tipo == 0]
        mejor_camino = []
        mejor_distancia = float('inf')
        mejor_penalizacion = float('inf')
        mejor_diferencia = float('inf')
        mejor_nodos_control = []
        
        for inicio in nodos_validos:
            for fin in nodos_validos:
                if inicio != fin:
                    camino, distancia, nodos_control = self.camino_menor_distancia(inicio, fin)
                    
                    if camino:
                        valido = True
                        penalizaciones = 0
                        
                        for nodo_id in nodos_control:
                            nodo = self.grafo.nodos[nodo_id]
                            if int(nodo.dificultad) > dificultad_max:
                                valido = False
                                break
                            
                            if nodo.riesgo not in criterios['riesgo']:
                                penalizaciones += 1
                            if nodo.accidentalidad not in criterios['accidentalidad']:
                                penalizaciones +=1
                            if nodo.popularidad not in criterios['popularidad']:
                                penalizaciones +=1
                            
                        if valido:
                            diferencia = abs(distancia_deseada - distancia)
                            if (penalizaciones < mejor_penalizacion) or \
                                (penalizaciones == mejor_penalizacion and diferencia < mejor_diferencia):
                                    mejor_camino = camino
                                    mejor_distancia = distancia
                                    mejor_diferencia = diferencia
                                    mejor_penalizacion = penalizaciones
                                    mejor_nodos_control = nodos_control
        
        return mejor_camino, mejor_distancia, mejor_penalizacion, mejor_diferencia, mejor_nodos_control
    
    def camino_disntacias_minimas_desde_nodo_dado(self, nodo_inicio):
        """
        Devuelve las distancias minimas dado un nodo, usando floyd-warshall

        Args:
            nodo_inicio (str): Id nodo inicial

        Returns:
            dict: {nodo_destino: (distancia, camino)}
        """
        resultados = {}
        nodos_validos = [n for n in self.grafo.nodos if self.grafo.nodos[n].tipo == 0]
        
        for nodo in nodos_validos:
            if nodo != nodo_inicio:
                distancia = self.distancias[nodo_inicio][nodo]
                camino = self.reconstruccion_camino(nodo_inicio, nodo, self.caminos)
                resultados[nodo] = (distancia, camino)
                
        return resultados
    
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