from src.models.usuario import Usuario
from views.Formulario import Formulario
import pygame

class InterfazUsuario:
    def __init__(self, screen, area_mapa, on_finish, campos=None ):
        self.screen = screen
        self.area_mapa = area_mapa
        self.on_finish = on_finish
        self.olvidar_validacion = False
        if campos:
            self.olvidar_validacion = True
        self.formulario = self.iniciar_formulario(campos)
        
    def iniciar_formulario(self, campos=None):
        campos = [
            "Nombre"
        ] if campos is None else campos
        formulario = Formulario(self.screen, campos, area_mapa=self.area_mapa)
        return formulario
    
    def manejar_evento(self, evento):
        self.formulario.manejar_evento(evento)
        
        #Verificar si ya se completó o canceló
        if self.formulario.esta_listo():
            datos = self.formulario.campos
            if self.verificacion(datos):
                try:
                    #Sacamos datos si existen
                    nombre = datos.get("Nombre", "").strip()
                    experiencia = int(datos.get("Nivel de experiencia (1,3)", 1))
                    distancia = float(datos.get("Distancia máxima", 0))
                    riesgo = int(datos.get("Riesgo máximo (1,5)", 1))
                    accidentalidad = int(datos.get("Accidentalidad máxima (1,5)", 1))
                    dificultad = int(datos.get("Dificultad máxima (1,5)", 1))
                    usuario = Usuario(
                        nombre = nombre,
                        experiencia = experiencia,
                        distancia_max = distancia,
                        riesgo_max = riesgo,
                        accidentalidad_max = accidentalidad,
                        dificultad_max = dificultad
                    )
                    self.on_finish(usuario)
                except Exception as e:
                    print("Error al crear usuario: ", e)
                    self.on_finish(None)
                
        elif self.formulario.fue_cancelado():
            self.on_finish(None)
                
    def verificacion(self, datos):
        if self.olvidar_validacion:
            return True
        nombre = datos.get("Nombre", "").strip()
        if not nombre:
            print("El nombre no puede estar vacío.")
            return False
        
        experiencia = int(datos.get("Nivel de experiencia (1,3)", 1))
        distancia = float(datos.get("Distancia máxima", 1))
        riesgo = int(datos.get("Riesgo máximo (1,5)", 1))
        accidentalidad = int(datos.get("Accidentalidad máxima (1,5)", 1))
        dificultad = int(datos.get("Dificultad máxima (1,5)", 1))
        
        for campo, valor in [
            ("riesgo", riesgo),
            ("accidentalidad", accidentalidad),
            ("dificultad", dificultad),
        ]:
            if not (1 <= valor <= 5):
                print(f"El campo '{campo}' debe ser un entero entre 1 y 5.")
                return False
        if distancia <= 0:
            print("La distancia debe ser mayor a 0.")
            return False
        if not 1 <= experiencia <= 3:
            print("El nivel de experiencia debe ser entre 1 y 3")
            return False
        return True
    
    def dibujar(self):
        self.formulario.dibujar()