import pygame
import math
import networkx as nx

class InterfazGrafo:
    def __init__(self, grafo, area_mapa, screen):
        self.screen = screen
        self.grafo = grafo
        self.area_mapa = area_mapa
        self.posiciones_nodos = self.calcular_posiciones() 
        self.aristas_resaltadas = []  # Lista de (id_origen, id_destino, color, grosor)
        self.nodos_resaltados = []  # Lista de (id_nodo, color, grosor)        
        
        
    def calcular_posiciones(self):
        return {id_nodo: nodo.posicion for id_nodo, nodo in self.grafo.nodos.items() if nodo.posicion}

    def seleccionar_nodo(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.area_mapa.collidepoint(event.pos):
            for nodo_id, pos in self.posiciones_nodos.items():
                if math.hypot(pos[0] - event.pos[0], pos[1] - event.pos[1]) <= 15:
                    print(f"Nodo seleccionado: {nodo_id}")
                    return nodo_id    
        return None
    
    def resaltar_nodo(self, id_nodo, color=(0, 255, 0), grosor=2):
        """Añade un nodo a la lista de resaltados."""
        if id_nodo in self.posiciones_nodos:
            # Evitar duplicados
            self.nodos_resaltados = [nodo for nodo in self.nodos_resaltados
                                    if nodo[0] != id_nodo]
            self.nodos_resaltados.append((id_nodo, color, grosor))
        else:
            print(f"No se puede resaltar nodo: Posición no disponible para {id_nodo}")
    
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

    def dibujar_nodos(self):
        for nodo_id, pos in self.posiciones_nodos.items():
            nodo = self.grafo.nodos[nodo_id]
            pygame.draw.circle(self.screen, (255, 0, 0), pos, 15)
            
            etiqueta = nodo.id if nodo.tipo == 0 and nodo.id else str(nodo_id) if nodo.tipo == 1 else "CP"
            texto = pygame.font.Font(None, 20).render(etiqueta, True, (255, 255, 255))
            self.screen.blit(texto, texto.get_rect(center=pos))

    def dibujar_nodos_resaltados(self):
        """Dibuja los nodos resaltados."""
        for id_nodo, color, grosor in self.nodos_resaltados:
            if id_nodo in self.posiciones_nodos:
                pygame.draw.circle(self.screen, color, self.posiciones_nodos[id_nodo], 18, grosor)               
    
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
    
    def dibujar(self):
        """Dibuja el grafo completo."""
        self.dibujar_aristas()
        self.dibujar_nodos()
        self.dibujar_aristas_resaltadas()
        self.dibujar_nodos_resaltados()
    
    def obtener_nodo_seleccionado(self, mouse_pos):
        for nodo_id, pos in self.posiciones_nodos.items():
            distancia = math.hypot(pos[0] - mouse_pos[0], pos[1] - mouse_pos[1])
            if distancia <= 15:
                return nodo_id
        return None