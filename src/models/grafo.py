from src.models.arista import Arista
from src.models.nodo import Nodo
class Grafo:
    def __init__(self):
        self.nodos = {} #id -> Nodo
        
    def agregar_nodo(self, id, nombre=None, descripcion=None, riesgo=None, tipo=0, accidentalidad=None, popularidad=None, dificultad=None, posicion=None):
        if id not in self.nodos:
            self.nodos[id] = Nodo(id, nombre, descripcion, riesgo, tipo, accidentalidad, popularidad, dificultad, posicion)

    def proximo_id(self):
        max_id = 0
        for id_nodo in self.nodos:
            try:
                num_id = int(id_nodo)
                if num_id > max_id:
                    max_id = num_id
            except ValueError:
                pass
        return str(max_id + 1)
    
    def agregar_arista(self, id_origen, id_destino, peso=1):
        if id_origen in self.nodos and id_destino in self.nodos:
            arista = Arista(id_destino, peso)
            self.nodos[id_origen].vecinos[id_destino] = arista
    
    def eliminar_arista(self, id_origen, id_destino):
        if id_origen in self.nodos and id_destino in self.nodos:
            if id_destino in self.nodos[id_origen].vecinos:
                del self.nodos[id_origen].vecinos[id_destino]

    def validar_agregar_arista(self, id_origen, id_destino):
        if len(self.nodos) < 2:
            return False, "Se necesitan al menos dos nodos para agregar una arista."
        if id_origen not in self.nodos or id_destino not in self.nodos:
            return False, "Uno o ambos nodos no existen."
        if id_origen == id_destino:
            return False, "No se pueden agregar aristas de un nodo a sí mismo."
        if id_destino in self.nodos[id_origen].vecinos:
            return False, "Ya existe una arista entre estos nodos."
        return True, None
    def validar_eliminar_arista(self, id_origen, id_destino):
        if id_origen not in self.nodos or id_destino not in self.nodos:
            return False, "Uno o ambos nodos no existen."
        if id_destino not in self.nodos[id_origen].vecinos:
            return False, "No existe una arista entre estos nodos."
        return True, None         
    def eliminar_nodo(self, id_nodo):
        if id_nodo in self.nodos:
            # Eliminar aristas que salen del nodo y las que llegan a él
            for vecino in list(self.nodos[id_nodo].vecinos.keys()):
                if vecino in self.nodos:
                    self.nodos[vecino].vecinos.pop(id_nodo, None)
            # Eliminar el nodo
            del self.nodos[id_nodo]

    def validar_eliminacion_nodo(self, nodo_id):
        if nodo_id not in self.nodos:
            return False, "Nodo no existe"
        if len(self.nodos) == 1:
            return False, "No se puede eliminar el único nodo"
        return True, None
    def cargar_json(self, datos):
        #Agregar nodos
        for nodo in datos['nodos']:
            self.agregar_nodo(
                id=nodo['id'],
                nombre=nodo['nombre'],
                descripcion=nodo['descripcion'],
                riesgo=nodo['riesgo'],
                tipo=nodo['tipo'],
                accidentalidad=nodo['accidentalidad'],
                popularidad=nodo['popularidad'],
                dificultad=nodo['dificultad'],
                posicion=nodo.get('posicion')
            )
        
        #Agregar aristas
        for arista in datos['aristas']:
            self.agregar_arista(
                id_origen=arista['origen'],
                id_destino=arista['destino'],
                peso=arista['peso']
            )
        
    def guardar_json(self):
        data = {
            "nodos": [],
            "aristas": []
        }
        
        #Guardar nodos
        for nodo_id, nodo in self.nodos.items():
            if nodo.tipo == 0:
                data["nodos"].append({
                    "id": nodo.id,
                    "nombre": nodo.nombre,
                    "descripcion": nodo.descripcion,
                    "riesgo": None,
                    "tipo": nodo.tipo,
                    "accidentalidad": None,
                    "popularidad": None,
                    "dificultad": None,
                    "posicion": nodo.posicion
                })
            elif nodo.tipo == 1:
                data["nodos"].append({
                    "id": nodo.id,
                    "nombre": None,
                    "descripcion": None,
                    "riesgo": nodo.riesgo,
                    "tipo": nodo.tipo,
                    "accidentalidad": nodo.accidentalidad,
                    "popularidad": nodo.popularidad,
                    "dificultad": nodo.dificultad,
                    "posicion": nodo.posicion
                })
            
        # Guardar aristas
        aristas_guardadas = set()
        for origen_id, nodo in self.nodos.items():
            for destino_id, arista in nodo.vecinos.items():
                clave = tuple(sorted([origen_id, destino_id]))
                if clave in aristas_guardadas:
                    continue
                aristas_guardadas.add(clave)

                data["aristas"].append({
                    "origen": origen_id,
                    "destino": destino_id,
                    "peso": arista.peso
                })
            
        return data

    def floyd_warshall(self):
        """
        Find all-pairs shortest paths using Floyd-Warshall algorithm. As well as the paths

        Returns:
            dict: Dictionary of dictionaries with shortest distances between all pairs of nodes.
            dict: Dictionary of dictionaries with the routes between the nodes
        """
        # Saca los nodos
        nodes = list(self.nodos.keys())
        
        #Inicia la matriz con infinito
        distances = {u: {v: float('inf') for v in nodes} for u in nodes}
        
        #Matriz de camino
        next_node = {u: {v: None for v in nodes} for u in nodes}
        
        for u in nodes:
            #Pone valores en si mismos a 0
            distances[u][u] = 0
            #Saca las distancias directas entre nodos vecinos
            for v, arista in self.nodos[u].vecinos.items():
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
        """_summary_

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
    