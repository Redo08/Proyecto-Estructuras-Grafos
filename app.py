import pygame
from src.Grafo import Graph  # Asegúrate de que la ruta sea correcta
from src.helpers import Helpers
from views.Interfaz import Visualizador

# Inicialización de Pygame
pygame.init()
ANCHO, ALTO = 1300, 650

# Instancias
helpers = Helpers()
grafo = Graph()
grafo.graph = {"C":{"M":10, "D": 15},
               "M": {"C": 12},
               "D": {}}

visualizador = Visualizador(grafo.graph, ANCHO, ALTO)

# Ejecutar el programa
visualizador.ejecutar()