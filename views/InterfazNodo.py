import pygame
from views.Formulario import Formulario
import math

class InterfazNodo:
    def __init__(self, screen, area_mapa, grafo, interfaz_grafo, on_finish, modo):
        self.screen = screen
        self.area_mapa = area_mapa
        self.grafo = grafo
        self.interfaz_grafo = interfaz_grafo
        self.on_finish = on_finish
        self.modo = modo  # "agregar" o "eliminar"
        self.esperando_posicion = self.modo == "agregar"
        self.esperando_seleccion = self.modo == "eliminar"
        self.nodo_seleccionado = None
        self.posicion_nuevo_nodo = None
        
        self.formulario = None
        #self.campos_iniciales = ["tipo"] if self.modo == "agregar" else None

    def manejar_evento(self, event):
        #Si es agregar
        if self.esperando_posicion:
            self._manejar_seleccion_posicion(event)
        elif self.esperando_seleccion:
            self._manejar_seleccion_nodo(event)
        elif self.formulario:
            self._manejar_formulario(event)

    def _manejar_seleccion_posicion(self, event):
        """Captura la posición donde se agregará el nodo."""
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.area_mapa.collidepoint(event.pos):
            self.posicion_nuevo_nodo = event.pos
            self.esperando_posicion = False
            # Crear formulario con campos iniciales
            campos_iniciales = ["nombre", "descripcion"]
            self.formulario = Formulario(self.screen, campos_iniciales,None, self.area_mapa)
            print(f"Posición seleccionada para nuevo nodo: {self.posicion_nuevo_nodo}")

    def _manejar_seleccion_nodo(self, event):
        """Selecciona un nodo para eliminar (modo eliminar)."""
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.area_mapa.collidepoint(event.pos):
            nodo = self.interfaz_grafo.seleccionar_nodo(event)
            self.nodo_seleccionado = nodo
            if nodo is not None:
                # Resaltar el nodo seleccionado
                self.nodo_seleccionado = nodo
                self.interfaz_grafo.nodos_resaltados.append(nodo)
                self.esperando_seleccion = False
                # Mostrar formulario de confirmación
                self.formulario = Formulario(self.screen, [], None, self.area_mapa, 
                                            f"¿Eliminar nodo {nodo.id}?", accion="confirmar")
            else:
                self.esperando_seleccion = False
                self.formulario = Formulario(self.screen, [], None, self.area_mapa, "Error: No se seleccionó ningún nodo.", accion="error")

   
    
    def _manejar_formulario(self, event):
        self.formulario.manejar_evento(event)
        if self.formulario.fue_cancelado():
            print("Acción cancelada.")
            self.interfaz_grafo.limpiar_resaltado()
            self.nodo_seleccionado = None
            self.on_finish()
        elif self.formulario.esta_listo():
            if self.modo == "agregar":
                self.agregar_nodo()
            elif self.modo == "eliminar":
                if self.formulario.accion == "confirmar" and self.nodo_seleccionado is not None:
                    self.eliminar_nodo(self.nodo_seleccionado)
                else:
                    # Formulario de error, solo cerrar                    
                    self.interfaz_grafo.limpiar_resaltado()
                    self.nodo_seleccionado = None
                    self.on_finish()
                
    

    def eliminar_nodo(self,nodo):
        """Elimina un nodo del grafo (modo eliminar)."""
        # Eliminar nodo del grafo
        if nodo.tipo == 0:
            self.grafo.eliminar_nodo_interes(nodo.id)
        if nodo.tipo == 1:
            self.grafo.eliminar_nodo_control(nodo.id)

        self.interfaz_grafo.limpiar_resaltado()
        self.nodo_seleccionado = None
        # Imprimir mensaje
        print(f"Nodo {nodo.id} eliminado.")
        self.on_finish() 

    def agregar_nodo(self):
        data = self.formulario.campos
        nombre = data.get("nombre", "Indefinido").strip()
        descripcion = data.get("descripcion", "").strip()
        nodo=self.grafo.agregar_nodo_interes(nombre, descripcion, posicion=self.posicion_nuevo_nodo)
        # Actualizar visualización
        
        print(f"Nodo {nodo.id} agregado en posición: {self.posicion_nuevo_nodo}")
        self.on_finish()
        """
        if self.grafo.hallar_id(self.grafo.nodos, id_nodo):
            raise ValueError("El ID ya existe en el grafo.")
        
        if data['tipo'] == '0':
            nombre = data['nombre'].strip() or "Indefinido"
            nuevo_id = self.grafo.proximo_id(0, nombre)
            self.grafo.agregar_nodo(nuevo_id, nombre, data['descripcion'], None, 0, None, None, None, posicion)
        elif data['tipo'] == '1':
            nuevo_id = self.grafo.proximo_id(1)
            riesgo = str(data['riesgo']).strip() or "Desconocido"
            accidentalidad = str(data['accidentalidad']).strip() or "Desconocido"
            popularidad = str(data['popularidad']).strip() or "Desconocido"
            dificultad = str(data['dificultad']).strip() or "Desconocido"
            self.grafo.agregar_nodo(nuevo_id, None, None, riesgo, 1, accidentalidad, popularidad, dificultad, posicion)
        self.interfaz_grafo.posiciones_nodos = self.interfaz_grafo.calcular_posiciones() """

    def dibujar(self):
        if self.formulario:
            self.formulario.dibujar()
       