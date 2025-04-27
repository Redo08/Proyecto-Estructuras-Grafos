import pygame
import math
import networkx as nx

class DibujadorGrafo:
    def __init__(self, grafo, area_mapa, screen):
        self.grafo = grafo  # El grafo como diccionario de adyacencia
        self.area_mapa = area_mapa  # Rectángulo del área donde se dibuja el grafo
        self.screen = screen  # Superficie de Pygame donde se dibuja
        self.posiciones_nodos = self.calcular_posiciones()  # Calcula posiciones automáticamente
        self.dibujadas = set()  # Para evitar duplicar aristas

    def calcular_posiciones(self):
        """Calcula posiciones automáticas de los nodos usando NetworkX."""
        G = nx.Graph()
        for nodo, vecinos in self.grafo.items():
            for vecino, peso in vecinos.items():
                G.add_edge(nodo, vecino, weight=peso)
                
        # Usar spring_layout para posiciones automáticas
        pos = nx.spring_layout(G, seed=42, scale=1.0)
        
        # Escalar posiciones al área del mapa
        min_x = min(x for x, y in pos.values())
        max_x = max(x for x, y in pos.values())
        min_y = min(y for x, y in pos.values())
        max_y = max(y for x, y in pos.values())
        
        posiciones = {}
        for nodo, (x, y) in pos.items():
            # Normalizar a [0,1]
            x_norm = (x - min_x) / (max_x - min_x) if max_x != min_x else 0.5
            y_norm = (y - min_y) / (max_y - min_y) if max_y != min_y else 0.5
            # Ajustar a las dimensiones del área del mapa con márgenes
            posiciones[nodo] = (
                int(self.area_mapa.x + 20 + x_norm * (self.area_mapa.width - 40)),
                int(self.area_mapa.y + 20 + y_norm * (self.area_mapa.height - 40))
            )
        return posiciones

    def dibujar_nodos(self):
        """Dibuja los nodos como círculos con etiquetas."""
        for nodo, pos in self.posiciones_nodos.items():
            pygame.draw.circle(self.screen, (255, 0, 0), pos, 15)  # Círculo rojo
            texto_nodo = pygame.font.Font(None, 20).render(nodo, True, (255, 255, 255))
            self.screen.blit(texto_nodo, (pos[0] - 10, pos[1] - 10))  # Etiqueta centrada

    def dibujar_arista_con_flecha(self, inicio, fin, peso, color=(0, 0, 0)):
        """Dibuja una arista con flecha y su peso."""
        pygame.draw.line(self.screen, color, inicio, fin, 2)  # Línea de la arista
        # Calcular dirección para la flecha
        dx = fin[0] - inicio[0]
        dy = fin[1] - inicio[1]
        longitud = max(1, math.sqrt(dx * dx + dy * dy))
        dx, dy = dx / longitud, dy / longitud
        # Punto de la flecha ajustado al borde del nodo
        punta = (fin[0] - dx * 15, fin[1] - dy * 15)
        # Dibujar triángulo de la flecha
        pygame.draw.polygon(self.screen, color, [
            punta,
            (punta[0] - dy * 5 + dx * 5, punta[1] + dx * 5 + dy * 5),
            (punta[0] + dy * 5 + dx * 5, punta[1] - dx * 5 + dy * 5)
        ])
        # Peso en el centro
        texto_peso = pygame.font.Font(None, 20).render(str(peso), True, (0, 255, 0))
        medio = ((inicio[0] + fin[0]) // 2, (inicio[1] + fin[1]) // 2)
        self.screen.blit(texto_peso, medio)

    def dibujar_arista_desplazada(self, inicio, fin, peso, desplazamiento=8, color=(0, 0, 0)):
        """Dibuja una arista desplazada para grafos bidireccionales."""
        dx = fin[0] - inicio[0]
        dy = fin[1] - inicio[1]
        longitud = max(1, math.sqrt(dx * dx + dy * dy))
        nx, ny = -dy / longitud, dx / longitud  # Vector normal
        inicio_desplazado = (inicio[0] + nx * desplazamiento, inicio[1] + ny * desplazamiento)
        fin_desplazado = (fin[0] + nx * desplazamiento, fin[1] + ny * desplazamiento)
        self.dibujar_arista_con_flecha(inicio_desplazado, fin_desplazado, peso, color)

    def dibujar_aristas(self):
        """Dibuja las aristas, manejando casos dirigidos y no dirigidos."""
        self.dibujadas.clear()  # Reiniciar aristas dibujadas
        for nodo, vecinos in self.grafo.items():
            for vecino, peso in vecinos.items():
                if (nodo, vecino) in self.dibujadas:
                    continue
                inicio = self.posiciones_nodos[nodo]
                fin = self.posiciones_nodos[vecino]
                vuelta = self.grafo.get(vecino, {}).get(nodo)  # ¿Es bidireccional?
                if vuelta is not None:  # Si hay arista de ida y vuelta
                    self.dibujar_arista_desplazada(inicio, fin, peso, desplazamiento=8)
                    self.dibujar_arista_desplazada(fin, inicio, vuelta, desplazamiento=-8)
                    self.dibujadas.add((nodo, vecino))
                    self.dibujadas.add((vecino, nodo))
                else:  # Arista dirigida o simple
                    self.dibujar_arista_con_flecha(inicio, fin, peso)
                    self.dibujadas.add((nodo, vecino))

    def dibujar(self):
        """Dibuja el grafo completo."""
        self.dibujar_aristas()
        self.dibujar_nodos()
