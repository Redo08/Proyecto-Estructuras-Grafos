class Nodo:
    def __init__(self, id, nombre, descripcion, riesgo, tipo, accidentalidad, popularidad, dificultad, posicion=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.tipo = tipo # Tipo -> 0 Punto de interes, 1 Punto de control
        self.posicion = posicion # (x,y)
        
        #Si es un punto de control, tiene los atributos de punto de control.
        if self.tipo == 1:
            self.nombre = None
            self.descripcion = None
            self.riesgo = riesgo
            self.accidentalidad = accidentalidad
            self.popularidad = popularidad
            self.dificultad = dificultad       
