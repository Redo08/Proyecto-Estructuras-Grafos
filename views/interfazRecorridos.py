from src.models.recorridos import Recorridos
class InterfazRecorridos:
    def __init__(self, screen, area_mapa, grafo, interfaz_grafo, usuario, on_finish):
        self.screen = screen
        self.area_mapa = area_mapa
        self.grafo = grafo
        self.interfaz_grafo = interfaz_grafo
        self.usuario = usuario
        self.on_finish = on_finish
        self.formulario = None
        self.tipo_actual = None
        self.botones = self.crear_botones()
        
    def crear_botones(self):
        tipos = []
        
        
