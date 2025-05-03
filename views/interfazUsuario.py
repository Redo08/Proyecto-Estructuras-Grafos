from src.models.usuario import Usuario
from views.Formulario import Formulario

class InterfazUsuario:
    def __init__(self, screen, area_mapa, on_finish):
        self.screen = screen
        self.area_mapa = area_mapa
        self.on_finish = on_finish
        self.formulario = self.iniciar_formulario()
        
    def iniciar_formulario(self):
        campos = [
            "Nombre",
            "Nivel de experiencia (1,3)",
            "Distancia máxima",
            "Riesgo máximo (1,5)",
            "Accidentalidad máxima (1,5)",
            "Dificultad máxima (1,5)"
        ]
        formulario = Formulario(self.screen, campos, area_mapa=self.area_mapa)
        return formulario
    
    def manejar_evento(self, evento):
        self.formulario.manejar_evento(evento)
        
        #Verificar si ya se completó o canceló
        if self.formulario.esta_listo():
            datos = self.formulario.campos
            if self.verificacion(datos):
                try:
                    usuario = Usuario(
                        nombre = datos["Nombre"],
                        experiencia = int(datos["Nivel de experiencia (1,3)"]),
                        distancia_max = int(datos["Distancia máxima"]),
                        riesgo_max = int(datos["Riesgo máximo (1,5)"]),
                        accidentalidad_max = int(datos["Accidentalidad máxima (1,5)"]),
                        dificultad_max = int(datos["Dificultad máxima (1,5)"])
                    )
                    self.on_finish(usuario)
                except Exception as e:
                    print("Error al crear usuario: ", e)
                    self.on_finish(None)
                
        elif self.formulario.fue_cancelado():
            self.on_finish(None)
                
    def verificacion(self, datos):
        nombre = datos["Nombre"].strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        
        experiencia = int(datos["Nivel de experiencia (1,3)"])
        riesgo = int(datos["Riesgo máximo (1,5)"])
        accidentalidad = int(datos["Accidentalidad máxima (1,5)"])
        dificultad = int(datos["Dificultad máxima (1,5)"])
        distancia = float(datos["Distancia máxima"])
        
        for campo, valor in [
            ("riesgo", riesgo),
            ("accidentalidad", accidentalidad),
            ("dificultad", dificultad),
        ]:
            if not (1 <= valor <= 5):
                raise ValueError(f"El campo '{campo}' debe ser un entero entre 1 y 5.")
        if distancia <= 0:
            raise ValueError("La distancia debe ser mayor a 0.")
        if not 1 <= experiencia <= 3:
            raise ValueError("El nivel de experiencia debe ser entre 1 y 3")
        return True
    
    def dibujar(self):
        self.formulario.dibujar()
