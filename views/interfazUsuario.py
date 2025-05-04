from src.models.usuario import Usuario
from views.Formulario import Formulario

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
            "Nombre",
            "Nivel de experiencia (1,3)",
            "Distancia máxima",
            "Riesgo máximo (1,5)",
            "Accidentalidad máxima (1,5)",
            "Dificultad máxima (1,5)"
        ] if campos is None else campos
        formulario = Formulario(self.screen, campos, area_mapa=self.area_mapa)
        return formulario
    
    def manejar_evento(self, evento):
        self.formulario.manejar_evento(evento)
        
        #Verificar si ya se completó o canceló
        if self.formulario.esta_listo():
            datos = self.formulario.campos
            if self.verificacion(datos) or self.olvidar_validacion:
                try:
                    usuario = Usuario(
                        nombre = datos["Nombre"] if datos["Nombre"] is not None else "",
                        experiencia = int(datos["Nivel de experiencia (1,3)"]) if datos["Nivel de experiencia (1,3)"] is not None else 1,
                        distancia_max = int(datos["Distancia máxima"]) if datos["Distancia máxima"] else None,
                        riesgo_max = int(datos["Riesgo máximo (1,5)"]) if datos["Riesgo máximo (1,5)"] else None,
                        accidentalidad_max = int(datos["Accidentalidad máxima (1,5)"]) if datos["Accidentalidad máxima (1,5)"] else None,
                        dificultad_max = int(datos["Dificultad máxima (1,5)"]) if datos["Dificultad máxima (1,5)"] else None
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
            print("El nombre no puede estar vacío.")
            return False
        
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
