import pygame
import math
from src.helpers import Helpers
# Definición de colores
COLOR_NODO_INTERES_1 = (26,154,177)    # Rojo (tipo 0)

COLOR_NODO_CONTROL = (254, 182, 20)      # Verde
COLOR_ETIQUETA = (89,48,11)      # Blanco
COLOR_ARISTA = (0, 0, 0)              # Negro
COLOR_PESO = (0, 0, 0)              # Verde
COLOR_RESALTADO = (255, 253, 85)       # Amarillo
COLOR_CAMINO = (0, 255, 0)            # Verde

# Constantes de tamaño
RADIO_NODO_INTERES = 15
RADIO_NODO_CONTROL = 15
RADIO_SELECCION = 15

FPS = 60

class InterfazGrafo:
    def __init__(self, grafo, area_mapa, screen):
        self.screen = screen
        self.grafo = grafo
        self.area_mapa = area_mapa
        self.aristas_resaltadas = []  
        self.nodos_resaltados = []      
        
        
    def seleccionar_nodo(self, event):
        """Selecciona un nodo basado en un clic y retorna su ID o None."""
        #if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.area_mapa.collidepoint(event.pos):
        # Buscar en nodos de interés
        nodo = self.buscar_nodo_en_lista(self.grafo.nodos, event.pos, radio=15, es_control=False)
        if nodo is not None:
            return nodo
        # Buscar en nodos de control
        for arista in self.grafo.aristas:
            nodo = self.buscar_nodo_en_lista(arista.nodos_control, event.pos, radio=15, es_control=True)
            if nodo is not None:
                return nodo
            
        return None
    
    def buscar_nodo_en_lista(self, lista_nodos, pos_clic, radio=15, es_control=False):
        """Busca un nodo en la lista cuyo círculo contenga el punto del clic."""
        for nodo in lista_nodos:
            if nodo and nodo.posicion and math.hypot(nodo.posicion[0] - pos_clic[0], nodo.posicion[1] - pos_clic[1]) <= radio:
                tipo = "control" if es_control else "interés"
                print(f"Nodo de {tipo} seleccionado: {nodo.id}")
                return nodo
        return None
    
     

    def limpiar_resaltado(self):
        """Limpia los resaltados de nodos y aristas."""
        self.aristas_resaltadas = []
        self.nodos_resaltados = []

    def dibujar_nodos_interes(self):
        for nodo in self.grafo.nodos:
            if nodo.posicion:
                
                pygame.draw.circle(self.screen, COLOR_NODO_INTERES_1, nodo.posicion, RADIO_NODO_INTERES)                
                etiqueta = nodo.id 
                texto = pygame.font.Font(None, 20).render(etiqueta, True, COLOR_ETIQUETA)
                self.screen.blit(texto, texto.get_rect(center=nodo.posicion))

    def dibujar_nodos_control(self):
        for arista in self.grafo.aristas:
            for nodo_control in arista.nodos_control:    
                if nodo_control.posicion:
                    pygame.draw.circle(self.screen, COLOR_NODO_CONTROL, nodo_control.posicion, RADIO_NODO_CONTROL)
                    etiqueta = nodo_control.id 
                    texto = pygame.font.Font(None, 20).render(etiqueta, True, COLOR_ETIQUETA)
                    self.screen.blit(texto, texto.get_rect(center=nodo_control.posicion))


    def dibujar_nodos_resaltados(self):
        """Dibuja los nodos resaltados."""
       
        grosor = 3
        for nodo in self.nodos_resaltados:
            pygame.draw.circle(self.screen, COLOR_RESALTADO, nodo.posicion, RADIO_NODO_INTERES + 3, grosor)               
    
    def dibujar_aristas(self):
        """Dibuja las aristas entre los nodos, evitando la superposición de dos aristas."""
        bidireccionales=set()
        for arista in self.grafo.aristas:
            id_origen = arista.origen.id
            id_destino = arista.destino.id
            
            if (id_destino, id_origen) in  [(a.origen.id, a.destino.id) for a in self.grafo.aristas]:
             bidireccionales.add(tuple(sorted((id_origen, id_destino))))
        for arista in self.grafo.aristas:
            inicio = arista.origen.posicion
            fin = arista.destino.posicion
        # Calcular desplazamiento si es bidireccional
            id_origen = arista.origen.id
            id_destino = arista.destino.id
            desplazamiento = (0, 0)  # Desplazamiento inicial
            if tuple(sorted((id_origen, id_destino))) in bidireccionales:
                if id_origen < id_destino:
                    desplazamiento = (-12, -12)  # Desplazar hacia arriba y a la izquierda
                else:
                    desplazamiento = (12, 12)    # Desplazar hacia abajo y a la derecha
                inicio_desplazado = (inicio[0] + desplazamiento[0], inicio[1] + desplazamiento[1])
                fin_desplazado = (fin[0] + desplazamiento[0], fin[1] + desplazamiento[1])
            else:
                inicio_desplazado = inicio
                fin_desplazado = fin
            # Dibujar la arista con flecha y peso
            self.dibujar_arista_con_flecha(inicio_desplazado, fin_desplazado, arista.peso,desplazamiento)
            arista.calcular_posiciones(inicio, fin, desplazamiento)

    def dibujar_aristas_resaltadas(self):
        """Dibuja las aristas resaltadas."""
        for nodo_origen, nodo_destino in self.aristas_resaltadas:
            if Helpers.el_nodo_existe(self.grafo.nodos, nodo_origen.id) and Helpers.el_nodo_existe(self.grafo.nodos, nodo_destino.id):                
                pygame.draw.line(self.screen, COLOR_RESALTADO, nodo_origen.posicion, nodo_destino.posicion, 2)
                

    def dibujar_arista_con_flecha(self, inicio, fin, peso, desplazamiento, color=COLOR_ARISTA):
        #Dibuja la linea
        pygame.draw.line(self.screen, color, inicio, fin, 2)
        #Dibujar la flecha
        
        #Calcular dirección
        dx = fin[0] - inicio[0]
        dy = fin[1] - inicio[1]
        distancia = (dx**2 + dy**2)**0.5  #Formula de distancia euclidiana
        
        #Retroceder un poco el final para que la flecha no tape
        offset = 20
        fin_flecha = (fin[0] - dx / distancia * offset, fin[1] - dy / distancia * offset)
        
        #Dibujar la flecha
        self.dibujar_flecha(fin_flecha, inicio, color)

        # Dibujar el peso
        texto_peso = pygame.font.Font(None, 20).render(str(peso), True, COLOR_PESO)
        t = 0.5
        pos_base = (inicio[0] + t * (fin[0] - inicio[0]), inicio[1] + t * (fin[1] - inicio[1]))
        # Calcular vector perpendicular
        dx_norm = dx / distancia
        dy_norm = dy / distancia
        # Vector perpendicular (rotar 90 grados): (-dy, dx) o (dy, -dx)
        # Usamos la dirección que coincide con el desplazamiento de la arista
        if desplazamiento[0]  <= 0 and desplazamiento[1]  <= 0:  # Arriba/izquierda
            perp_dx, perp_dy = -dy_norm, dx_norm
        elif desplazamiento[0]  > 0 and desplazamiento[1]  > 0:  # Abajo/derecha
            perp_dx, perp_dy = dy_norm, -dx_norm
        else:  # Unidireccional, usamos (-dy, dx) por defecto
            perp_dx, perp_dy = -dy_norm, dx_norm
        # Desplazar un poco más de la mitad del radio del nodo de control
        distancia_perp = RADIO_NODO_CONTROL + 5  # 23 con radio de 18
        pos_peso = (pos_base[0] + perp_dx * distancia_perp, pos_base[1] + perp_dy * distancia_perp)
        self.screen.blit(texto_peso, texto_peso.get_rect(center=pos_peso))


        
    def dibujar_flecha(self, fin, inicio, color=COLOR_ARISTA):
        dx = fin[0] - inicio[0]
        dy = fin[1] - inicio[1]
        angulo = math.atan2(dy, dx)
        largo = 10
        ancho = 5
        # Puntos del triángulo
        punto1 = (fin[0], fin[1])
        punto2 = (fin[0] - largo * math.cos(angulo - math.pi/6), fin[1] - largo * math.sin(angulo - math.pi/6))
        punto3 = (fin[0] - largo * math.cos(angulo + math.pi/6), fin[1] - largo * math.sin(angulo + math.pi/6))
        pygame.draw.polygon(self.screen, color, [punto1, punto2, punto3])        
        
    def mostrar_camino(self, camino):
        self.limpiar_resaltado()
        
        for i in range(len(camino[0])-1):
            origen = camino[0][i]
            destino = camino[0][i + 1]
            
            nodo_origen = Helpers.hallar_nodo(self.grafo.nodos, origen)
            nodo_destino = Helpers.hallar_nodo(self.grafo.nodos, destino)
            self.aristas_resaltadas.append((nodo_origen, nodo_destino))
            
            self.nodos_resaltados.append(nodo_origen)
            self.nodos_resaltados.append(nodo_destino)
            
        if camino:
            ultimo = camino[0][-1]
            ultimo_nodo = Helpers.hallar_nodo(self.grafo.nodos, ultimo)
            self.nodos_resaltados.append(ultimo_nodo)
    
    def mostrar_caminos(self, caminos):
        self.limpiar_resaltado()
        
        for destino, (costo, camino) in caminos.items():
            for i in range(len(camino) - 1):
                origen = camino[i]
                siguiente = camino[i + 1]
                nodo_origen = Helpers.hallar_nodo(self.grafo.nodos, origen)
                nodo_siguiente = Helpers.hallar_nodo(self.grafo.nodos, siguiente)
                self.aristas_resaltadas.append((nodo_origen, nodo_siguiente))
                self.nodos_resaltados.append(nodo_origen)
                
            # Resaltar el ultimo nodo del camino
            if camino:
                nodo_ultimo = Helpers.hallar_nodo(self.grafo.nodos, camino[-1])
                self.nodos_resaltados.append(nodo_ultimo)
        
    def dibujar(self):
        """Dibuja el grafo completo."""
        #self.dibujar_aristas()
        self.dibujar_aristas()
        self.dibujar_aristas_resaltadas()
        self.dibujar_nodos_interes()
        self.dibujar_nodos_resaltados()
        
        self.dibujar_nodos_control()
        

    
    