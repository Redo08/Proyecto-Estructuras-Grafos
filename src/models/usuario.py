class Usuario:
    def __init__(self, nombre, experiencia=None, distancia_max=None, riesgo_max=None, accidentalidad_max=None, dificultad_max=None):
        self.nombre = nombre
        self.experiencia = experiencia
        self.distancia_max = distancia_max
        self.riesgo_max = riesgo_max
        self.accidentalidad_max = accidentalidad_max
        self.dificultad_max = dificultad_max
        
    