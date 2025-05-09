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
            prefix = nombre[:2].upper() if len(nombre) >= 2 else "PI" #Primeras 2 letras y en mayuscula
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
            nodo=Nodo(id, nombre, descripcion, None, tipo, None, None, None, posicion)
            self.nodos.append(Nodo(id, nombre, descripcion, None, tipo, None, None, None, posicion))
        return nodo
            
    def agregar_nodo_control (self, arista_index, riesgo=None, accidentalidad=None, popularidad=None, dificultad=None):
        if not (0 <= arista_index < len(self.aristas)):
            print("Índice de arista inválido.")
            return None
        arista = self.aristas[arista_index] 
        id_control = self.proximo_id(tipo=1)
        nodo_control = Nodo(id_control, None, None, riesgo, 1, accidentalidad, popularidad, dificultad, None)
        arista.agregar_nodo_control(nodo_control)
        return nodo_control
        
    def agregar_arista(self, id_origen, id_destino, peso=1, nodo_control=None, riesgo=None, accidentalidad=None, popularidad=None, dificultad=None, crear_nodo_control=True):
       
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
        if crear_nodo_control:
            self.agregar_nodo_control(len(self.aristas)-1, riesgo=None, accidentalidad=None, popularidad=None, dificultad=None)
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
            if arista.origen.id != id_nodo and arista.destino.id != id_nodo #Probar si es or
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


        print(f"Nodo de control {id_nodo_control} eliminado.")
        return True
    
    def eliminar_arista(self, id_origen, id_destino):
        """
        Elimina la arista que conecta los nodos con id_origen y id_destino.
        Retorna True si se eliminó, False si no se encontró.
        """
        arista_idx = Helpers.hallar_indice_arista_por_nodos(self.aristas, id_origen, id_destino)
        if arista_idx == -1:
            print(f"No se encontró arista entre {id_origen} y {id_destino}.")
            return False

        self.aristas.pop(arista_idx)
        print(f"Arista entre {id_origen} y {id_destino} eliminada.")
        return True

    ## TOCA CAMBIAR ##
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
    """
    def eliminar_arista(self, id_origen, id_destino):
        # Buscamos la arista especifica
        for arista in self.aristas[:]: #Recorremos una copia de la lista
            if arista.origen == id_origen and arista.destino == id_destino:
                # Eliminamos la arista de la lista
                self.aristas.remove(arista)
                return #Se sale despues de salir """

    def cargar_json(self, datos):
        if datos is not None:
            #Agregar nodos
            for nodo in datos['nodos']:
                if nodo['tipo'] == 0:
                    self.agregar_nodo_interes(
                        nombre=nodo['nombre'],
                        descripcion=nodo['descripcion'],
                        posicion=nodo.get('posicion')
                    )

            #Agregar aristas y sus nodos de control
            for arista in datos['aristas']:
                id_origen = arista['origen'],
                id_destino = arista['destino'],
                if isinstance(id_origen, (tuple, list)):
                    id_origen = id_origen[0] if id_origen else ""
                if isinstance(id_destino, (tuple, list)):
                    id_destino = id_destino[0] if id_destino else ""                
                
                peso = arista['peso']
                nodos_control = arista.get('nodos_control', [])
                
                # Depuración: Imprimir IDs para verificar
                print(f"Procesando arista: id_origen={id_origen}, id_destino={id_destino}, peso={peso}")
                
                # Crear la arista   
                arista = self.agregar_arista(
                    id_origen=id_origen,
                    id_destino=id_destino,
                    peso=peso,
                    crear_nodo_control=False
                )
                
                if arista:
                    #Añadir nodos de control
                    for nodo_control in nodos_control:
                        nodo_control = Nodo(
                            id=nodo_control['id'],
                            nombre=None,
                            descripcion=None,
                            riesgo=nodo_control['riesgo'],
                            tipo=1,
                            accidentalidad=nodo_control['accidentalidad'],
                            popularidad=nodo_control['popularidad'],
                            dificultad=nodo_control['dificultad'],
                            posicion=nodo_control.get('posicion')
                        )
                        arista.agregar_nodo_control(nodo_control)
                else:
                    print(f"No se pudo crear la arista: {id_origen} -> {id_destino} ")            
    
    ## TOCA CAMBIAR ##  
    def guardar_json(self):
        data = {
            "nodos": [],
            "aristas": []
        }
        
        #Guardar nodos
        for nodo in self.nodos:
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
            
        # Guardar aristas
        for arista in self.aristas:
            nodos_control = []
            for nodo_control in arista.nodos_control:
                nodos_control.append({
                    "id": nodo_control.id,
                    "nombre": None,
                    "descripcion": None,
                    "riesgo": nodo_control.riesgo,
                    "tipo": 1,
                    "accidentalidad": nodo_control.accidentalidad,
                    "popularidad": nodo_control.popularidad,
                    "dificultad": nodo_control.dificultad,
                    "posicion": nodo_control.posicion if nodo_control.posicion else None
                })
                
            data["aristas"].append({
                "origen": arista.origen.id,
                "destino": arista.destino.id,
                "peso": arista.peso,
                "nodos_control": nodos_control
            })
            
        return data 