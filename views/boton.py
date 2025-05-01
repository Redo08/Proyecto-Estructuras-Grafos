import pygame
class Boton:
    def __init__(self, rect, texto, accion, screen, color_fondo=(40,40,40), color_texto=(255,255,255)):
        self.screen = screen
        self.rect = rect
        self.texto = texto
        self.accion = accion #Acción asociada al botón
        self.color_fondo = color_fondo
        self.color_texto = color_texto
        self.color_hover = self._oscurecer_color(color_fondo)
        
    def _oscurecer_color(self, color_fondo):
        # Reduce cada componente en 40, sin pasarse de 0 para dar el efecto de hover
        return tuple(max(c - 40, 0) for c in color_fondo)
    
    def dibujar(self):
        #Sacamos posicion del mouse para saber si esta hover o no
        mouse_pos = pygame.mouse.get_pos()
        esta_hover = self.rect.collidepoint(mouse_pos)
        color_actual = self.color_hover if esta_hover else self.color_fondo
        
        #Dibujamos el botón
        pygame.draw.rect(self.screen, color_actual, self.rect)
        
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
                
            