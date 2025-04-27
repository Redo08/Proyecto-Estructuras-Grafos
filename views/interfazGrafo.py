import pygame
import math
import networkx as nx

class InterfazGrafo:
    def __init__(self, grafo, area_mapa, screen):
        self.screen = screen
        self.grafo = grafo
        self.area_mapa = area_mapa
        self.posiciones_nodos = self.calcular_posiciones() 
        
    
    def calcular_posiciones(self):
        """Calcula posiciones automaticas de los nodos"""
        G = nx.Graph()
        for nodo, vecinos in self.grafo.items():
            print(nodo, vecinos)
            for vecino, peso in vecinos.items():
                print(vecino, peso)
                G.add_edge(nodo, vecino, weight=peso)

        #Algoritmo que simula conexión entre nodos, el seed=42 asegura que siempre este igual, y ahi también se pone la escala el tamaño
        pos = nx.spring_layout(G, seed=42, scale=1.0)

        #Escalar y centrar
        min_x = min(x for x, y in pos.values()) 
        max_x = max(x for x, y in pos.values())
        min_y = min(y for x, y in pos.values())
        max_y = max(y for x, y in pos.values())

        posiciones = {}
        for nodo, (x, y) in pos.items():
            # Normalizar a [0,1]
            x_norm = (x - min_x) / (max_x - min_x) if max_x != min_x else 0.5
            y_norm = (y - min_y) / (max_y - min_y) if max_y != min_y else 0.5
            posiciones[nodo] = (
                int(self.area_mapa.x + 20 + x_norm * (self.area_mapa.width - 40)),
                int(self.area_mapa.y + 20 + y_norm * (self.area_mapa.height - 40))
            ) 

        return posiciones

    def dibujar_nodos(self):
        for nodo, pos in self.posiciones_nodos.items():
            pygame.draw.circle(self.screen, (255, 0, 0), pos, 15)
            texto_nodo = pygame.font.Font(None, 20).render(nodo, True, (255, 255, 255))
            self.screen.blit(texto_nodo, (pos[0] - 10, pos[1] - 10))
    
    def dibujar_aristas(self):
        dibujadas = set() #Para evitar repetidas

        for nodo, vecinos in self.grafo.items():
            for vecino, peso in vecinos.items():
                if (nodo, vecino) in dibujadas:
                    continue # Ya esta
                inicio = self.posiciones_nodos[nodo]
                fin = self.posiciones_nodos[vecino]

                #Si existe doble conexión
                vuelta = self.grafo.get(vecino, {}).get(nodo)

                if vuelta is not None:
                    #Se desplazan las 2 
                    self.dibujar_arista_desplazada(inicio, fin, peso, desplazamiento=8)
                    self.dibujar_arista_desplazada(fin, inicio, vuelta, desplazamiento=-8)
                    dibujadas.add((nodo, vecino))
                    dibujadas.add((vecino, nodo))
                else:
                    #Solo una dirección
                    self.dibujar_arista_con_flecha(inicio, fin, peso)
                    dibujadas.add((nodo, vecino))
                    
    def dibujar_arista_con_flecha(self, inicio, fin, peso, color=(0,0,0)):
        pygame.draw.line(self.screen, color, inicio, fin, 2)
        self.dibujar_flecha(fin, inicio, color)

        # Dibujar el peso
        texto_peso = pygame.font.Font(None, 20).render(str(peso), True, (0, 255, 0))
        medio = ((inicio[0] + fin[0]) // 2, (inicio[1] + fin[1]) // 2)
        self.screen.blit(texto_peso, medio)
        

    def dibujar_arista_desplazada(self, inicio, fin, peso, desplazamiento=8, color=(0,0,0)):
        dx = fin[0] - inicio[0]
        dy = fin[1] - inicio[1]
        normal = (dy, dx)
        norma = (normal[0]**2 + normal[1]**2)**0.5
        if norma != 0:
            normal_unitario = (normal[0]/norma, normal[1]/norma)
        else:
            normal_unitario = (0, 0)

        inicio_desplazado = (
            inicio[0] + normal_unitario[0]*desplazamiento,
            inicio[1] + normal_unitario[1]*desplazamiento
        )
        fin_desplazado = (
            fin[0] + normal_unitario[0]*desplazamiento,
            fin[1] + normal_unitario[1]*desplazamiento
        )

        pygame.draw.line(self.screen, color, inicio_desplazado, fin_desplazado, 2)
        self.dibujar_flecha(fin_desplazado, inicio_desplazado, color)

        # Dibujar el peso
        texto_peso = pygame.font.Font(None, 20).render(str(peso), True, (0, 255, 0))
        medio = ((inicio_desplazado[0] + fin_desplazado[0]) // 2, (inicio_desplazado[1] + fin_desplazado[1]) // 2)
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
        