from src.models.recorridos import Recorridos
from views.boton import Boton
from views.Formulario import Formulario
from views.interfazUsuario import InterfazUsuario
import pygame
class InterfazRecorridos:
    def __init__(self, screen, area_mapa, grafo, interfaz_grafo, usuario, area_info, on_finish):
        self.screen = screen
        self.area_mapa = area_mapa
        self.area_info = area_info
        self.usuario = usuario
        self.grafo = grafo
        self.recorrido = Recorridos(grafo, self.usuario)
        self.interfaz_grafo = interfaz_grafo
        self.on_finish = on_finish  
        self.formulario = None
        self.botones = self.crear_botones()
        self.sub_interfaz_usuario = None 
        self.mensaje = ""

    def crear_botones(self):
        botones = [
            Boton(pygame.Rect(self.area_mapa.x + 120, self.area_mapa.y + 150, 150, 40),
                  "Camino más apropiado experiencia",
                  lambda: self.seleccionar_tipo_recorrido("mejor_experiencia"),
                  self.screen,
                  color_fondo=(100,100,255)),
            Boton(pygame.Rect(self.area_mapa.x + 300, self.area_mapa.y + 150, 150, 40),
                  "Camino menos peligroso",
                  lambda: self.seleccionar_tipo_recorrido("menos_peligroso"),
                  self.screen,
                  color_fondo=(100,100,255)),
            Boton(pygame.Rect(self.area_mapa.x + 120, self.area_mapa.y + 210, 150, 40),
                  "Camino equilibrado distancia, dificultad y riesgo",
                  lambda: self.seleccionar_tipo_recorrido("balanceado"),
                  self.screen,
                  color_fondo=(100,100,255)),
            Boton(pygame.Rect(self.area_mapa.x + 300, self.area_mapa.y + 210, 150, 40),
                  "Camino más apropiado experiencia(2)",
                  lambda: self.seleccionar_tipo_recorrido("mejor_experiencia_distancia"),
                  self.screen,
                  color_fondo=(100,100,255)),
            Boton(pygame.Rect(self.area_mapa.x + 120, self.area_mapa.y + 270, 150, 40),
                  "De un nodo a todos",
                  lambda: self.seleccionar_tipo_recorrido("todos_todos"),
                  self.screen,
                  color_fondo=(100,100,255)),
            Boton(pygame.Rect(self.area_mapa.x + 300, self.area_mapa.y + 270, 150, 40),
                  "Volver",
                  lambda: self.on_finish(),
                  self.screen,
                  color_fondo=(255,0,0)),
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
            print("Caminooo", camino)
            
            #Mostrarlo en interfaz
            self.interfaz_grafo.mostrar_camino(camino)
            self.mostrar_informacion(camino)
            
        self.sub_interfaz_usuario = None
    
    def actualizar_riesgo(self, nuevo_usuario):
        if nuevo_usuario:
            self.usuario.riesgo_max = nuevo_usuario.riesgo_max
            print("Riesgo actualizada", self.usuario.riesgo_max)
            #Llamar recorrido
            self.recorrido.recalcular_usuario(self.usuario)
            camino = self.recorrido.camino_menos_peligroso()
            print("Caminoo", camino)
            
            #Mostrarlo en interfaz
            self.interfaz_grafo.mostrar_camino(camino)
            
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
            print("Caminooo", camino)
            #Mostrarlo en interfaz
            self.interfaz_grafo.mostrar_camino(camino)
            self.mostrar_informacion(camino)
                        
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

            print("Caminooo", camino)
            #Mostrarlo en interfaz
            self.interfaz_grafo.mostrar_camino(camino)
            self.on_finish()
                        
        self.sub_interfaz_usuario = None
    
    def todos_todos(self):
        #Sacar nodo clickeado (Esto esta en interfazGrafo)
        #Llamar recorrido de floyd-warshall y mostrarlo
        camino = self.recorrido.camino_disntacias_minimas_desde_nodo_dado() 
        print("Caminooo", camino)
        #Mostrarlo en interfaz
        self.interfaz_grafo.mostrar_camino(camino)
        self.on_finish()        
        
    
    def mostrar_subinterfaz(self, campos, callback):
        self.sub_interfaz_usuario = InterfazUsuario(
            self.screen,
            self.area_mapa,
            on_finish=callback,
            campos=campos
        )
        
    def sacar_informacion(self, camino):
        if camino:
            origen = camino[0][0]
            fin = camino[0][-1]
            
            nombre_inicio = self.grafo.nodos[origen].nombre
            descripcion_inicio = self.grafo.nodos[origen].descripcion
            nombre_fin = self.grafo.nodos[fin].nombre
            descripcion_fin = self.grafo.nodos[fin].descripcion

            informacion_nodos = {}
            for i in camino[-1]:
                riesgo_nodo = self.grafo.nodos[i].riesgo
                accidentalidad_nodo = self.grafo.nodos[i].accidentalidad
                popularidad_nodo = self.grafo.nodos[i].popularidad
                dificultad_nodo = self.grafo.nodos[i].dificultad
                informacion_nodos.update({i: (riesgo_nodo, accidentalidad_nodo, popularidad_nodo, dificultad_nodo)})            
            
            return nombre_inicio, descripcion_inicio, nombre_fin, descripcion_fin, informacion_nodos
        return None
    
    
    def mostrar_informacion(self, camino):
        datos = self.sacar_informacion(camino)
        if not datos:
            self.mensaje = "No se encontro un recorrido valido"
            return

        nombre_inicio, descripcion_inicio, nombre_fin, descripcion_fin, info_control = datos
        lineas = [
            f"Inicio: {nombre_inicio}",
            f"Descripción: {descripcion_inicio}",
            f"",
            f"Fin: {nombre_fin}",
            f"Descripción: {descripcion_fin}",
            f"",
            f"Detalles nodos de control:"
        ]
        
        for id_nodo, (riesgo, accidentalidad, popularidad, dificultad) in info_control.items():
            linea = f"Nodo {id_nodo} - Riesgo: {riesgo}, Accidentalidad: {accidentalidad}, Popularidad: {popularidad}, Dificultad: {dificultad}"
            lineas.append(linea)
        
        self.mensaje = "\n".join(lineas)
        self.dibujar()
        
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
        if self.mensaje:
            y = self.area_info.y + 10
            for linea in self.mensaje.split("\n"):
                pygame.draw.rect(self.screen, (0, 255, 0), self.area_info, 2)  # borde verde
                texto = pygame.font.Font(None, 24).render(linea, True, (0,0,0))
                self.screen.blit(texto, (self.area_info.x + 10, y))
                y += 25