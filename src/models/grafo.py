from src.models.arista import Arista
from src.models.nodo import Nodo
class Grafo:
    def __init__(self):
        self.nodos = {} #id -> Nodo
        
    def agregar_nodo(self, id, nombre=None, descripcion=None, riesgo=None, tipo=0, accidentalidad=None, popularidad=None, dificultad=None, posicion=None):
        if id not in self.nodos:
            self.nodos[id] = Nodo(id, nombre, descripcion, riesgo, tipo, accidentalidad, popularidad, dificultad, posicion)
            
    def agregar_arista(self, id_origen, id_destino, peso=1):
        if id_origen in self.nodos and id_destino in self.nodos:
            arista = Arista(id_destino, peso)
            self.nodos[id_origen].vecinos[id_destino] = arista
    
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
            