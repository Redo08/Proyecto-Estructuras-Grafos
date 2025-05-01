import pygame
class Boton:
    def __init__(self, rect, texto, accion, screen, color_fondo=(0,0,0), color_texto=(255,255,255)):
        self.screen = screen
        self.rect = rect
        self.texto = texto
        self.accion = accion #Acción asociada al botón
        self.color_fondo = color_fondo
        self.color_texto = color_texto
        
        
    def dibujar(self):
        #Dibujamos el botón
        pygame.draw.rect(self.screen, self.color_fondo, self.rect)
        
        fuente = pygame.font.Font(None, 24)
        texto = fuente.render(self.texto, True, self.color_texto)
        #Posicionar texto en el centro del boton    
        texto_rect = texto.get_rect(center=self.rect.center)
    
        #Dibujar dentro del centro del boton
        self.screen.blit(texto, texto_rect)
        
    def manejar_evento(self, evento):
        #Si suelta el mouse, osea da un click
        if evento.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(evento.pos):
                self.accion() # Llama a la función asociada
                
            