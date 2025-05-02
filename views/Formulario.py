import pygame
from views.boton import Boton

class Formulario:
    def __init__(self, screen, campos_iniciales=None, condiciones=None, area_mapa=None, mensaje_confirmacion=None, accion="agregar"):
        self.screen = screen
        self.area_mapa = area_mapa
        self.campos = {campo: "" for campo in (campos_iniciales or [])}  # Manejar None
        self.orden_campos = list(campos_iniciales or [])  # Manejar None
        self.condiciones = condiciones or {}
        self.indice_campo_actual = 0 if campos_iniciales else -1  # -1 para eliminación
        self.completo = False
        self.cancelado = False
        self.accion = accion  # "agregar", "eliminar" o "error"
        self.mensaje_confirmacion = mensaje_confirmacion
        self.form_rect = pygame.Rect(area_mapa.x + 100, area_mapa.y + 100, 400, 300)
        # Botones
        boton_confirmar_texto = "Guardar" if accion == "agregar" else "Sí"
        self.botones = [
            Boton(
                pygame.Rect(self.form_rect.x + 150, self.form_rect.y + 250, 100, 40),
                boton_confirmar_texto,
                self.marcar_completo,
                self.screen,
                color_fondo=(0, 255, 0)
            ),
            Boton(
                pygame.Rect(self.form_rect.x + 270, self.form_rect.y + 250, 100, 40),
                "Cancelar",
                self.marcar_cancelado,
                self.screen,
                color_fondo=(255, 0, 0)
            )
        ]

    def manejar_evento(self, evento):
        if self.accion == "agregar" and self.indice_campo_actual >= 0:
            campo_actual = self.orden_campos[self.indice_campo_actual]
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if self.campos[campo_actual]:
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
                    char = evento.unicode
                    if char.isprintable():
                        self.campos[campo_actual] += char
        # Manejar botones
        for boton in self.botones:
            boton.manejar_evento(evento)

    def dibujar(self):
        pygame.draw.rect(self.screen, (200, 200, 200), self.form_rect)
        fuente = pygame.font.Font(None, 30)
        if self.accion == "agregar":
            instruccion = "Ingrese los datos solicitados"
            superficie_inst = fuente.render(instruccion, True, (0, 0, 0))
            self.screen.blit(superficie_inst, (self.form_rect.x + 20, self.form_rect.y + 20))
            x, y = self.form_rect.x + 20, self.form_rect.y + 60
            for i, campo in enumerate(self.orden_campos):
                if i < self.indice_campo_actual:
                    texto = f"{campo}: {self.campos[campo]}"
                elif i == self.indice_campo_actual:
                    texto = f"{campo}: {self.campos[campo]}_"
                else:
                    texto = f"{campo}: "
                superficie = fuente.render(texto, True, (0, 0, 0))
                self.screen.blit(superficie, (x, y + i * 30))
        elif self.accion == "eliminar" or self.accion == "error":
            mensaje = self.mensaje_confirmacion or "¿Está seguro de eliminar este nodo?"
            superficie_mensaje = fuente.render(mensaje, True, (0, 0, 0))
            self.screen.blit(superficie_mensaje, (self.form_rect.x + 20, self.form_rect.y + 20))
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