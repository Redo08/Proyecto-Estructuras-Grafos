import pygame

class FormularioNodo:
    def __init__(self):
        self.campos = {
            'tipo': '' #Primer campo
        }
        self.orden_campos = ['tipo'] # Orden que se mostraran los campos
        self.indice_campo_actual = 0
        self.completo = False #Indica si ya se lleno todos los datos del formulario
        self.terminado = False #Indica si ya se hizo el click y listo para finalizar
        self.tipo = None # 0-> Punto de interes, 1-> Punto de control
        self.posicion = None # (x,y) se asignara depsues del click
        self.estado = 'formulario' # 'formulario' -> Llenando formulario, 'esperando_click' -> Esperando click
        
    def manejar_evento(self, evento):
        #Si estamos llenando el formulario:
        if self.estado == 'formulario':
            if evento.type == pygame.KEYDOWN: #Si se preciona la tecla
                campo_actual = self.orden_campos[self.indice_campo_actual]
                
                # Si es una tecla de letra/número
                if evento.key == pygame.K_BACKSPACE: 
                    self.campos[campo_actual] = self.campos[campo_actual][:-1] #Borra el ultimo caracter al presionar eliminar
                
                elif evento.key == pygame.K_RETURN: #Si da enter:
                    if campo_actual == 'tipo':
                        tipo_ingresado = self.campos['tipo']
                        if tipo_ingresado == '0': # Punto de interes
                            self.tipo = 0
                            self.campos.update({
                                'id': '',
                                'nombre': '',
                                'descripcion': ''
                            })
                        elif tipo_ingresado == '1': #Punto de control
                            self.tipo = 1
                            self.campos.update({
                                'id': '',
                                'riesgo': '',
                                'accidentalidad': '',
                                'popularidad': '',
                                'dificultad': ''
                            })
                        else: #Valor invalido
                            print("Valor invalido")
                            return
                        
                        # Actualizamos el orden de campos para reflejar los nuevos
                        self.orden_campos = list(self.campos.keys())
                        
                    self.indice_campo_actual += 1
                    
                    
                    if self.indice_campo_actual >= len(self.orden_campos):
                        self.estado = 'esperando_click'
                        self.completo = True
                else:
                    #Agregar normal el caracter
                    self.campos[campo_actual] += evento.unicode
                    
        #Si ya se lleno el formulario
        elif self.estado == 'esperando_click':
            if evento.type == pygame.MOUSEBUTTONDOWN:
                self.posicion = evento.pos
                self.campos.update({
                    'posicion': self.posicion
                })
                self.terminado = True
                
    def dibujar(self, pantalla, fuente, area_mapa):
        x = area_mapa.x + 50
        y = area_mapa.y + 200
        
        if self.estado == 'formulario':
            campo_actual = self.orden_campos[self.indice_campo_actual]
            
            for i, campo in enumerate(self.orden_campos):
                valor = self.campos[campo] if i < self.indice_campo_actual else ''
                texto = f"{campo}: {valor}"
                superficie = fuente.render(texto, True, (0,0,0))
                pantalla.blit(superficie, (x, y + i * 30))      
            
            texto_ingreso = fuente.render(f"{campo_actual}: {self.campos[campo_actual]}", True, (0,0,255))
            pantalla.blit(texto_ingreso, (x, y + len(self.orden_campos) * 30))
        
        elif self.estado == 'esperando_click':
            texto = fuente.render("Haz click donde quieras colocar el nodo", True, (255, 0, 0))
            pantalla.blit(texto, (x,y))
            
    
    def esta_listo(self):
        return self.terminado