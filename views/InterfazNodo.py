import pygame
from views.Formulario import Formulario

class InterfazNodo:
    def __init__(self, screen, area_mapa, grafo, interfaz_grafo, on_finish):
        self.screen = screen
        self.area_mapa = area_mapa
        self.grafo = grafo
        self.interfaz_grafo = interfaz_grafo
        self.on_finish = on_finish
        self.esperando_posicion = True
        self.posicion_nuevo_nodo = None
        condiciones = {
            "tipo": {
                "0": ["nombre", "descripcion"],
                "1": ["riesgo", "accidentalidad", "popularidad", "dificultad"]
            }
        }
        self.formulario = None
        self.campos_iniciales = ["tipo"]
        self.condiciones = condiciones

    def manejar_evento(self, event):
        if self.esperando_posicion:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.area_mapa.collidepoint(event.pos):
                    self.posicion_nuevo_nodo = event.pos
                    self.esperando_posicion = False
                    self.formulario = Formulario(self.campos_iniciales, self.condiciones)
        elif self.formulario:
            self.formulario.manejar_evento(event)
            if self.formulario.fue_cancelado():
                self.on_finish()
            elif self.formulario.esta_listo():
                self.procesar_nodo(self.formulario.campos, self.posicion_nuevo_nodo)
                self.on_finish()

    def procesar_nodo(self, data, posicion):
        nuevo_id = self.grafo.proximo_id()
        if data['tipo'] == '0':
            self.grafo.agregar_nodo(nuevo_id, data['nombre'], data['descripcion'], None, 0, None, None, None, posicion)
        elif data['tipo'] == '1':
            self.grafo.agregar_nodo(nuevo_id, None, None, data['riesgo'], 1, data['accidentalidad'], data['popularidad'], data['dificultad'], posicion)
        self.interfaz_grafo.posiciones_nodos = self.interfaz_grafo.calcular_posiciones()

    def dibujar(self):
        if self.formulario:
            self.formulario.dibujar(self.screen, pygame.font.Font(None, 30), self.area_mapa)