class Nodo:
    def __init__(self, id, nombre, descripcion, riesgo, tipo, accidentalidad, popularidad, dificultad, posicion=None):
        self.id = id
        self.tipo = tipo  # 0 para punto de interés, 1 para punto de control
        self.posicion = posicion  #(x,y)
        if self.tipo ==0:
            self.nombre = nombre
            self.descripcion = descripcion
           
        
        #Si es un punto de control, tiene los atributos de punto de control.
        if self.tipo == 1:
            self.nombre = None
            self.descripcion = None
            self.riesgo = riesgo
            self.accidentalidad = accidentalidad
            self.popularidad = popularidad
            self.dificultad = dificultad   
