from src.models.arista import Arista
from src.models.nodo import Nodo
class Grafo:
    def __init__(self):
        self.nodos = {} #id -> Nodo
        
    def agregar_nodo(self, id, nombre='', descripcion='', riesgo=1):
        if id not in self.nodos:
            self.nodos[id] = Nodo(id, nombre, descripcion, riesgo)
            
    def agregar_arista(self, id_origen, id_destino, peso=1, riesgo=1, accidentalidad=1, popularidad=1, dificultad=1):
        if id_origen in self.nodos and id_destino in self.nodos:
            arista = Arista(id_destino, peso, riesgo, accidentalidad, popularidad, dificultad)
            self.nodos[id_origen].vecinos[id_destino] = arista
    
    def cargar_json(self, datos):
        #Agregar nodos
        for nodo in datos['nodos']:
            self.agregar_nodo(
                id=nodo['id'],
                nombre=nodo['nombre'],
                descripcion=nodo['descripcion'],
                riesgo=nodo['riesgo']
            )
        
        #Agregar aristas
        for arista in datos['aristas']:
            self.agregar_arista(
                id_origen=arista['origen'],
                id_destino=arista['destino'],
                peso=arista['peso'],
                riesgo=arista['riesgo'],
                accidentalidad=arista['accidentalidad'],
                popularidad=arista['popularidad'],
                dificultad=arista['dificultad']
            )
        
    def guardar_json(self):
        data = {
            "nodos": [],
            "aristas": []
        }
        
        #Guardar nodos
        for nodo_id, nodo in self.nodos.items():
            data["nodos"].append({
                "id": nodo.id,
                "nombre": nodo.nombre,
                "descripcion": nodo.descripcion,
                "riesgo": nodo.riesgo
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
                    "peso": arista.peso,
                    "riesgo": arista.riesgo,
                    "accidentalidad": arista.accidentalidad,
                    "popularidad": arista.popularidad,
                    "dificultad": arista.dificultad
                })
            
        return data
            