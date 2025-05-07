from src.helpers import Helpers
class Arista:
    def __init__(self, origen, destino, peso=1):
        self.origen = origen
        self.destino = destino #Id del nodo destino
        self.peso = peso
        self.nodos_control = [] # => Id nodo_control: Nodo(tipo=1)

    def actualizar_posiciones(self, pos_origen, pos_destino):
        n= len(self.nodos_control)
        if n==0:
            return
        for i,nodo_control in enumerate(self.nodos_control):  #enumerate permite obtener tanto el índice como el elemento en una sola pasada por la lista, evitando la necesidad de manejar índices manualmente
            t=(i+1)/(n+1) # Factor de interpolación
            x= pos_origen[0] + t*(pos_destino[0]-pos_origen[0])
            y= pos_origen[1] + t*(pos_destino[1]-pos_origen[1])
            nodo_control.posicion = (x,y)

    # Añade un nodo de control a la arista y actualiza posiciones si es posible.
    def agregar_nodo_control(self, nodo_control):
        
        self.nodos_control.append(nodo_control)
        if self.origen.posicion and self.destino.posicion:
            self.actualizar_posiciones(self.origen.posicion, self.destino.posicion)
    
    def remover_nodo_control(self, id_nodo_control):
        """
        Elimina un nodo de control de la lista nodos_control por su ID.
        Retorna True si se eliminó, False si no se encontró.
        """
        nodo_control = Helpers.hallar_nodo(self.nodos_control, id_nodo_control)
        if not nodo_control:
            return False
        self.nodos_control.remove(nodo_control)
        # Si quedan nodos de control, recalcular posiciones
        if self.nodos_control and self.origen.posicion and self.destino.posicion:
            self.actualizar_posiciones(self.origen.posicion, self.destino.posicion)
        return True