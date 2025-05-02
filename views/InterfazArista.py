import pygame
from views.Formulario import Formulario

class InterfazArista:
    def __init__(self, screen, area_mapa, grafo, interfaz_grafo, on_finish, modo):
        self.screen = screen
        self.area_mapa = area_mapa
        self.grafo = grafo
        self.interfaz_grafo = interfaz_grafo
        self.on_finish = on_finish
        self.modo = modo  # "agregar_arista" o "eliminar_arista"
        self.esperando_primer_nodo = True
        self.esperando_segundo_nodo = False
        self.primer_nodo = None
        self.segundo_nodo = None
        self.formulario = None
        self.campos_iniciales = ["peso"] if modo == "agregar_arista" else None
        self.condiciones = None

    def manejar_evento(self, event):
        if self.esperando_primer_nodo:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.area_mapa.collidepoint(event.pos):
                    nodo_id = self.interfaz_grafo.obtener_nodo_seleccionado(event.pos)
                    if nodo_id:
                        self.primer_nodo = nodo_id
                        self.esperando_primer_nodo = False
                        self.esperando_segundo_nodo = True
                        print(f"Primer nodo seleccionado: {nodo_id}")
                    else:
                        print("No se seleccionó un nodo válido.")
        elif self.esperando_segundo_nodo:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.area_mapa.collidepoint(event.pos):
                    nodo_id = self.interfaz_grafo.obtener_nodo_seleccionado(event.pos)
                    if nodo_id and nodo_id != self.primer_nodo:
                        self.segundo_nodo = nodo_id
                        self.esperando_segundo_nodo = False
                        print(f"Segundo nodo seleccionado: {nodo_id}")
                        if self.modo == "agregar_arista":
                            self.formulario = Formulario(
                                self.screen, self.campos_iniciales, None, self.area_mapa,
                                accion="agregar_arista"
                            )
                        elif self.modo == "eliminar_arista":
                            nodo1 = self.grafo.nodos[self.primer_nodo]
                            nodo2 = self.grafo.nodos[self.segundo_nodo]
                            nombre1 = nodo1.nombre or "CP" if nodo1.tipo == 0 else f"CP (Riesgo: {nodo1.riesgo})"
                            nombre2 = nodo2.nombre or "CP" if nodo2.tipo == 0 else f"CP (Riesgo: {nodo2.riesgo})"
                            mensaje = f"¿Eliminar arista entre {nombre1} y {nombre2}?"
                            self.formulario = Formulario(
                                self.screen, None, None, self.area_mapa, mensaje,
                                accion="eliminar_arista"
                            )
                    else:
                        print("Seleccione un segundo nodo diferente al primero.")
        elif self.formulario:
            self.formulario.manejar_evento(event)
            if self.formulario.fue_cancelado():
                print(f"Acción de {self.modo} cancelada.")
                self.on_finish()
            elif self.formulario.esta_listo():
                if self.modo == "agregar_arista":
                    try:
                        peso = float(self.formulario.campos["peso"])
                        if peso <= 0:
                            self.formulario = Formulario(
                                self.screen, None, None, self.area_mapa,
                                "El peso debe ser un número positivo.", accion="error"
                            )
                            return
                        valido, mensaje = self.grafo.validar_agregar_arista(self.primer_nodo, self.segundo_nodo)
                        if not valido:
                            self.formulario = Formulario(
                                self.screen, None, None, self.area_mapa, mensaje, accion="error"
                            )
                            return
                        self.grafo.agregar_arista(self.primer_nodo, self.segundo_nodo, peso)
                        self.interfaz_grafo.posiciones_nodos = self.interfaz_grafo.calcular_posiciones()
                        print(f"Arista agregada: {self.primer_nodo} -> {self.segundo_nodo}, peso: {peso}")
                    except ValueError:
                        self.formulario = Formulario(
                            self.screen, None, None, self.area_mapa,
                            "El peso debe ser un número válido.", accion="error"
                        )
                        return
                elif self.modo == "eliminar_arista":
                    try:
                        valido, mensaje = self.grafo.validar_eliminar_arista(self.primer_nodo, self.segundo_nodo)
                        if not valido:
                            self.formulario = Formulario(
                                self.screen, None, None, self.area_mapa, mensaje, accion="error"
                            )
                            return
                        self.grafo.eliminar_arista(self.primer_nodo, self.segundo_nodo)
                        self.interfaz_grafo.posiciones_nodos = self.interfaz_grafo.calcular_posiciones()
                        print(f"Arista eliminada: {self.primer_nodo} -> {self.segundo_nodo}")
                    except Exception as e:
                        self.formulario = Formulario(
                            self.screen, None, None, self.area_mapa,
                            f"Error al eliminar arista: {str(e)}", accion="error"
                        )
                        return
                self.on_finish()

    def dibujar(self):
        if self.formulario:
            self.formulario.dibujar()
        else:
            # Resaltar nodos seleccionados
            if self.primer_nodo:
                pos = self.interfaz_grafo.posiciones_nodos.get(self.primer_nodo)
                if pos:
                    pygame.draw.circle(self.screen, (0, 255, 0), pos, 18, 2)
            if self.segundo_nodo:
                pos = self.interfaz_grafo.posiciones_nodos.get(self.segundo_nodo)
                if pos:
                    pygame.draw.circle(self.screen, (0, 255, 0), pos, 18, 2)
            # Resaltar arista en modo eliminar_arista si ambos nodos están seleccionados
            if self.modo == "eliminar_arista" and self.primer_nodo and self.segundo_nodo:
                if self.primer_nodo in self.grafo.nodos and self.segundo_nodo in self.grafo.nodos[self.primer_nodo].vecinos:
                    self.interfaz_grafo.resaltar_arista(self.primer_nodo, self.segundo_nodo)