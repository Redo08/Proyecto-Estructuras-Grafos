import pygame
from src.grafo2 import Grafo  # Asegúrate de que la ruta sea correcta
from views.Interfaz import Visualizador

# Inicialización de Pygame
pygame.init()
ANCHO, ALTO = 1300, 760

# Instancias
grafo = Grafo()
visualizador = Visualizador(grafo, ANCHO, ALTO)

# Ejecutar el programa
visualizador.ejecutar()