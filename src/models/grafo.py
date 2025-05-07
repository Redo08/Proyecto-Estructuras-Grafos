from src.models.arista import Arista
from src.helpers import Helpers
from src.models.nodo import Nodo
from src.models.recorridos import Recorridos
class Grafo:
    def __init__(self):
        self.nodos = [] #Nodo
        self.aristas = []  # Aristas
        self.recorridos = Recorridos(self,None) #Recorridos del grafo

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

        for nodo in self.nodos:
            #Verificamos si el prefio ya existe
            if nodo.id.startswith(prefix):
                #Extraemos los digitos del final
                num_str = ''
                for char in reversed(nodo.id):
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
    
        
    def agregar_nodo_interes(self, id, nombre=None, descripcion=None, riesgo=None, tipo=0, accidentalidad=None, popularidad=None, dificultad=None, posicion=None):
        if id not in self.nodos:
            self.nodos.append(Nodo(id, nombre, descripcion, riesgo, 0, accidentalidad, popularidad, dificultad, posicion))
            
    def agregar_nodo_control(self, id, riesgo, accidentalidad, popularidad, dificultad, posicion):
        return Nodo(id, None, None, riesgo, 1, accidentalidad, popularidad, dificultad, posicion)
    
    def eliminar_nodo(self, id_nodo):
        if Helpers.hallar_id(self.nodos, id_nodo):
            # Eliminar aristas que salen del nodo y las que llegan a él
            for vecino in list(self.nodos[id_nodo].vecinos.keys()):
                self.eliminar_arista(id_nodo, vecino)
            # Eliminar todas las aristas que terminen en el nodo a eliminar
            for otro_nodo in list(self.nodos.keys()):
                if otro_nodo != id_nodo and id_nodo in self.nodos[otro_nodo].vecinos:
                    self.eliminar_arista(otro_nodo, id_nodo)
            # Eliminar el nodo
            self.nodos.
            del self.nodos[id_nodo]

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

    def agregar_arista(self, id_origen, id_destino, peso=1, nodo_control=None):
        if Helpers.hallar_id(self.nodos, id_origen) and Helpers.hallar_id(self.nodos, id_destino):
            arista = Arista(id_origen, id_destino, peso, nodo_control)
            self.aristas.append(arista)
    
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