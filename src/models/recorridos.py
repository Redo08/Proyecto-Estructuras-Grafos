class Recorridos:
    def __init__(self, grafo, usuario):
        self.grafo = grafo
        self.usuario = usuario
        
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


    