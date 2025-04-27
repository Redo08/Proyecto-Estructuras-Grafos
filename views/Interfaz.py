import pygame
from src.helpers import Helpers
from views.interfazGrafo import InterfazGrafo


class Visualizador:
    def __init__(self, grafo, ancho, alto):
        self.grafo = grafo
        self.ancho = ancho
        self.alto = alto
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Visualizador de Grafos Escalable")
        self.clock = pygame.time.Clock()
        
        #Configuración Areas
        self.altura_titulo = 50
        self.area_titulo = pygame.Rect(0, 0, ancho, self.altura_titulo)  # Área del título
        margen = 10 
        self.area_mapa = pygame.Rect(margen, self.altura_titulo+margen, ancho * 0.60 -2 * margen, alto-self.altura_titulo-2 * margen)  # 75% del ancho para el mapa
        self.area_control = pygame.Rect(ancho * 0.60, 0, ancho * 0.4, alto)  # 25% para controles
        
        #Grafo
        self.interfaz_grafo = InterfazGrafo(self.grafo, self.area_mapa, self.screen)
        
        #Estado
        self.running = True
    
    def dibujar(self):
        """Dibuja el grafo y la interfaz en la pantalla"""
        # Colores
        NEGRO = (0, 0, 0)
        BLANCO = (255, 255, 255)
        ROJO = (255, 0, 0)
        GRIS = (150, 150, 150)
        VERDE = (0, 255, 0)
    
        # Fondo
        self.screen.fill(BLANCO)
    
        # Titulo
        font = pygame.font.Font(None, 36)
        texto_mapa = font.render("MAPA", True, NEGRO)
        ancho_texto = texto_mapa.get_width()
        pos_x = (self.ancho * 0.6 / 2) - (ancho_texto / 2)
        pos_y = (self.altura_titulo / 2) - (texto_mapa.get_height() / 2)
        self.screen.blit(texto_mapa, (pos_x, pos_y))
        
        # Dibujar áreas
        pygame.draw.rect(self.screen, NEGRO, self.area_mapa, 2)
        pygame.draw.rect(self.screen, GRIS, self.area_control)
        
        # Dibujar grafo
        self.interfaz_grafo.dibujar()
        
        #Botones
        botones = [("Cargar mapa", 20, 50, 150, 40)]
        for i in botones:
            self.generar_botones(i[0], i[1], i[2], i[3], i[4])

    def generar_botones(self, nombre_boton, p1, p2, p3, p4):
        boton = pygame.Rect(self.area_control.x + p1, p2, p3, p4)
        pygame.draw.rect(self.screen, (0,0,0), boton)
        texto_cargar = pygame.font.Font(None, 24).render(nombre_boton, True, (255, 255, 255))
        self.screen.blit(texto_cargar, (boton.x + 10, boton.y + 10))
 
    def manejar_eventos(self):
        """Maneja los eventos de Pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posicion = event.pos
                
                # Verificar si el clic está en cargar mapa
                boton_rect = pygame.Rect(self.area_control.x + 20, 50, 150, 40)
                if boton_rect.collidepoint(posicion):
                    grafo = Helpers.cargar_texto()
                    if grafo:    
                        self.grafo = grafo
                        self.interfaz_grafo = InterfazGrafo(grafo, self.area_mapa, self.screen)
                        
                    
    def ejecutar(self):
        """Ejecuta el bucle principal del juego"""
        while self.running:
            self.manejar_eventos()  # Manejar eventos
            self.dibujar()  # Dibujar
            pygame.display.flip()  # Actualizar pantalla
            self.clock.tick(60)  # 60 FPS
        pygame.quit()