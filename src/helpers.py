import  json
from tkinter import Tk, Button, Label
from tkinter.filedialog import askopenfilename, asksaveasfilename
class Helpers:
    def __init__(self):
        pass
    
    def cargar_texto(self): #
        ruta = askopenfilename(filetypes=[("JSON files", "*.json")]) #Solo archivos que terminan en .json
        if ruta: # Si existe una ruta, lo abre y lee
            with open(ruta, 'r', encoding="utf-8") as archivo:
                grafo = json.load(archivo)
            print("grafo cargado", grafo)

            
    def guardar_texto(self, grafo): #
        ruta = asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if ruta:
            with open(ruta, 'w', encoding="utf-8") as archivo:
                json.dump(grafo, archivo, indent=4)    

if __name__ == "__main__":
    grafo = {"A": {"B": 10, "C": 12},
             "B": {"A":12}}
    helpers = Helpers()
    ventana = Tk()
    Button(ventana, text="Cargar grafo", command=helpers.cargar_texto).pack()
    Button(ventana, text="Guardar grafo", command= lambda: helpers.guardar_texto(grafo)).pack()
    ventana.mainloop()