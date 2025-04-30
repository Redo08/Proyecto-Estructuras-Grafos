import pygame

# Clase para el formulario del nodo
class FormularioNodo:
    def __init__(self):
        self.campos = {"id": "", "tipo": "", "nombre": "", "descripcion": ""}
        self.orden_campos = ["id", "tipo", "nombre", "descripcion"]
        self.indice_campo_actual = 0
        self.completo = False
        self.form_rect = None

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            campo_actual = self.orden_campos[self.indice_campo_actual]
            if evento.key == pygame.K_RETURN:
                if self.indice_campo_actual < len(self.orden_campos) - 1:
                    self.indice_campo_actual += 1
            elif evento.key == pygame.K_BACKSPACE:
                self.campos[campo_actual] = self.campos[campo_actual][:-1]
            else:
                self.campos[campo_actual] += evento.unicode
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Botón "Guardar"
            guardar_rect = pygame.Rect(self.form_rect.x + 150, self.form_rect.y + 250, 100, 40)
            if guardar_rect.collidepoint(evento.pos):
                self.completo = True

    def dibujar(self, pantalla, fuente, area_mapa):
        # Rectángulo de fondo del formulario
        self.form_rect = pygame.Rect(area_mapa.x + 100, area_mapa.y + 100, 400, 300)
        pygame.draw.rect(pantalla, (200, 200, 200), self.form_rect)

        # Dibujar campos
        x, y = self.form_rect.x + 20, self.form_rect.y + 20
        for i, campo in enumerate(self.orden_campos):
            if i < self.indice_campo_actual:
                texto = f"{campo}: {self.campos[campo]}"
            elif i == self.indice_campo_actual:
                texto = f"{campo}: {self.campos[campo]}_"
            else:
                texto = f"{campo}: "
            superficie = fuente.render(texto, True, (0, 0, 0))
            pantalla.blit(superficie, (x, y + i * 30))

        # Botón "Guardar"
        guardar_rect = pygame.Rect(self.form_rect.x + 150, self.form_rect.y + 250, 100, 40)
        pygame.draw.rect(pantalla, (0, 255, 0), guardar_rect)
        texto_guardar = fuente.render("Guardar", True, (0, 0, 0))
        pantalla.blit(texto_guardar, (guardar_rect.x + 10, guardar_rect.y + 10))

    def esta_listo(self):
        return self.completo

