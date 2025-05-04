from src.models.recorridos import Recorridos
from views.boton import Boton
from views.Formulario import Formulario
from views.interfazUsuario import InterfazUsuario
import pygame
class InterfazRecorridos:
    def __init__(self, screen, area_mapa, grafo, interfaz_grafo, usuario, on_finish):
        self.screen = screen
        self.area_mapa = area_mapa
        self.usuario = usuario
        self.recorrido = Recorridos(grafo, self.usuario)
        self.interfaz_grafo = interfaz_grafo
        self.on_finish = on_finish  
        self.formulario = None
        self.botones = self.crear_botones()
        self.sub_interfaz_usuario = None 

    def crear_botones(self):
        botones = [
            Boton(pygame.Rect(self.area_mapa.x + 120, self.area_mapa.y + 100 + i* 50, 150, 40),
                  texto,
                  lambda tipo = t: self.seleccionar_tipo_recorrido(tipo),
                  self.screen,
                  color_fondo=(100,100,255)
                  
                )
            for i, (t,texto) in enumerate([
                ("mejor_experiencia", "Camino más apropiado experiencia"),
                ("menos_peligroso", "Camino menos peligroso"),
                ("balanceado", "Camino equilibrado distancia, dificultad y riesgo"),
                ("mejor_experiencia_distancia", "Camino más apropiado experiencia, distancia y dificultad"),
                ("todos_todos", "De un nodo a todos")
            ])
        ]
        self.formulario = Formulario(
            self.screen,
            area_mapa=self.area_mapa,
            accion="recorridos",
            botones=botones
        )
        return botones
        
    def seleccionar_tipo_recorrido(self, tipo):
        if tipo == "mejor_experiencia":
            #Recalcular datos usuario
            self.mostrar_subinterfaz(["Nivel de experiencia (1,3)"], self.actualizar_experiencia)
        elif tipo == "menos_peligroso":
            self.mostrar_subinterfaz(["Riesgo máximo (1,5)"], self.actualizar_riesgo)
        elif tipo == "balanceado":
            self.mostrar_subinterfaz([
                "Distancia máxima",
                "Riesgo máximo (1,5)",
                "Dificultad máxima (1,5)"
            ], self.actualizar_balanceado)
            
        elif tipo == "mejor_experiencia_distancia":
            self.mostrar_subinterfaz([
                "Nivel de experiencia (1,3)",
                "Distancia máxima",
                "Dificultad máxima (1,5)"
            ], self.actualizar_experiencia_distancia)
            
        elif tipo == "todos_todos":
            self.todos_todos()

    def actualizar_experiencia(self, nuevo_usuario):
        if nuevo_usuario:
            self.usuario.experiencia = nuevo_usuario.experiencia
            print("Experiencia actualizada", self.usuario.experiencia)
            #Llamar recorrido
            self.recorrido.recalcular_usuario(self.usuario)
            camino = self.recorrido.camino_mas_apropiado_experiencia()
            
            #Mostrarlo en interfaz
            #self.interfaz_grafo.mostrar_camino(camino)
            self.on_finish()
            
        self.sub_interfaz_usuario = None
    
    def actualizar_riesgo(self, nuevo_usuario):
        if nuevo_usuario:
            self.usuario.riesgo_max = nuevo_usuario.riesgo_max
            print("Riesgo actualizada", self.usuario.riesgo_max)
            #Llamar recorrido
            self.recorrido.recalcular_usuario(self.usuario)
            camino = self.recorrido.camino_menos_peligroso()
            
            #Mostrarlo en interfaz
            #self.interfaz_grafo.mostrar_camino(camino)
            self.on_finish()
            
        self.sub_interfaz_usuario = None
    
    
    def actualizar_balanceado(self, nuevo_usuario):
        if nuevo_usuario:
            self.usuario.distancia_max  = nuevo_usuario.distancia_max
            self.usuario.riesgo_max = nuevo_usuario.riesgo_max
            self.usuario.dificultad_max = nuevo_usuario.dificultad_max
            print("distancia actualizada", self.usuario.distancia_max)
            #Llamar recorrido
            self.recorrido.recalcular_usuario(self.usuario)
            camino = self.recorrido.camino_por_distancia_riesgo_dificultad_deseada() 

            #Mostrarlo en interfaz
            #self.interfaz_grafo.mostrar_camino(camino)
            self.on_finish()
                        
        self.sub_interfaz_usuario = None

    def actualizar_experiencia_distancia(self, nuevo_usuario):
        if nuevo_usuario:
            self.usuario.distancia_max  = nuevo_usuario.distancia_max
            self.usuario.experiencia = nuevo_usuario.experiencia
            self.usuario.dificultad_max = nuevo_usuario.dificultad_max
            print("distancia actualizada", self.usuario.distancia_max)
            #Llamar recorrido
            self.recorrido.recalcular_usuario(self.usuario)
            camino = self.recorrido.camino_distancia_dificultad_experiencia() 

            #Mostrarlo en interfaz
            #self.interfaz_grafo.mostrar_camino(camino)
            self.on_finish()
                        
        self.sub_interfaz_usuario = None
    
    def todos_todos(self):
        #Sacar nodo clickeado (Esto esta en interfazGrafo)
        #Llamar recorrido de floyd-warshall y mostrarlo
        camino = self.recorrido.camino_disntacias_minimas_desde_nodo_dado() 
        #Mostrarlo en interfaz
        #self.interfaz_grafo.mostrar_camino(camino)
        self.on_finish()        
        
    
    def mostrar_subinterfaz(self, campos, callback):
        self.sub_interfaz_usuario = InterfazUsuario(
            self.screen,
            self.area_mapa,
            on_finish=callback,
            campos=campos
        )

    def aplicar_recorridos(self, modificador_usuario_fn, metodo_recorrido):
        modificador_usuario_fn()
        self.recorrido.recalcular_usuario(self.usuario)
        camino = metodo_recorrido()
        self.on_finish()
        self.sub_interfaz_usuario = None
        
    def manejar_evento(self, evento):
        if self.sub_interfaz_usuario:
            self.sub_interfaz_usuario.manejar_evento(evento)
        elif self.formulario:
            self.formulario.manejar_evento(evento)
            
    
    def dibujar(self):
        if self.sub_interfaz_usuario:
            self.sub_interfaz_usuario.dibujar()
        elif self.formulario:
            self.formulario.dibujar()
    