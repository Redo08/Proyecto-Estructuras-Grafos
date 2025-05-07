import  json
from tkinter import filedialog, Tk

class Helpers:
    def __init__(self):
        pass
    
    def cargar_texto_manual(self, ruta):
        if ruta:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                grafo = json.load(archivo)
                return grafo
        print("No me entro nada we")
        return None
    
    def cargar_texto():
        """Carga el texto, abriendo solo JSON"""
        Tk().withdraw()
        ruta = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")]) #Solo archivos que terminan en .json
        if ruta: # Si existe una ruta, lo abre y lee
            with open(ruta, 'r', encoding="utf-8") as archivo:
                grafo = json.load(archivo)
                print("grafo cargado", grafo)
                return grafo
        return None
    
    def guardar_texto(grafo): 
        """Guarda un nuevo archivo, pasando como argumento el grafo actual"""
        Tk().withdraw()
        ruta = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if ruta:
            with open(ruta, 'w', encoding="utf-8") as archivo:
                json.dump(grafo, archivo, indent=4)    

    def quitar_decimales_si_no_hay(numero):
        numero_str = str(numero)
        if numero_str.endswith('.0'):
            return int(numero)
        return numero
    
    # Si el nodo existe
    def hallar_nodo( lista_nodos, id_nodo):
        for nodo in lista_nodos:
            if nodo.id == id_nodo:
                return nodo
        return None
    def hallar_arista_por_nodo_control(lista_aristas, id_nodo_control):
        """
        Busca la arista que contiene un nodo de control con el ID especificado.
        Retorna la arista si la encuentra, None si no.
        """
        for arista in lista_aristas:
            if Helpers.hallar_nodo(arista.nodos_control, id_nodo_control):
                return arista
        return None
    
    def hallar_indice_arista_por_nodo_control(lista_aristas, id_nodo_control):
        """
        Busca el índice de la arista que contiene un nodo de control con el ID especificado.
        Retorna el índice si lo encuentra, -1 si no.
        """
        for idx, arista in enumerate(lista_aristas):
            if Helpers.hallar_nodo(arista.nodos_control, id_nodo_control):
                return idx
        return -1
