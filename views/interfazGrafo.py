import pygame
import math
import networkx as nx

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
    
    
    
    def resaltar_arista(self, id_origen, id_destino, color=(255,255,0), grosor=4):
        if id_origen in self.posiciones_nodos and id_destino in self.posiciones_nodos:
            # Evitar duplicados
            self.aristas_resaltadas = [arista for arista in self.aristas_resaltadas
                                      if not (arista[0] == id_origen and arista[1] == id_destino)]
            self.aristas_resaltadas.append((id_origen, id_destino, color, grosor))
        else:
            print(f"No se puede resaltar arista: Posiciones no disponibles para {id_origen}, {id_destino}")   

    def limpiar_resaltado(self):
        """Limpia los resaltados de nodos y aristas."""
        self.aristas_resaltadas = []
        self.nodos_resaltados = []

    def dibujar_nodos_interes(self):
        for nodo in self.grafo.nodos:
            if nodo.posicion:
                color = (255, 0, 0) if nodo.tipo == 0 else (0, 0, 255)
                pygame.draw.circle(self.screen, color, nodo.posicion, 15)                
                etiqueta = nodo.id 
                texto = pygame.font.Font(None, 20).render(etiqueta, True, (255, 255, 255))
                self.screen.blit(texto, texto.get_rect(center=nodo.posicion))

    def dibujar_nodos_control(self):
        for arista in self.grafo.aristas:
            for nodo_control in arista.nodos_control:
                if nodo_control.posicion:
                    pygame.draw.circle(self.screen, (0, 255, 0), nodo_control.posicion, 10)
                    etiqueta = nodo_control.id 
                    texto = pygame.font.Font(None, 20).render(etiqueta, True, (255, 255, 255))
                    self.screen.blit(texto, texto.get_rect(center=nodo_control.posicion))


    def dibujar_nodos_resaltados(self):
        """Dibuja los nodos resaltados."""
        color = (255, 255, 0)  # Color amarillo
        grosor = 4
        for nodo in self.nodos_resaltados:
            pygame.draw.circle(self.screen, color, nodo.posicion, 18, grosor)               
    
    def dibujar_aristas(self):
        """Dibuja las aristas entre los nodos, evitando la superposición de dos aristas."""
        dibujadas = set() #Para evitar repetidas

        for id_nodo, nodo in self.grafo.nodos.items():
            for id_destino, arista in nodo.vecinos.items():
                if (id_nodo, id_destino) in dibujadas:
                    continue # Ya esta
                
                inicio = self.posiciones_nodos[id_nodo]
                fin = self.posiciones_nodos[id_destino]

                #Si existe doble conexión
                nodo_destino = self.grafo.nodos.get(id_destino)
                if nodo_destino:
                    #Verificar si el nodo destino tiene una arista que apunta al nodo actual
                    vuelta = nodo_destino.vecinos.get(nodo.id)

                if vuelta is not None:
                    self.dibujar_arista_con_flecha((inicio[0] - 12, inicio[1] - 12), (fin[0] - 12, fin[1] - 12), arista.peso)  # Superior y a la izquierda
                    self.dibujar_arista_con_flecha((fin[0] + 12, fin[1] + 12),(inicio[0] + 12, inicio[1] + 12), vuelta.peso)  # Inferior y a la derecha
                        
                    dibujadas.add((nodo.id, id_destino))
                    dibujadas.add((id_destino, nodo.id))
                else:
                    #Solo una dirección
                    self.dibujar_arista_con_flecha(inicio, fin, arista.peso)
                    dibujadas.add((nodo.id,id_destino))

    def dibujar_aristas_resaltadas(self):
        """Dibuja las aristas resaltadas."""
        for id_origen, id_destino, color, grosor in self.aristas_resaltadas:
            if id_origen in self.posiciones_nodos and id_destino in self.posiciones_nodos:
                pygame.draw.line(self.screen, color, self.posiciones_nodos[id_origen], self.posiciones_nodos[id_destino], grosor)
                

    def dibujar_arista_con_flecha(self, inicio, fin, peso, color=(0,0,0)):
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
        texto_peso = pygame.font.Font(None, 20).render(str(peso), True, (0, 255, 0))
        medio = ((inicio[0] + fin[0]) // 2, (inicio[1] + fin[1]) // 2)
        self.screen.blit(texto_peso, medio)

        
    def dibujar_flecha(self, fin, inicio, color=(0,0,0)):
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
            self.resaltar_arista(origen, destino, color=(0,255,0), grosor=4)
            self.resaltar_nodo(origen, color=(0,255,0), grosor=4)
            
        if camino:
            self.resaltar_nodo(camino[0][-1], color=(0,255,0), grosor=4)
    
    def mostrar_caminos(self, caminos):
        self.limpiar_resaltado()
        
        for destino, (costo, camino) in caminos.items():
            for i in range(len(camino) - 1):
                origen = camino[i]
                siguiente = camino[i + 1]
                self.resaltar_arista(origen, siguiente, color=(0,255,0), grosor=3)
                self.resaltar_nodo(origen, color=(0,255,0), grosor=3)
                
            # Resaltar el ultimo nodo del camino
            if camino:
                self.resaltar_nodo(camino[-1], color=(0,255,0), grosor=3)
        
    def dibujar(self):
        """Dibuja el grafo completo."""
        #self.dibujar_aristas()
        self.dibujar_nodos_interes()
        self.dibujar_nodos_resaltados()
        self.dibujar_nodos_control()
        #self.dibujar_aristas_resaltadas()
        #self.dibujar_nodos_resaltados()
    
    