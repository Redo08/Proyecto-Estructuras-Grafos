import pygame

class Formulario:
    def __init__(self,campos_iniciales,condiciones=None):
        self.campos = {campo: "" for campo in campos_iniciales}
        self.orden_campos = list(campos_iniciales)
        self.condiciones = condiciones or {}
        self.indice_campo_actual = 0
        self.completo = False
        self.cancelado = False
        self.form_rect = None
    import pygame

class Formulario:
    def __init__(self, campos_iniciales, condiciones=None):
        self.campos = {campo: "" for campo in campos_iniciales}
        self.orden_campos = list(campos_iniciales)
        self.condiciones = condiciones or {}
        self.indice_campo_actual = 0
        self.completo = False
        self.cancelado = False
        self.form_rect = None

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            campo_actual = self.orden_campos[self.indice_campo_actual]
            if evento.key == pygame.K_RETURN:
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
            elif evento.key == pygame.K_BACKSPACE:
                self.campos[campo_actual] = self.campos[campo_actual][:-1]
            else:
                self.campos[campo_actual] += evento.unicode
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            guardar_rect = pygame.Rect(self.form_rect.x + 150, self.form_rect.y + 250, 100, 40)
            cancelar_rect = pygame.Rect(self.form_rect.x + 270, self.form_rect.y + 250, 100, 40)
            if guardar_rect.collidepoint(evento.pos):
                self.completo = True
            elif cancelar_rect.collidepoint(evento.pos):
                self.cancelado = True

    def dibujar(self, pantalla, fuente, area_mapa):
        self.form_rect = pygame.Rect(area_mapa.x + 100, area_mapa.y + 100, 400, 300)
        pygame.draw.rect(pantalla, (200, 200, 200), self.form_rect)
        instruccion = "Ingrese los datos solicitados"
        superficie_inst = fuente.render(instruccion, True, (0, 0, 0))
        pantalla.blit(superficie_inst, (self.form_rect.x + 20, self.form_rect.y + 20))
        
        x, y = self.form_rect.x + 20, self.form_rect.y + 60
        for i, campo in enumerate(self.orden_campos):
            if i < self.indice_campo_actual:
                texto = f"{campo}: {self.campos[campo]}"
            elif i == self.indice_campo_actual:
                texto = f"{campo}: {self.campos[campo]}_"
            else:
                texto = f"{campo}: "
            superficie = fuente.render(texto, True, (0, 0, 0))
            pantalla.blit(superficie, (x, y + i * 30))

        guardar_rect = pygame.Rect(self.form_rect.x + 150, self.form_rect.y + 250, 100, 40)
        pygame.draw.rect(pantalla, (0, 255, 0), guardar_rect)
        texto_guardar = fuente.render("Guardar", True, (0, 0, 0))
        pantalla.blit(texto_guardar, (guardar_rect.x + 10, guardar_rect.y + 10))

        cancelar_rect = pygame.Rect(self.form_rect.x + 270, self.form_rect.y + 250, 100, 40)
        pygame.draw.rect(pantalla, (255, 0, 0), cancelar_rect)
        texto_cancelar = fuente.render("Cancelar", True, (0, 0, 0))
        pantalla.blit(texto_cancelar, (cancelar_rect.x + 10, cancelar_rect.y + 10))

    def esta_listo(self):
        return self.completo

    def fue_cancelado(self):
        return self.cancelado 