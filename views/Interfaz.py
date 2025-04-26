import pygame

class Visualizador:
    def __init__(self, grafo, ancho, alto):
        self.grafo = grafo
        self.ancho = ancho
        self.alto = alto
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Visualizador de Grafos Escalable")
        self.clock = pygame.time.Clock()
        self.area_mapa = pygame.Rect(0, 0, ancho * 0.50, alto)  # 75% del ancho para el mapa
        self.area_control = pygame.Rect(ancho * 0.75, 0, ancho * 0.50, alto)  # 25% para controles
        self.nodo_seleccionado = None
        self.running = True

    def dibujar(self):
        """Dibuja el grafo y la interfaz en la pantalla"""
        # Colores
        NEGRO = (0, 0, 0)
        BLANCO = (255, 255, 255)
        ROJO = (255, 0, 0)
        GRIS = (150, 150, 150)

        # Fondo
        self.screen.fill(BLANCO)
        pygame.draw.rect(self.screen, GRIS, self.area_control)  # Área de control en gris

        # Dibujar aristas
        for nodo, vecinos in self.grafo.adyacencia.items():
            for vecino in vecinos:
                pygame.draw.line(self.screen, BLANCO, self.grafo.nodos[nodo], self.grafo.nodos[vecino])

        # Dibujar nodos
        for nodo in self.grafo.nodos:
            pygame.draw.circle(self.screen, ROJO, nodo, 10)

        # Dibujar botón "Cargar mapa"
        boton_rect = pygame.Rect(self.area_control.x + 20, 50, 150, 40)
        pygame.draw.rect(self.screen, BLANCO, boton_rect)
        font = pygame.font.Font(None, 30)
        texto = font.render("Cargar mapa", True, NEGRO)
        self.screen.blit(texto, (boton_rect.x + 10, boton_rect.y + 10))

    def manejar_eventos(self):
        """Maneja los eventos de Pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posicion = event.pos
                # Verificar si el clic está en el área del mapa
                if self.area_mapa.collidepoint(posicion):
                    nodo_clicado = self.grafo.obtener_nodo_en_posicion(posicion)
                    if nodo_clicado is not None:
                        if self.nodo_seleccionado is None:
                            self.nodo_seleccionado = nodo_clicado
                        else:
                            self.grafo.agregar_arista(self.nodo_seleccionado, nodo_clicado)
                            self.nodo_seleccionado = None
                    else:
                        self.grafo.agregar_nodo(posicion)
                # Verificar clic en el botón (funcionalidad placeholder)
                elif self.area_control.collidepoint(posicion):
                    boton_rect = pygame.Rect(self.area_control.x + 20, 50, 150, 40)
                    if boton_rect.collidepoint(posicion):
                        print("Botón 'Cargar mapa' presionado (funcionalidad por implementar)")

    def ejecutar(self):
        """Ejecuta el bucle principal del juego"""
        while self.running:
            self.manejar_eventos()  # Manejar eventos
            self.dibujar()  # Dibujar
            pygame.display.flip()  # Actualizar pantalla
            self.clock.tick(60)  # 60 FPS
        pygame.quit()