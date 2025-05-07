from src.models.arista import Arista
from src.helpers import Helpers
from src.models.nodo import Nodo
from src.models.recorridos import Recorridos
import re
class Grafo:
    def __init__(self):
        self.nodos = [] #Listo de nodos de punto de interes, nodos tipo 0
        self.aristas = []  # Aristas
        

    def proximo_id(self, tipo, nombre=""):
        prefix = ""
        #Determinar el prefijo según el tipo
        if tipo == 1:
            prefix = "PC"
        elif tipo == 0 and len(nombre) >= 2:
            prefix = nombre[:2].capitalize() if len(nombre) >= 2 else "PI" #Primeras 2 letras y en mayuscula
        max_id = 0

        for nodo in self.nodos:
            #Verificamos si el prefio ya existe
            if nodo.id.startswith(prefix):
                #Extraemos los digitos del final
                match = re.search(r'\d+$', nodo.id)  # Buscar dígitos al final
                if match:
                    num_id = int(match.group())
                    max_id = max(max_id, num_id)
        # Revisar nodos de control en todas las aristas
        for arista in self.aristas:
            for nodo_control in arista.nodos_control:
                if nodo_control.id.startswith(prefix):
                    match = re.search(r'\d+$', nodo_control.id)
                    if match:
                        num_id = int(match.group())
                        max_id = max(max_id, num_id)

        return f"{prefix}{max_id + 1}" #Retornamos el prefijo más el siguietne numreo
    
        
    def agregar_nodo_interes(self, nombre=None, descripcion=None, posicion=None):
        tipo=0
        id=self.proximo_id(tipo, nombre)
        if not Helpers.hallar_nodo(self.nodos, id):
            self.nodos.append(Nodo(id, nombre, descripcion, None, tipo, None, None, None, posicion))

            
    def agregar_nodo_control (self, arista_index, riesgo=None, accidentalidad=None, popularidad=None, dificultad=None, posicion=None):
        if not (0 <= arista_index < len(self.aristas)):
            print("Índice de arista inválido.")
            return None
        arista = self.aristas[arista_index] 
        id_control = self.proximo_id(tipo=1)
        nodo_control = Nodo(id_control, None, None, riesgo, 1, accidentalidad, popularidad, dificultad)
        arista.agregar_nodo_control(nodo_control)
        return nodo_control
        
    def agregar_arista(self, id_origen, id_destino, peso=1, nodo_control=None, riesgo=None, accidentalidad=None, popularidad=None, dificultad=None, posicion=None):
       
        nodo_origen = Helpers.hallar_nodo(self.nodos, id_origen)
        nodo_destino = Helpers.hallar_nodo(self.nodos, id_destino)

        if id_origen == id_destino:
            print("El nodo de origen y destino no pueden ser el mismo.")
            return None
        
        # Verificar que los nodos existan
        if not nodo_origen or not nodo_destino:
            print("Nodos origen o destino no encontrados.")
            return None
        
        # Verificar que no exista una arista idéntica
        for arista in self.aristas:
            if arista.origen.id == id_origen and arista.destino.id == id_destino:
                print("Ya existe una arista entre estos nodos.")
                return None        
       
        arista = Arista(nodo_origen, nodo_destino, peso)            
        self.aristas.append(arista)
        self.agregar_nodo_control(len(self.aristas)-1, riesgo=None, accidentalidad=None, popularidad=None, dificultad=None, posicion=None)
        return arista
    

    # Elimina un nodo de interés y todas las aristas asociadas.

    def eliminar_nodo_interes(self, id_nodo):
        nodo = Helpers.hallar_nodo(self.nodos, id_nodo)
        if not nodo:
            print(f"El nodo con id {id_nodo} no existe.")
            return False
        # Eliminar todas las aristas que incluyen este nodo como origen o destino
        self.aristas = [
            arista for arista in self.aristas
            if arista.origen.id != id_nodo and arista.destino.id != id_nodo
        ]

        # Eliminar el nodo de la lista de nodos
        self.nodos = [nodo for nodo in self.nodos if nodo.id != id_nodo]

        print(f"Nodo {id_nodo} y sus aristas asociadas eliminados.")
        return True
    # Elimina un nodo de control de la arista especificada.
    # Si la arista queda sin nodos de control, elimina la arista.
    # Si quedan nodos de control, recalcula sus posiciones.
    
    def eliminar_nodo_control(self,id_nodo_control):
        # Buscar la arista que contiene el nodo de control
        arista_idx = Helpers.hallar_indice_arista_por_nodo_control(self.aristas, id_nodo_control)
        if arista_idx == -1:
            print(f"El nodo de control con id {id_nodo_control} no existe en ninguna arista.")
            return False

        arista = self.aristas[arista_idx]

        # Remueve el punto de control de la arista
        arista.remover_nodo_control(id_nodo_control)
       
       # Si no quedan nodos de control, eliminar la arista
        if not arista.nodos_control:
            self.aristas.pop(arista_idx)
            print(f"Arista eliminada porque no tiene nodos de control.")
            return True


        # Eliminar el nodo de control
        arista.nodos_control = [n for n in arista.nodos_control if n.id != id_nodo_control]

        # Si no quedan nodos de control, eliminar la arista
        if not arista.nodos_control:
            self.aristas.pop(arista_idx)
            print(f"Arista eliminada porque no tiene nodos de control.")
            return True

        print(f"Nodo de control {id_nodo_control} eliminado.")
        return True


        
    def validar_eliminacion_nodo(self, nodo_id):
        if nodo_id not in self.nodos:
            return False, "Nodo no existe"
        ##if len(self.nodos) == 1:
            ##return False, "No se puede eliminar el único nodo"
        return True, None

    def validar_nodo(self, id_nodo):
        nodo = self.nodos.get(id_nodo)
        if not nodo:
            return False, "Nodo no existe"
        
        if nodo.tipo == 1:  # Punto de control (amarillo)
            # Restricción 1: Al menos 2 vecinos distintos (entrantes o salientes)
            vecinos_salientes = set(nodo.vecinos.keys())  # Nodos a los que apunta
            vecinos_entrantes = set()
            for otro_nodo in self.nodos.values():
                if id_nodo in otro_nodo.vecinos:
                    vecinos_entrantes.add(otro_nodo.id)
            vecinos_totales = vecinos_salientes.union(vecinos_entrantes)
            if len(vecinos_totales) < 2:
                return False, f"El nodo {id_nodo} debe tener al menos 2 vecinos distintos"
            
            # Restricción 2: Verificar conectividad indirecta a nodos tipo 0
            self.recorridos = Recorridos(self, None)  # Reiniciar recorridos para reflejar cambios
            distancias, _ = self.recorridos.menor_distancia()
            tiene_conexion_indirecta = False
            for otro_nodo in self.nodos:
                if self.nodos[otro_nodo].tipo == 0 and distancias[id_nodo][otro_nodo] < float('inf'):
                    tiene_conexion_indirecta = True
                    break
            
            if not tiene_conexion_indirecta:
                return False, f"El nodo {id_nodo} no tiene conexión directa o indirecta a ningún nodo tipo 0"
            
            return True, None
        
        return True, None  # Nodos tipo 0 (rojos) siempre son válidos

    
    def validar_todos_con_boton(self):
        """Valida todos los nodos tipo 1 y elimina los que no cumplen al presionar un botón."""
        nodos_a_eliminar = []
        for id_nodo in self.nodos:
            if self.nodos[id_nodo].tipo == 1:
                valido, mensaje = self.validar_nodo(id_nodo)
                if not valido:
                    print(f"Error: {mensaje}. Marcando nodo {id_nodo} para eliminación.")
                    nodos_a_eliminar.append(id_nodo)
        for id_nodo in nodos_a_eliminar:
            self.eliminar_nodo(id_nodo)
        if not nodos_a_eliminar:
            print("Todos los nodos tipo 1 cumplen las restricciones.")

   
    
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