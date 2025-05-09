import pygame
from src.helpers import Helpers
from views.Formulario import Formulario

class InterfazArista:
    def __init__(self, screen, area_mapa, grafo, interfaz_grafo, on_finish, modo):
        self.screen = screen
        self.area_mapa = area_mapa
        self.grafo = grafo
        self.interfaz_grafo = interfaz_grafo
        self.on_finish = on_finish
        self.modo = modo  # "agregar_arista" o "eliminar_arista", "agregar punto de control"
        self.esperando_seleccion = True
        self.nodos_seleccionados = []
        self.formulario = None
        #self.campos_iniciales = ["peso"] if modo == "agregar_arista" else None
        #self.condiciones = None
    
    def manejar_evento(self, event):
        if self.esperando_seleccion:
            self._manejar_seleccion_nodos(event)
        elif self.formulario:
            self._manejar_formulario(event)

    def _manejar_seleccion_nodos(self, event):
        """Selecciona dos nodos de tipo 0 secuencialmente."""
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.area_mapa.collidepoint(event.pos):
            nodo = self.interfaz_grafo.seleccionar_nodo(event)
            if nodo:
                 # Asegurarse de que el nodo sea de interés (tipo 0)
                if nodo.tipo != 0:
                    self.formulario = Formulario(self.screen, [], None, self.area_mapa,
                                                "Error: Seleccione un nodo de interés (tipo 0).", accion="error")
                    self.esperando_seleccion = False
                    return
                if len(self.nodos_seleccionados) == 0:
                    self.nodos_seleccionados.append(nodo)
                    self.interfaz_grafo.nodos_resaltados.append(nodo)
                    print(f"Primer nodo seleccionado: {nodo.id}")
                elif len(self.nodos_seleccionados) == 1:
                    if nodo.id == self.nodos_seleccionados[0].id:
                        self.formulario = Formulario(self.screen, [], None, self.area_mapa, 
                                                    "Error: No puede seleccionar el mismo nodo.", accion="error")
                    else:
                        self.nodos_seleccionados.append(nodo)
                        self.interfaz_grafo.nodos_resaltados.append(nodo)
                        print(f"Segundo nodo seleccionado: {nodo.id}")
                        self.esperando_seleccion = False
                        
                        if self.modo == "agregar_arista":
                            campos_iniciales = ["peso", "riesgo", "accidentalidad", "popularidad", "dificultad"]
                            self.formulario = Formulario(self.screen, campos_iniciales, None, self.area_mapa,
                                                        accion="agregar_arista")
                        elif self.modo == "agregar_nodo_control":
                            # Verificar si la arista existe
                            arista = Helpers.hallar_arista_por_nodos(self.grafo.aristas,self.nodos_seleccionados[0].id, self.nodos_seleccionados[1].id)
                            if arista:
                                campos_iniciales = ["riesgo", "accidentalidad", "popularidad", "dificultad"]
                                print(f"Campos iniciales para formulario: {campos_iniciales}")  # Depuración
                                self.formulario = Formulario(self.screen, campos_iniciales, None, self.area_mapa,
                                                            accion="agregar_nodo_control")
                            else:
                                self.formulario = Formulario(self.screen, [], None, self.area_mapa,
                                                            "Error: No existe una arista entre los nodos seleccionados.", accion="error")
                        elif self.modo == "eliminar_arista":
                            self._procesar_eliminar_arista()
            else:
                self.formulario = Formulario(self.screen, [], None, self.area_mapa, 
                                            "Error: Seleccione un nodo de interés (tipo 0).", accion="error")
                self.esperando_seleccion = False

    def _manejar_formulario(self, event):
        self.formulario.manejar_evento(event)
        if self.formulario.fue_cancelado():
            print(f"Acción de {self.modo} cancelada.")
            self.interfaz_grafo.limpiar_resaltado()
            self.nodos_seleccionados = []
            self.on_finish()
        elif self.formulario.esta_listo():
            if self.modo == "agregar_arista":
                self._agregar_arista()
            elif self.modo == "agregar_nodo_control":
                self._agregar_nodo_control()
            elif self.modo == "eliminar_arista":
                self._procesar_eliminar_arista()

    def _agregar_arista(self):
        try:
            peso = Helpers.quitar_decimales_si_no_hay(float(self.formulario.campos["peso"]))
            if peso <= 0:
                self.formulario = Formulario(self.screen, None, None, self.area_mapa, "El peso debe ser positivo.", accion="error")
                return
            riesgo = self.formulario.campos["riesgo"].strip()
            accidentalidad = self.formulario.campos["accidentalidad"].strip()
            popularidad = self.formulario.campos["popularidad"].strip()
            dificultad = self.formulario.campos["dificultad"].strip()
            if not (riesgo and accidentalidad and popularidad and dificultad):
                self.formulario = Formulario(self.screen, [], None, self.area_mapa, 
                                            "Error: Todos los campos del nodo de control deben estar completos.", accion="error")
                return
            
            self.grafo.agregar_arista(self.nodos_seleccionados[0].id, self.nodos_seleccionados[1].id, peso, riesgo, accidentalidad, popularidad, dificultad)
            print(f"Arista agregada: {self.nodos_seleccionados[0].id} -> {self.nodos_seleccionados[1].id}, peso: {peso}")
            self.interfaz_grafo.limpiar_resaltado()
            self.nodos_seleccionados = []
            self.on_finish()
        except ValueError:
            self.formulario = Formulario(self.screen, None, None, self.area_mapa, "Peso inválido.", accion="error")

    def _procesar_eliminar_arista(self):
        try:
            valido, mensaje = self.grafo.validar_eliminar_arista(self.primer_nodo, self.segundo_nodo)
            if not valido:
                self.formulario = Formulario(self.screen, None, None, self.area_mapa, mensaje, accion="error")
                return
            self.grafo.eliminar_arista(self.primer_nodo, self.segundo_nodo)
            self.interfaz_grafo.posiciones_nodos = self.interfaz_grafo.calcular_posiciones()
            print(f"Arista eliminada: {self.primer_nodo} -> {self.segundo_nodo}")
            self.interfaz_grafo.limpiar_resaltado()
            self.on_finish()
        except Exception as e:
            self.formulario = Formulario(self.screen, None, None, self.area_mapa, f"Error: {str(e)}", accion="error")            
    def _agregar_nodo_control(self):
        try:
            riesgo = self.formulario.campos["riesgo"].strip()
            accidentalidad = self.formulario.campos["accidentalidad"].strip()
            popularidad = self.formulario.campos["popularidad"].strip()
            dificultad = self.formulario.campos["dificultad"].strip()
            if not (riesgo and accidentalidad and popularidad and dificultad):
                self.formulario = Formulario(self.screen, [], None, self.area_mapa, 
                                            "Error: Todos los campos del nodo de control deben estar completos.", accion="error")              
                return
            
            arista= Helpers.hallar_arista_por_nodos(self.grafo.aristas,self.nodos_seleccionados[0].id, self.nodos_seleccionados[1].id)
            arista.agregar_nodo_control(self.nodos_seleccionados[0].id, self.nodos_seleccionados[1].id, riesgo, accidentalidad, popularidad, dificultad)
            print(f"Nodo de control agregado entre: {self.nodos_seleccionados[0].id} y {self.nodos_seleccionados[1].id}")
            self.interfaz_grafo.limpiar_resaltado()
            self.nodos_seleccionados = []
            self.on_finish()
        except Exception as e:
            self.formulario = Formulario(self.screen, None, None, self.area_mapa, f"Error: {str(e)}", accion="error")

    def dibujar(self):
        if self.formulario:
            self.formulario.dibujar()
       