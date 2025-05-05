import pygame
from views.Formulario import Formulario

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
        self.condiciones = {
            "tipo": {
                "0": ["nombre", "descripcion"],
                "1": ["riesgo", "accidentalidad", "popularidad", "dificultad"]
            }
        } if modo == "agregar" else None
        self.formulario = None
        self.campos_iniciales = ["tipo"] if self.modo == "agregar" else None

    def manejar_evento(self, event):
        #Si es agregar
        if self.esperando_posicion:
            self._manejar_seleccion_posicion(event)
        elif self.esperando_seleccion:
            self._manejar_seleccion_nodo(event)
        elif self.formulario:
            self._manejar_formulario(event)

    def _manejar_seleccion_posicion(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.area_mapa.collidepoint(event.pos):
            self.posicion_nuevo_nodo = event.pos
            self.esperando_posicion = False
            self.formulario = Formulario(self.screen, self.campos_iniciales, self.condiciones, self.area_mapa)
            print(f"Posición seleccionada para nuevo nodo: {self.posicion_nuevo_nodo}")

    def _manejar_seleccion_nodo(self, event):
        nodo_id = self.interfaz_grafo.seleccionar_nodo(event)
        if nodo_id:
            self.nodo_seleccionado = nodo_id
            self.esperando_seleccion = False
            self.interfaz_grafo.resaltar_nodo(nodo_id, color=(0, 0, 255), grosor=4)
            nodo = self.grafo.nodos[nodo_id]
            nombre = nodo.nombre or "CP" if nodo.tipo == 0 else f"CP (Riesgo: {nodo.riesgo})"
            self.formulario = Formulario(self.screen, None, None, self.area_mapa, f"¿Eliminar nodo {nombre}?", accion="eliminar")
            print(f"Formulario de eliminación creado para nodo: {nodo_id}")

    def _manejar_formulario(self, event):
        self.formulario.manejar_evento(event)
        if self.formulario.fue_cancelado():
            print("Acción cancelada.")
            self.interfaz_grafo.limpiar_resaltado()
            self.on_finish()
        elif self.formulario.esta_listo():
            if self.modo == "agregar":
                self._procesar_nodo_agregar()
            elif self.modo == "eliminar":
                self._procesar_nodo_eliminar() 
                
    def _procesar_nodo_agregar(self):
        self.procesar_nodo(self.formulario.campos, self.posicion_nuevo_nodo)
        print(f"Nodo agregado en posición: {self.posicion_nuevo_nodo}")
        self.interfaz_grafo.limpiar_resaltado()
        self.on_finish()

    def _procesar_nodo_eliminar(self):
        try:
            valido, mensaje = self.grafo.validar_eliminacion_nodo(self.nodo_seleccionado)
            if not valido:
                self.formulario = Formulario(self.screen, None, None, self.area_mapa, mensaje, accion="error")
                print(f"Error al eliminar nodo: {mensaje}")
                return
            self.grafo.eliminar_nodo(self.nodo_seleccionado)
            self.interfaz_grafo.posiciones_nodos = self.interfaz_grafo.calcular_posiciones()
            print(f"Nodo {self.nodo_seleccionado} eliminado.")
            self.interfaz_grafo.limpiar_resaltado()
            self.on_finish()
        except Exception as e:
            self.formulario = Formulario(self.screen, None, None, self.area_mapa, f"Error al eliminar nodo: {str(e)}", accion="error")
            print(f"Excepción al eliminar nodo: {str(e)}")

    def procesar_nodo(self, data, posicion):
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
        self.interfaz_grafo.posiciones_nodos = self.interfaz_grafo.calcular_posiciones()

    def dibujar(self):
        if self.formulario:
            self.formulario.dibujar()
       