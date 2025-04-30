import pygame
class Boton:
    def __init__(self, rect, texto, accion, screen):
        self.screen = screen
        self.rect = rect
        self.texto = texto
        self.accion = accion #Acción asociada al botón
        
    def dibujar(self):
        #Dibujamos el botón
        pygame.draw.rect(self.screen, (0,0,0), self.rect)
        
        fuente = pygame.font.Font(None, 24)
        texto = fuente.render(self.texto, True, (255, 255, 255))
        #Posicionar texto en el centro del boton    
        texto_rect = texto.get_rect(center=self.rect.center)
    
        #Dibujar dentro del centro del boton
        self.screen.blit(texto, texto_rect)
        
    def manejar_evento(self, evento):
        #Si suelta el mouse, osea da un click
        if evento.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(evento.pos):
                self.accion(evento) # Llama a la función asociada
                
            