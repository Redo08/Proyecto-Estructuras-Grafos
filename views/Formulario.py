import pygame
from views.boton import Boton
class Formulario:
    def __init__(self, screen, campos_iniciales, condiciones=None, area_mapa=None):
        self.screen = screen
        self.campos = {campo: "" for campo in campos_iniciales}
        self.orden_campos = list(campos_iniciales)
        self.condiciones = condiciones or {}
        self.indice_campo_actual = 0
        self.completo = False
        self.cancelado = False
        self.form_rect = pygame.Rect(area_mapa.x + 100, area_mapa.y + 100, 400, 300)
        #Botones
        self.botones = [
            Boton(pygame.Rect(self.form_rect.x + 150, self.form_rect.y + 250, 100, 40), "Guardar", self.marcar_completo, self.screen, (0, 255, 0)),
            Boton(pygame.Rect(self.form_rect.x + 270, self.form_rect.y + 250, 100, 40), "Cancelar", self.marcar_cancelado, self.screen, (255, 0, 0))
        ]

    def manejar_evento(self, evento):
        # Si se le da a una tecla
        if evento.type == pygame.KEYDOWN:
            campo_actual = self.orden_campos[self.indice_campo_actual]
            if evento.key == pygame.K_RETURN: # Si se le da enter, continua con el siguiente campo
                # Verificar si el campo actual tiene condiciones
                if campo_actual in self.condiciones and self.campos[campo_actual] in self.condiciones[campo_actual]:
                    nuevos_campos = self.condiciones[campo_actual][self.campos[campo_actual]]
                    for campo in nuevos_campos:
                        if campo not in self.campos:
                            self.campos[campo] = ""
                            self.orden_campos.append(campo)
                self.indice_campo_actual += 1
                if self.indice_campo_actual >= len(self.orden_campos):
                    self.completo = True
            elif evento.key == pygame.K_BACKSPACE: #Si se le da borrar elimina la la ultima letra
                self.campos[campo_actual] = self.campos[campo_actual][:-1]
            else: #Agrega el caracter escrito
                self.campos[campo_actual] += evento.unicode
                
        #Manejar botones
        for boton in self.botones:
            boton.manejar_evento(evento)
            

    def dibujar(self):
        #Dibujar rectangulo 
        pygame.draw.rect(self.screen, (200, 200, 200), self.form_rect)
        instruccion = "Ingrese los datos solicitados"
        superficie_inst = pygame.font.Font(None, 30).render(instruccion, True, (0, 0, 0))
        self.screen.blit(superficie_inst, (self.form_rect.x + 20, self.form_rect.y + 20))
        
        x, y = self.form_rect.x + 20, self.form_rect.y + 60
        for i, campo in enumerate(self.orden_campos):
            if i < self.indice_campo_actual:
                texto = f"{campo}: {self.campos[campo]}"
            elif i == self.indice_campo_actual:
                texto = f"{campo}: {self.campos[campo]}_"
            else:
                texto = f"{campo}: "
            superficie = pygame.font.Font(None, 30).render(texto, True, (0, 0, 0))
            self.screen.blit(superficie, (x, y + i * 30))

        # Dibujar botones
        for boton in self.botones:
            boton.dibujar()

    def marcar_completo(self):
        self.completo = True
        
    def marcar_cancelado(self):
        self.cancelado = True
        
    def esta_listo(self):
        return self.completo

    def fue_cancelado(self):
        return self.cancelado 