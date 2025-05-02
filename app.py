import pygame
from src.models.grafo import Grafo  # Asegúrate de que la ruta sea correcta
from src.helpers import Helpers
from views.Interfaz import Visualizador

# Inicialización de Pygame
pygame.init()
ANCHO, ALTO = 1300, 650

# Instancias
helpers = Helpers()
grafo = Grafo()
data = helpers.cargar_texto_manual("archivos/pordefecto.json")
grafo.cargar_json(data)

visualizador = Visualizador(grafo, ANCHO, ALTO)

# Ejecutar el programa
visualizador.ejecutar()