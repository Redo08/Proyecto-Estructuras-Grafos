import pygame
from src.helpers import Helpers
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
            self._manejar_seleccion_primer_nodo(event)
        elif self.esperando_segundo_nodo:
            self._manejar_seleccion_segundo_nodo(event)
        elif self.formulario:
            self._manejar_formulario(event)

    def _manejar_seleccion_primer_nodo(self, event):
        nodo_id = self.interfaz_grafo.seleccionar_nodo(event)
        if nodo_id:
            self.primer_nodo = nodo_id
            self.esperando_primer_nodo = False
            self.esperando_segundo_nodo = True
            self.interfaz_grafo.resaltar_nodo(nodo_id, color=(0, 255, 0), grosor=2)
            print(f"Primer nodo asignado: {nodo_id}")

    def _manejar_seleccion_segundo_nodo(self, event):
        nodo_id = self.interfaz_grafo.seleccionar_nodo(event)
        if nodo_id and nodo_id != self.primer_nodo:
            self.segundo_nodo = nodo_id
            self.esperando_segundo_nodo = False
            self.interfaz_grafo.resaltar_nodo(nodo_id, color=(0, 255, 0), grosor=2)
            print(f"Segundo nodo asignado: {nodo_id}")
            arista_existe = (self.primer_nodo in self.grafo.nodos and self.segundo_nodo in self.grafo.nodos and self.segundo_nodo in self.grafo.nodos[self.primer_nodo].vecinos)
            if self.modo == "agregar_arista":
                self.formulario = Formulario(self.screen, self.campos_iniciales, None, self.area_mapa, accion="agregar_arista")
            elif self.modo == "eliminar_arista":
                nodo1, nodo2 = self.grafo.nodos[self.primer_nodo], self.grafo.nodos[self.segundo_nodo]
                nombre1 = nodo1.nombre or "CP" if nodo1.tipo == 0 else f"CP (Riesgo: {nodo1.riesgo})"
                nombre2 = nodo2.nombre or "CP" if nodo2.tipo == 0 else f"CP (Riesgo: {nodo2.riesgo})"
                mensaje = f"¿Eliminar arista entre {nombre1} y {nombre2}?"
                if arista_existe:
                    self.interfaz_grafo.resaltar_arista(self.primer_nodo, self.segundo_nodo, color=(255, 255, 0), grosor=8)
                else:
                    mensaje += " (No existe arista)"
                self.formulario = Formulario(self.screen, None, None, self.area_mapa, mensaje, accion="eliminar_arista")

    def _manejar_formulario(self, event):
        self.formulario.manejar_evento(event)
        if self.formulario.fue_cancelado():
            print(f"Acción de {self.modo} cancelada.")
            self.interfaz_grafo.limpiar_resaltado()
            self.on_finish()
        elif self.formulario.esta_listo():
            if self.modo == "agregar_arista":
                self._procesar_agregar_arista()
            elif self.modo == "eliminar_arista":
                self._procesar_eliminar_arista()

    def _procesar_agregar_arista(self):
        try:
            peso = Helpers.quitar_decimales_si_no_hay(float(self.formulario.campos["peso"]))
            if peso <= 0:
                self.formulario = Formulario(self.screen, None, None, self.area_mapa, "El peso debe ser positivo.", accion="error")
                return
            valido, mensaje = self.grafo.validar_agregar_arista(self.primer_nodo, self.segundo_nodo)
            if not valido:
                self.formulario = Formulario(self.screen, None, None, self.area_mapa, mensaje, accion="error")
                return
            self.grafo.agregar_arista(self.primer_nodo, self.segundo_nodo, peso)
            self.interfaz_grafo.posiciones_nodos = self.interfaz_grafo.calcular_posiciones()
            print(f"Arista agregada: {self.primer_nodo} -> {self.segundo_nodo}, peso: {peso}")
            self.interfaz_grafo.limpiar_resaltado()
            self.on_finish()
        except ValueError:
            self.formulario = Formulario(self.screen, None, None, self.area_mapa, "Peso inválido.", accion="error")

    def _procesar_eliminar_arista(self):
        try:
            valido, mensaje = self.grafo.validar_eliminar_arista(self.primer_nodo, self.segundo_nodo)
            if not valido:
                self.formulario = Formulario(self.screen, None, None, self.area_mapa, mensaje, accion="error")
                return
            self.grafo.eliminar_arista(self.primer_nodo, self.segundo_nodo)
            self.interfaz_grafo.posiciones_nodos = self.interfaz_grafo.calcular_posiciones()
            print(f"Arista eliminada: {self.primer_nodo} -> {self.segundo_nodo}")
            self.interfaz_grafo.limpiar_resaltado()
            self.on_finish()
        except Exception as e:
            self.formulario = Formulario(self.screen, None, None, self.area_mapa, f"Error: {str(e)}", accion="error")            
            

    def dibujar(self):
        if self.formulario:
            self.formulario.dibujar()
       