import pygame
from src.models.grafo import Grafo
from src.models.recorridos import Recorridos
from src.helpers import Helpers
from views.interfazGrafo import InterfazGrafo
from views.boton import Boton
from views.InterfazNodo import InterfazNodo
from views.interfazUsuario import InterfazUsuario
from views.InterfazArista import InterfazArista
from views.interfazRecorridos import InterfazRecorridos
AZUL=(1,46,67)

class Visualizador:
    def __init__(self, grafo, ancho, alto):
        self.grafo = grafo
        self.ancho = ancho
        self.alto = alto
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Visualizador de Grafos")
        self.clock = pygame.time.Clock()
        
        #Configuración Areas
        self.altura_titulo = 50
        self.area_titulo = pygame.Rect(0, 0, ancho, self.altura_titulo)  # Área del título
        margen = 10 
        self.area_mapa = pygame.Rect(margen, self.altura_titulo+margen, ancho * 0.60 -2 * margen, alto-self.altura_titulo-2 * margen)  # 75% del ancho para el mapa
        self.area_control = pygame.Rect(ancho * 0.60, 0, ancho * 0.4, alto)  # 25% para controles
        self.area_info = pygame.Rect(self.area_control.x + 20, self.area_control.y + 280, self.area_control.width - 30, 350)
        #Grafo
        self.interfaz_grafo = InterfazGrafo(self.grafo, self.area_mapa, self.screen)
        
        #Usuario
        self.usuario = None #Aqui se guarda el objeot Uusario
        
        #Botones
        self.botones = [

            Boton(pygame.Rect(self.area_control.x + 380, 50, 150, 40), "New nodo control", self.iniciar_agregar_nodo_control, self.screen,AZUL),
            Boton(pygame.Rect(self.area_control.x + 20, 50, 150, 40), "Cargar mapa", self.cargar_mapa, self.screen,AZUL),
            Boton(pygame.Rect(self.area_control.x + 200, 50, 150, 40), "Guardar mapa", self.guardar_mapa, self.screen,AZUL),
            Boton(pygame.Rect(self.area_control.x + 20, 110, 150, 40), "New nodo", self.iniciar_agregar_nodo, self.screen,AZUL),
            Boton(pygame.Rect(self.area_control.x + 200, 110, 150, 40), "Eliminar nodo", self.iniciar_eliminar_nodo, self.screen,AZUL),
            Boton(pygame.Rect(self.area_control.x + 380, 110, 150, 40), "Crear usuario", self.iniciar_crear_usuario, self.screen,AZUL),
            Boton(pygame.Rect(self.area_control.x + 20, 170, 150, 40), "Agregar arista", self.iniciar_agregar_arista, self.screen,AZUL),
            Boton(pygame.Rect(self.area_control.x + 200, 170, 150, 40), "Eliminar arista", self.iniciar_eliminar_arista, self.screen,AZUL),
            Boton(pygame.Rect(self.area_control.x + 380, 170, 150, 40), "Recorridos", self.iniciar_recorridos, self.screen,AZUL),
        ]
        
       
        #Estado
        self.modo_actual = None  # Modo actual (puede ser "nuevo_nodo" o "eliminar_nodo" o "Recorridos")      
        self.running = True

    def dibujar(self):
        """Dibuja el grafo y la interfaz en la pantalla"""
        # Colores
        NEGRO = (0, 0, 0)
        BLANCO = (255, 255, 255)
        ROJO = (255, 0, 0)
        GRIS = (234, 235, 237)
        VERDE = (0, 255, 0)
        
    
        # Fondo
        self.screen.fill(BLANCO)
    
        # Titulo
        font = pygame.font.Font(None, 36)
        texto_mapa = font.render("RUTAS POR LA CIUDAD", True, AZUL)
        ancho_texto = texto_mapa.get_width()
        pos_x = (self.ancho * 0.6 / 2) - (ancho_texto / 2)
        pos_y = (self.altura_titulo / 2) - (texto_mapa.get_height() / 2)
        self.screen.blit(texto_mapa, (pos_x, pos_y))
        
        # Dibujar áreas
        pygame.draw.rect(self.screen, NEGRO, self.area_mapa, 2)
        pygame.draw.rect(self.screen, BLANCO, self.area_control)
        pygame.draw.rect(self.screen, GRIS, self.area_info)
        
        # Dibujar grafo
        self.interfaz_grafo.dibujar()
        
        #Dibujar botones
        for boton in self.botones:
            boton.dibujar()
            
        # Dibujar formulario
        if self.modo_actual:
            self.modo_actual.dibujar()
        
        #Dibujar usuario
        if self.usuario:
            font = pygame.font.Font(None, 32)
            mensaje = f"Bienvenido, {self.usuario.nombre}"
            texto = font.render(mensaje, True, (0, 0, 0))  # Verde oscuro
            x = self.area_control.x + 25
            y = self.area_control.y + 240
            self.screen.blit(texto, (x, y))
            
    def cargar_mapa(self):
        datos = Helpers.cargar_texto()
        grafo = Grafo()
        
        grafo.cargar_json(datos)
        
        if grafo:
            self.grafo = grafo
            self.interfaz_grafo = InterfazGrafo(grafo, self.area_mapa, self.screen)
            
    def guardar_mapa(self):
        data = self.grafo.guardar_json()
        if data:
            Helpers.guardar_texto(data)
            print("Si se guardo bien")
  
    def iniciar_agregar_nodo(self): 
        def on_finish():
            self.modo_actual = None
        self.modo_actual = InterfazNodo(self.screen, self.area_mapa, self.grafo, self.interfaz_grafo, on_finish, modo="agregar")

    def iniciar_eliminar_nodo(self):
        def on_finish():
            self.modo_actual = None
        self.modo_actual = InterfazNodo(self.screen, self.area_mapa, self.grafo, self.interfaz_grafo, on_finish, modo="eliminar")

    def iniciar_agregar_arista(self):
        def on_finish():
            self.modo_actual = None
        self.modo_actual = InterfazArista(self.screen, self.area_mapa, self.grafo, self.interfaz_grafo, on_finish, modo="agregar_arista")

    def iniciar_eliminar_arista(self):
        def on_finish():
            self.modo_actual = None
        self.modo_actual = InterfazArista(self.screen, self.area_mapa, self.grafo, self.interfaz_grafo, on_finish, modo="eliminar_arista")

    def iniciar_agregar_nodo_control(self):
        def on_finish():
            self.modo_actual = None
        self.modo_actual = InterfazArista(self.screen, self.area_mapa, self.grafo, self.interfaz_grafo, on_finish, modo="agregar_nodo_control")
    

    def iniciar_crear_usuario(self):
        def on_finish(usuario_creado):
            self.usuario = usuario_creado
            self.modo_actual = None
        self.modo_actual = InterfazUsuario(self.screen, self.area_mapa, on_finish)
    
    def iniciar_recorridos(self):
        if not self.usuario:
            # Mandar a crear usuario
            def on_finish(usuario_creado):
                self.usuario = usuario_creado
                self.modo_actual = None
                # Se vuelve a mandar a los recorridos
                self.iniciar_recorridos()
            self.modo_actual = InterfazUsuario(self.screen, self.area_mapa, on_finish)
        else:
            def on_finish():
                self.modo_actual = None
            self.modo_actual = InterfazRecorridos(self.screen, self.area_mapa, self.grafo, self.interfaz_grafo, self.usuario, self.area_info, on_finish)
        
    def manejar_eventos(self):
        """Maneja los eventos de Pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            #Verificar botones
            for boton in self.botones:
                boton.manejar_evento(event)

            if self.modo_actual:
                self.modo_actual.manejar_evento(event)               
                        
                    
    def ejecutar(self):
        """Ejecuta el bucle principal del juego"""
        while self.running:
            self.manejar_eventos()  # Manejar eventos
            self.dibujar()  # Dibujar
            pygame.display.flip()  # Actualizar pantalla
            self.clock.tick(60)  # 60 FPS
        pygame.quit()