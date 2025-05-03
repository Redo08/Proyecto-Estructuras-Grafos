from src.models.arista import Arista
from src.models.nodo import Nodo
class Grafo:
    def __init__(self):
        self.nodos = {} #id -> Nodo
        
    def agregar_nodo(self, id, nombre=None, descripcion=None, riesgo=None, tipo=0, accidentalidad=None, popularidad=None, dificultad=None, posicion=None):
        if id not in self.nodos:
            self.nodos[id] = Nodo(id, nombre, descripcion, riesgo, tipo, accidentalidad, popularidad, dificultad, posicion)

    def proximo_id(self, tipo, nombre=""):
        max_id = 0
        prefix = ""
        #Determinar el prefijo según el tipo
        if tipo == 1:
            prefix = "PC"
        elif tipo == 0 and len(nombre) >= 2:
            prefix = nombre[:2].capitalize() #Primeras 2 letras y en mayuscula
        else:
            prefix = "ND" #No definido

        for id_nodo in self.nodos:
            #Verificamos si el prefio ya existe
            if id_nodo.startswith(prefix):
                #Extraemos los digitos del final
                num_str = ''
                for char in reversed(id_nodo):
                    if char.isdigit():
                        num_str = char + num_str
                    else:
                        #Si no es numero se sale
                        break
                if num_str: 
                    num_id = int(num_str)
                    if num_id > max_id:
                        max_id = num_id

        return f"{prefix}{max_id + 1}" #Retornamos el prefijo más el siguietne numreo
    
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
        ##if len(self.nodos) == 1:
            ##return False, "No se puede eliminar el único nodo"
        return True, None
    def cargar_json(self, datos):
        if datos is not None:
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
        for origen_id, nodo in self.nodos.items():
            for destino_id, arista in nodo.vecinos.items():
                data["aristas"].append({
                    "origen": origen_id,
                    "destino": destino_id,
                    "peso": arista.peso
                })
            
        return data 