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
        if self.esperando_posicion:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.area_mapa.collidepoint(event.pos):
                    self.posicion_nuevo_nodo = event.pos
                    self.esperando_posicion = False
                    self.formulario = Formulario(self.screen, self.campos_iniciales, self.condiciones, self.area_mapa)
        elif self.esperando_seleccion:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.area_mapa.collidepoint(event.pos):
                    nodo_id = self.interfaz_grafo.obtener_nodo_seleccionado(event.pos)
                    if nodo_id:
                        self.nodo_seleccionado = nodo_id
                        self.esperando_seleccion = False
                        nodo = self.grafo.nodos[nodo_id]
                        nombre = nodo.nombre or "CP" if nodo.tipo == 0 else f"CP (Riesgo: {nodo.riesgo})"
                        mensaje = f"¿Eliminar nodo {nombre}?"
                        self.formulario = Formulario(self.screen, None, None, self.area_mapa, mensaje, accion="eliminar")
                    else:
                        print("No se seleccionó ningún nodo.")
        elif self.formulario:
            self.formulario.manejar_evento(event)
            if self.formulario.fue_cancelado():
                print("Acción de eliminación cancelada." if self.modo == "eliminar" else "Acción de agregar cancelada.")
                self.on_finish()
            elif self.formulario.esta_listo():
                if self.modo == "agregar":
                    self.procesar_nodo(self.formulario.campos, self.posicion_nuevo_nodo)
                    print(f"Nodo agregado en posición: {self.posicion_nuevo_nodo}")
                elif self.modo == "eliminar":
                    try:
                        valido, mensaje = self.grafo.validar_eliminacion_nodo(self.nodo_seleccionado)
                        if not valido:
                            self.formulario = Formulario(self.screen, None, None, self.area_mapa, mensaje, accion="error")
                            return
                        self.grafo.eliminar_nodo(self.nodo_seleccionado)
                        self.interfaz_grafo.posiciones_nodos = self.interfaz_grafo.calcular_posiciones()
                        print(f"Nodo {self.nodo_seleccionado} eliminado.")
                    except Exception as e:
                        self.formulario = Formulario(self.screen, None, None, self.area_mapa, f"Error al eliminar nodo: {str(e)}", accion="error")
                        return
                self.on_finish()

    def procesar_nodo(self, data, posicion):
        nuevo_id = self.grafo.proximo_id()
        if data['tipo'] == '0':
            nombre = data['nombre'].strip() or "SinNombre"
            self.grafo.agregar_nodo(nuevo_id, nombre, data['descripcion'], None, 0, None, None, None, posicion)
        elif data['tipo'] == '1':
            riesgo = str(data['riesgo']).strip() or "Desconocido"
            accidentalidad = str(data['accidentalidad']).strip() or "Desconocido"
            popularidad = str(data['popularidad']).strip() or "Desconocido"
            dificultad = str(data['dificultad']).strip() or "Desconocido"
            self.grafo.agregar_nodo(nuevo_id, None, None, riesgo, 1, accidentalidad, popularidad, dificultad, posicion)
        self.interfaz_grafo.posiciones_nodos = self.interfaz_grafo.calcular_posiciones()

    def dibujar(self):
        if self.formulario:
            self.formulario.dibujar()
        elif self.nodo_seleccionado and self.modo == "eliminar":
            pos = self.interfaz_grafo.posiciones_nodos.get(self.nodo_seleccionado)
            if pos:
                pygame.draw.circle(self.screen, (0, 255, 0), pos, 18, 2)  # Resaltar nodo