import pygame
from grafo2 import Grafo
from views.Interfaz import Visualizador

# Inicialización de Pygame
pygame.init()
ANCHO, ALTO = 1300, 760

# Instancias
grafo = Grafo()
visualizador = Visualizador(grafo, ANCHO, ALTO)

# Ejecutar el programa
visualizador.ejecutar()