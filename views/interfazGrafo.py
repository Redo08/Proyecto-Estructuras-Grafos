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
        for id_nodo, nodo in self.grafo.nodos.items():
            print(id_nodo, f"nodo:  {nodo}")
            for id_destino, arista in nodo.vecinos.items():
                print(id_destino, f"arista: {arista}")
                G.add_edge(nodo.id, id_destino, weight=arista.peso)

        #Algoritmo que simula conexión entre nodos, el seed=42 asegura que siempre este igual, y ahi también se pone la escala el tamaño
        pos = nx.spring_layout(G, seed=42, scale=1.0)
        print("POS:", pos)
        #Escalar y centrar
        min_x = min(x for x, y in pos.values()) 
        max_x = max(x for x, y in pos.values())
        min_y = min(y for x, y in pos.values())
        max_y = max(y for x, y in pos.values())

        posiciones = {}
        for id_nodo, nodo in self.grafo.nodos.items():
            if nodo.posicion:  # Usar posición definida si existe
                posiciones[id_nodo] = nodo.posicion
            else:  # Calcular posición automática
                x, y = pos[id_nodo]
                x_norm = (x - min_x) / (max_x - min_x) if max_x != min_x else 0.5
                y_norm = (y - min_y) / (max_y - min_y) if max_y != min_y else 0.5
                posiciones[id_nodo] = (
                    int(self.area_mapa.x + 20 + x_norm * (self.area_mapa.width - 40)),
                    int(self.area_mapa.y + 20 + y_norm * (self.area_mapa.height - 40))
                )

        return posiciones

    def dibujar_nodos(self):
        for nodo_id, pos in self.posiciones_nodos.items():
            # Obtener el objeto Nodo
            nodo = self.grafo.nodos[nodo_id]

            #Crear circulo
            pygame.draw.circle(self.screen, (255, 0, 0), pos, 15)
            
            # Determinar la etiqueta
            if nodo.tipo == 0 and nodo.nombre:  # Punto de Interés con nombre
                etiqueta = nodo.nombre[:2] if len(nodo.nombre) >= 2 else nodo.nombre
            elif nodo.tipo == 1:  # Punto de Control con riesgo
                if nodo.riesgo is not None:
                    # Usar el valor de riesgo como etiqueta
                    etiqueta = str(nodo.riesgo)
                else:
                    etiqueta = "CP"  # Valor predeterminado si riesgo es None
            else:
                etiqueta = "CP"  # Valor predeterminado para nodos sin nombre o riesgo
            #Crear el texto del nodo
            texto_nodo = pygame.font.Font(None, 20).render(etiqueta, True, (255, 255, 255))
            
            #Posicionar en el centro del nodo
            texto_rect = texto_nodo.get_rect(center=pos)
            
            #Poner el texto en el centro del nodo
            self.screen.blit(texto_nodo, texto_rect)
    
    
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
                    dibujadas.add((nodo.id, id_destino))
                    
                
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
        
        
    def dibujar(self):
        """Dibuja el grafo completo."""
        self.dibujar_aristas()
        self.dibujar_nodos()
    
    def obtener_nodo_seleccionado(self, mouse_pos):
        for nodo_id, pos in self.posiciones_nodos.items():
            distancia = math.hypot(pos[0] - mouse_pos[0], pos[1] - mouse_pos[1])
            if distancia <= 15:
                return nodo_id
        return None