import pygame
from src.models.grafo import Grafo  # Asegúrate de que la ruta sea correcta
from src.helpers import Helpers
from views.Interfaz import Visualizador

# Inicialización de Pygame
pygame.init()
ANCHO, ALTO = 1350, 650

# Instancias
grafo = Grafo()
data = Helpers.cargar_texto_manual("archivos/nuevoJson.json")
grafo.cargar_json(data)

visualizador = Visualizador(grafo, ANCHO, ALTO)

# Ejecutar el programa
visualizador.ejecutar()