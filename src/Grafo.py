from collections import defaultdict, deque
import heapq

class Graph:
    """
    A graph implementation using adjacency lists (dictionary of dictionaries).
    Supports both directed and undirected weighted graphs.
    """

    def __init__(self):
        """
        Initialize an empty graph using a dictionary of dictionaries representation.
        """
        # Esto hace que si se hace un llamado a alguna llave que no existia, se crea al instante y no crashea
        self.graph = defaultdict(dict)

    def add_node(self, node):
        """
        Add a node to the graph if it doesn't exist.

        Args:
            node: The node to be added to the graph.
        """
        #Crea el nodo, asignandolo como una llave, le asigna un diccionario vacio
        if node not in self.graph:
            self.graph[node] = {}

    def add_edge(self, node1, node2, weight=1, directed=False):
        """
        Add an edge between two nodes with an optional weight.

        Args:
            node1: First node of the edge.
            node2: Second node of the edge.
            weight (int, optional): Weight of the edge. Defaults to 1.
            directed (bool, optional): If True, creates a directed edge. Defaults to False.
        """
        self.graph[node1][node2] = weight
        #Si no es dirigido, solo pone una parte que apunta a la otra, mostrando asi la flechita del nodo 1 al nodo 2
        if not directed:
            self.graph[node2][node1] = weight

    def bfs(self, start): #Anchura
        """
        Perform Breadth-First Search traversal starting from a given node.

        Args:
            start: Starting node for the traversal.

        Returns:
            list: Nodes in BFS traversal order.
        """
        #Conjunto
        visited = set()
        
        #Cola
        queue = deque([start])
        result = []

        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                result.append(node)
                queue.extend(self.graph[node].keys() - visited)
        
        return result

    def dfs(self, start): #Profundidad
        """ 
        Perform Depth-First Search traversal starting from a given node.

        Args:
            start: Starting node for the traversal.

        Returns:
            list: Nodes in DFS traversal order.
        """
        visited = set()
        stack = [start]
        result = []

        while stack:
            #Saca el ultimo
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                result.append(node)
                #Añade a los vecinos que no han sido visitados
                stack.extend(self.graph[node].keys() - visited)
        
        return result

    def prim(self, start):
        """
        Find the Minimum Spanning Tree using Prim's algorithm.

        Args:
            start: Starting node for the algorithm.

        Returns:
            list: List of tuples (from_node, to_node, weight) representing MST edges.
        """
        visited = set([start])
        edges = [
            (weight, start, to) for to, weight in self.graph[start].items()
        ]
        heapq.heapify(edges)
        mst = []

        while edges:
            # Saca el más pequeño de la lista de edges
            weight, frm, to = heapq.heappop(edges)
            if to not in visited:
                visited.add(to)
                mst.append((frm, to, weight))

                for next_to, next_weight in self.graph[to].items():
                    if next_to not in visited:
                        heapq.heappush(edges, (next_weight, to, next_to))

        return mst

    def kruskal(self):
        """
        Find the Minimum Spanning Tree using Kruskal's algorithm.

        Returns:
            list: List of tuples (from_node, to_node, weight) representing MST edges.
        """
        edges = [
            (weight, u, v) for u in self.graph for v, weight in self.graph[u].items()
        ]
        edges = sorted(edges)
        # Donde se guardan los conjuntos
        parent = {}

        def find(v):
            #Si no es su propio padre, se encuentra el verdadero padre, osea se encuentra un conjunto
            if parent[v] != v:
                parent[v] = find(parent[v])
            return parent[v]

        def union(v1, v2):
            #Une 2 conjuntos
            root1, root2 = find(v1), find(v2)
            parent[root2] = root1

        mst = []
        for node in self.graph:
            #Cada nodo inicialmente es su propio padre, su propio conjunto
            parent[node] = node

        # Recorre inicialmente por las aristas con peso menor
        for weight, u, v in edges:
            #Si sus padres no son iguales, significa que son conjuntos separados, por lo que los une
            if find(u) != find(v):
                union(u, v)
                mst.append((u, v, weight))

        return mst

    def dijkstra(self, start):
        """
        Find shortest paths from a start node using Dijkstra's algorithm.

        Args:
            start: Starting node for the algorithm.

        Returns:
            dict: Dictionary with shortest distances to all nodes from start node.
        """
        #Inician todas las distancias infinitas menos la del start
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        #Cola de prioridad
        pq = [(0, start)]

        while pq:
            #Saca el más pequeño 
            current_distance, current_node = heapq.heappop(pq)
            
            #Si no es más optimo, continua
            if current_distance > distances[current_node]:
                continue

            # Saca el coste desde el nodo hasta sus vecinos
            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight

                #Actualiza si es más eficiente
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

        return distances

    def floyd_warshall(self):
        """
        Find all-pairs shortest paths using Floyd-Warshall algorithm.

        Returns:
            dict: Dictionary of dictionaries with shortest distances between all pairs of nodes.
        """
        # Saca los nodos
        nodes = list(self.graph.keys())
        #Inicia la matriz con infinito
        distances = {u: {v: float('inf') for v in nodes} for u in nodes}
        for u in nodes:
            #Pone valores en si mismos a 0
            distances[u][u] = 0
            #Saca las distancias directas entre nodos vecinos
            for v, weight in self.graph[u].items():
                distances[u][v] = weight

        # El k es nodo intermedio, verifica cada nodo como posible intermedio
        for k in nodes:
            #El i y j son par de nodos, y se verifica que distancia es menor, si la directa, o si tomando un intermedio
            for i in nodes:
                for j in nodes:
                    distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])

        return distances

    def bellman_ford(self, start):
        """
        Find shortest paths from a start node using Bellman-Ford algorithm.
        Can detect negative cycles.

        Args:
            start: Starting node for the algorithm.

        Returns:
            dict: Dictionary with shortest distances to all nodes from start node.

        Raises:
            ValueError: If a negative cycle is detected in the graph.
        """
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0

        for _ in range(len(self.graph) - 1):
            for u in self.graph:
                for v, weight in self.graph[u].items():
                    if distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight

        for u in self.graph:
            for v, weight in self.graph[u].items():
                if distances[u] + weight < distances[v]:
                    raise ValueError("El grafo contiene un ciclo negativo")

        return distances
    
    def ford_fulkerson(self, source, sink):
        """
        Find the maximum flow in a flow network using Ford-Fulkerson algorithm.

        Args:
            source: Source node of the flow network.
            sink: Sink node of the flow network.

        Returns:
            int: Maximum flow from source to sink.
        """
        def bfs_find_path(parent):
            visited = set([source])
            queue = deque([source])
            while queue:
                u = queue.popleft()
                for v in self.graph[u]:
                    if v not in visited and self.graph[u][v] - flow[u][v] > 0:
                        queue.append(v)
                        visited.add(v)
                        parent[v] = u
                        if v == sink:
                            return True
            return False

        flow = {u: {v: 0 for v in self.graph} for u in self.graph}
        max_flow = 0
        parent = {}

        while bfs_find_path(parent):
            path_flow = float('inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s] - flow[parent[s]][s])
                s = parent[s]
            v = sink
            while v != source:
                u = parent[v]
                flow[u][v] += path_flow
                flow[v][u] -= path_flow
                v = u
            max_flow += path_flow

        return max_flow
    
def test_graph():
    g = Graph()

    nodes = ['10', '15', '20', '25', '30', '35', '40', '45', '47', '50', '55', '60', '65']
    for node in nodes:
        g.add_node(node)

    g.add_edge('10', '15')
    g.add_edge('10', '30')
    g.add_edge('30', '47')
    g.add_edge('47', '50')
    g.add_edge('50', '55')
    g.add_edge('55', '35')
    g.add_edge('55', '60')
    g.add_edge('60', '65')
    g.add_edge('60', '40')
    g.add_edge('35', '40')
    g.add_edge('40', '20')
    g.add_edge('15', '20')
    g.add_edge('15', '35')
    g.add_edge('20', '25')
    g.add_edge('25', '45')
    g.add_edge('45', '65')


    print("Grafo:", g.graph)
    print("BFS from node 'A':", g.bfs('35'))
    print("DFS from node 'A':", g.dfs('35'))

    print("Primm from node 'A':", g.prim('A'))

    print("Kruskal:", g.kruskal())

    print("Minimum distances from node 'A' (Dijkstra):", g.dijkstra('35'))
    # print("Ejercicio preparcial anchura:", g.ejercicio_preparcial_anchura('35',2))
    # print("Ejercicio preparcial dijsktra", g.ejercicio_preparcial_dijkstra('35',2))

    print("Minimum distances all-pair of nodes (Floyd-Warshall):")
    floyd_distances = g.floyd_warshall()
    for u in floyd_distances:
        for v in floyd_distances[u]:
            print(f"Distance from {u} to {v}: {floyd_distances[u][v]}")

    print("Minimum distances from node 'A' (Bellman-Ford):", g.bellman_ford('A'))

    try:
        max_flow = g.ford_fulkerson('A', 'E')
        print("Maximum flow from node A to node E (Ford-Fulkerson):", max_flow)
    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    test_graph()
