import pygame
from src.models.grafo import Grafo
from src.models.recorridos import Recorridos
from src.helpers import Helpers
from views.interfazGrafo import InterfazGrafo
from views.boton import Boton
from views.InterfazNodo import InterfazNodo
from views.interfazUsuario import InterfazUsuario
from views.InterfazArista import InterfazArista

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
        
        #Grafo
        self.interfaz_grafo = InterfazGrafo(self.grafo, self.area_mapa, self.screen)
        
        #Usuario
        self.usuario = None #Aqui se guarda el objeot Uusario
        
        #Botones
        self.botones = [
            Boton(pygame.Rect(self.area_control.x + 20, 50, 150, 40), "Cargar mapa", self.cargar_mapa, self.screen),
            Boton(pygame.Rect(self.area_control.x + 200, 50, 150, 40), "Guardar mapa", self.guardar_mapa, self.screen),
            Boton(pygame.Rect(self.area_control.x + 20, 110, 150, 40), "Nuevo nodo", self.iniciar_agregar_nodo, self.screen),
            Boton(pygame.Rect(self.area_control.x + 200, 110, 150, 40), "Eliminar nodo", self.iniciar_eliminar_nodo, self.screen),
            Boton(pygame.Rect(self.area_control.x + 20, 170, 150, 40), "Crear usuario", self.iniciar_crear_usuario, self.screen),
            Boton(pygame.Rect(self.area_control.x + 20, 230, 150, 40), "Agregar arista", self.iniciar_agregar_arista, self.screen),
            Boton(pygame.Rect(self.area_control.x + 200, 230, 150, 40), "Eliminar arista", self.iniciar_eliminar_arista, self.screen),
            Boton(pygame.Rect(self.area_control.x + 20, 290, 150, 40), "Validar", self.validar_grafo, self.screen)  # Botón de validación
        ]
        
       
        #Estado
        self.modo_actual = None  # Modo actual (puede ser "nuevo_nodo" o "editar_nodo")      
        self.running = True

    def dibujar(self):
        """Dibuja el grafo y la interfaz en la pantalla"""
        # Colores
        NEGRO = (0, 0, 0)
        BLANCO = (255, 255, 255)
        ROJO = (255, 0, 0)
        GRIS = (150, 150, 150)
        VERDE = (0, 255, 0)
    
        # Fondo
        self.screen.fill(BLANCO)
    
        # Titulo
        font = pygame.font.Font(None, 36)
        texto_mapa = font.render("MAPA", True, NEGRO)
        ancho_texto = texto_mapa.get_width()
        pos_x = (self.ancho * 0.6 / 2) - (ancho_texto / 2)
        pos_y = (self.altura_titulo / 2) - (texto_mapa.get_height() / 2)
        self.screen.blit(texto_mapa, (pos_x, pos_y))
        
        # Dibujar áreas
        pygame.draw.rect(self.screen, NEGRO, self.area_mapa, 2)
        pygame.draw.rect(self.screen, GRIS, self.area_control)
        
        # Dibujar grafo
        self.interfaz_grafo.dibujar()
        
        #Dibujar botones
        for boton in self.botones:
            boton.dibujar()
            
        # Dibujar formulario
        if self.modo_actual:
            self.modo_actual.dibujar()
            
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

    def validar_grafo(self):
        """Llama al método de validación del grafo y muestra resultados"""
        self.grafo.validar_todos_con_boton()
        # Forzar sincronización completa después de la validación
        self.interfaz_grafo.posiciones_nodos = self.interfaz_grafo.calcular_posiciones()
        self.interfaz_grafo.dibujar()  # Redibujar para reflejar cambios

    def iniciar_crear_usuario(self):
        def on_finish(usuario_creado):
            self.usuario = usuario_creado
            self.modo_actual = None
            if self.usuario is not None:
                print("Usuario creado:", self.usuario)
                print("Usuario:", self.usuario.nombre)
                print("Experiencia:", self.usuario.experiencia)
                print("Riesgo:", self.usuario.riesgo_max)
                print("Accidentalidad:", self.usuario.accidentalidad_max)
                print("Dificultad:", self.usuario.dificultad_max)
                print("Distancia:", self.usuario.distancia_max)
                recorridos = Recorridos(self.grafo, self.usuario)
                print("Mejor recorrido respecto exp:",recorridos.camino_mas_apropiado_experiencia())
                print("Recorrido menos riesgo: ", recorridos.camino_menos_peligroso())
                print("Mejor recorrido segun el usuario:", recorridos.camino_por_distancia_riesgo_dificultad_deseada())

        
        self.modo_actual = InterfazUsuario(self.screen, self.area_mapa, on_finish)
    
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