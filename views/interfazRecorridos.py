from src.models.recorridos import Recorridos
from views.boton import Boton
from views.Formulario import Formulario
from views.interfazUsuario import InterfazUsuario
from src.helpers import Helpers
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
        self.nodo_seleccionado = None #Almacena el nodo seleccionado para el recorrido
        self.esperando_seleccion = False  # Estado para esperar selección de nodo

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
            self.formulario = None
        elif tipo == "menos_peligroso":
            self.actualizar_riesgo()
            self.formulario = None
        elif tipo == "balanceado":
            self.mostrar_subinterfaz([
                "Distancia máxima",
                "Riesgo máximo (1,5)",
                "Dificultad máxima (1,5)"
            ], self.actualizar_balanceado)
            self.formulario = None
            
        elif tipo == "mejor_experiencia_distancia":
            self.mostrar_subinterfaz([
                "Nivel de experiencia (1,3)",
                "Distancia máxima",
                "Dificultad máxima (1,5)"
            ], self.actualizar_experiencia_distancia)
            self.formulario = None
            
        elif tipo == "todos_todos":
            self.esperando_seleccion = True  # Activar estado de espera
            self.mensaje = "Por favor, selecciona un nodo haciendo clic en el mapa."
            self.nodo_seleccionado = None  # Reiniciar selección
            self.formulario = None  # Ocultar el formulario
           

    def actualizar_experiencia(self, nuevo_usuario):
        self.actualizar_recorrido(nuevo_usuario, ["experiencia"], "camino_mas_apropiado_experiencia")
    
    def actualizar_riesgo(self):
        #Llamar recorrido
        camino = self.recorrido.camino_menos_peligroso()            
        #Mostrarlo en interfaz
        self.mostrar_en_interfaz(camino)
    
    def actualizar_balanceado(self, nuevo_usuario):
        self.actualizar_recorrido(nuevo_usuario, ["distancia_max", "riesgo_max", "dificultad_max"], "camino_por_distancia_riesgo_dificultad_deseada")

    def actualizar_experiencia_distancia(self, nuevo_usuario):
        self.actualizar_recorrido(nuevo_usuario, ["experiencia", "distancia_max", "dificultad_max"], "camino_distancia_dificultad_experiencia")

    def todos_todos(self):
        if self.nodo_seleccionado is None:
            self.mensaje = "Por favor, selecciona un nodo haciendo clic en el mapa."
            return

        if self.nodo_seleccionado.tipo == 1:
            self.mensaje = "Por favor, selecciona un nodo de Interes, no uno de control."
            return
        
        #Llamar recorrido de floyd-warshall y mostrarlo
        camino = self.recorrido.camino_disntacias_minimas_desde_nodo_dado(self.nodo_seleccionado.id) 
        print("Camino:", camino)
        #Mostrarlo en interfaz
        self.mostrar_en_interfaz(camino)
        self.esperando_seleccion = False 
        
    def mostrar_subinterfaz(self, campos, callback):
        self.sub_interfaz_usuario = InterfazUsuario(
            self.screen,
            self.area_mapa,
            on_finish=callback,
            campos=campos
        )
        
    def mostrar_en_interfaz(self, camino):
        if isinstance(camino, dict):
            self.interfaz_grafo.mostrar_caminos(camino)
        else:
            self.interfaz_grafo.mostrar_camino(camino)
        self.mostrar_informacion(camino)
        
    def actualizar_recorrido(self, nuevo_usuario, atributos_usuario, metodo_recorrido):
        if nuevo_usuario:
            for attr in atributos_usuario:
                setattr(self.usuario, attr, getattr(nuevo_usuario, attr))
            print(f"Atributos actualizados: {[getattr(self.usuario, attr) for attr in atributos_usuario]}") 
            self.recorrido.recalcular_usuario(self.usuario)
            try:    
                camino = getattr(self.recorrido, metodo_recorrido)()
                if not camino:
                    self.mensaje = f"No existe un recorrido valido con las opciones dadas."
                else:
                    # Mostrar en interfaz
                    self.mostrar_en_interfaz(camino)
            except Exception as e:
                self.mensaje = f"Error al calcular el recorrido: \n {e}"
                
        self.sub_interfaz_usuario = None
        
    #MODIFICAR
    def sacar_informacion(self, camino):
        if camino:
            origen = camino[0][0]
            fin = camino[0][-1]
            
            nodo_origen = Helpers.hallar_nodo(self.grafo.nodos, origen)
            nodo_fin = Helpers.hallar_nodo(self.grafo.nodos, fin)
            
            nombre_inicio = nodo_origen.nombre
            descripcion_inicio = nodo_origen.descripcion
            nombre_fin = nodo_fin.nombre
            descripcion_fin = nodo_fin.descripcion

            informacion_nodos = {}
            for i in camino[-1]: #Ultima posicion porque ahi estan los nodos_control
                nodo_control = Helpers.hallar_nodo_control(self.grafo.aristas, i)
                riesgo_nodo = nodo_control.riesgo
                accidentalidad_nodo = nodo_control.accidentalidad
                popularidad_nodo = nodo_control.popularidad
                dificultad_nodo = nodo_control.dificultad
                informacion_nodos.update({i: (riesgo_nodo, accidentalidad_nodo, popularidad_nodo, dificultad_nodo)})            
            
            return nombre_inicio, descripcion_inicio, nombre_fin, descripcion_fin, informacion_nodos
        return None

    #MODIFICAR
    def sacar_informacion_todos(self, caminos_dict):
        informacion_rutas = {}
        
        for destino, (costo, camino) in caminos_dict.items():
            if not camino:
                continue
            
            origen = camino[0]
            fin = camino[-1]

            nombre_inicio = self.grafo.nodos[origen].nombre
            descripcion_inicio = self.grafo.nodos[origen].descripcion
            nombre_fin = self.grafo.nodos[fin].nombre
            descripcion_fin = self.grafo.nodos[fin].descripcion

            informacion_nodos = {}
            for i in camino:
                nodo = self.grafo.nodos[i] if self.grafo.nodos[i].tipo == 1 else None
                if nodo is not None:
                    informacion_nodos[i] = (
                        nodo.riesgo,
                        nodo.accidentalidad,
                        nodo.popularidad,
                        nodo.dificultad
                    )
            # Guardar la información asociada
            informacion_rutas[destino] = (
                nombre_inicio,
                descripcion_inicio,
                nombre_fin,
                descripcion_fin,
                informacion_nodos,
                costo
            )

        return informacion_rutas
    
    def mostrar_informacion(self, camino):
        
        if isinstance(camino, dict):
            datos = self.sacar_informacion_todos(camino)
            lineas = []
            for destino, (nombre_inicio, _, nombre_fin, _, info_control, costo) in datos.items():
                lineas.extend([
                    f"{nombre_inicio} -> {nombre_fin} ({destino}) ",
                    f" Costo: {costo}",
                    f" Nodos de control: {len(info_control)}",
                ])
        else:  
            datos = self.sacar_informacion(camino)
        
            print(datos)
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
                linea = f"Nodo {id_nodo} - Riesgo: {riesgo}, Accidentalidad: {accidentalidad}, \n  Popularidad: {popularidad}, Dificultad: {dificultad}"
                lineas.append(linea)

        self.mensaje = "\n".join(lineas)
        self.dibujar()
        
    def manejar_evento(self, evento):
        if self.sub_interfaz_usuario:
            self.sub_interfaz_usuario.manejar_evento(evento)
        elif self.formulario:
            self.formulario.manejar_evento(evento)
        elif self.esperando_seleccion:
            # Verificar si se selecciona un nodo en el área del mapa
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1 and self.area_mapa.collidepoint(evento.pos):
                nodo = self.interfaz_grafo.seleccionar_nodo(evento)
                if nodo:
                    self.nodo_seleccionado = nodo
                    print(f"Nodo seleccionado para 'todos_todos': {self.nodo_seleccionado}")    
                self.todos_todos()  # Calcular y mostrar el camino tras seleccionar
                
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