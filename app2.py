# Crear un grafo
from src.helpers import Helpers
from src.models.grafo import Grafo
data = Helpers.cargar_texto_manual("archivos/nuevoJson.json")
grafo = Grafo()
grafo.cargar_json(data)

# Agregar nodos de interés
grafo.agregar_nodo_interes(nombre="Punto A", posicion=(100, 100))  # ID: Pu1
grafo.agregar_nodo_interes(nombre="Punto B", posicion=(300, 300))  # ID: Pu2
grafo.agregar_nodo_interes(nombre="Punto C", posicion=(500, 500))  # ID: Pu3

# Agregar aristas
grafo.agregar_arista("Pu1", "Pu2", peso=10, riesgo=0.5, accidentalidad=0.1, popularidad=0.8, dificultad=0.3)  # Arista 0, PC1
grafo.agregar_arista("Pu2", "Pu3", peso=15, riesgo=0.4, accidentalidad=0.2, popularidad=0.7, dificultad=0.4)  # Arista 1, PC2

# Agregar un segundo nodo de control a la primera arista
grafo.agregar_nodo_control(0, riesgo=0.6, accidentalidad=0.3, popularidad=0.9, dificultad=0.5)  # PC3

# Imprimir estado inicial
print("Nodos de interés:", [nodo.id for nodo in grafo.nodos])
print("Aristas creadas:", [(arista.origen.id, arista.destino.id) for arista in grafo.aristas])
print("Nodos de control en arista 0:", [nodo.id for nodo in grafo.aristas[0].nodos_control])
print("Posiciones de nodos de control en arista 0:", [nodo.posicion for nodo in grafo.aristas[0].nodos_control])
print("Nodos de control en arista 1:", [nodo.id for nodo in grafo.aristas[1].nodos_control])

# Eliminar nodo de control PC1
grafo.eliminar_nodo_control("PC1")
print("\nDespués de eliminar nodo de control PC1:")
print("Aristas creadas:", [(arista.origen.id, arista.destino.id) for arista in grafo.aristas])
print("Nodos de control en arista 0:", [nodo.id for nodo in grafo.aristas[0].nodos_control])
print("Posiciones de nodos de control en arista 0:", [nodo.posicion for nodo in grafo.aristas[0].nodos_control])

# Eliminar nodo de control PC3 (último en arista 0, debería eliminar la arista)
grafo.eliminar_nodo_control("PC3")
print("\nDespués de eliminar nodo de control PC3:")
print("Aristas creadas:", [(arista.origen.id, arista.destino.id) for arista in grafo.aristas])

# Probar con un nodo de control inexistente
grafo.eliminar_nodo_control("PC99")

# Guardar el grafo en un nuevo JSON
nuevo_json = grafo.guardar_json()
Helpers.guardar_texto(nuevo_json)
# Crear un nuevo grafo y cargar el JSON guardado
nuevo_grafo = Grafo()
data_nueva = Helpers.cargar_texto()
nuevo_grafo.cargar_json(data_nueva)

# Imprimir estado del nuevo grafo
print("\nEstado del grafo cargado desde el JSON guardado:")
print("Nodos de interés:", [nodo.id for nodo in nuevo_grafo.nodos])
print("Aristas creadas:", [(arista.origen.id, arista.destino.id) for arista in nuevo_grafo.aristas])
for i, arista in enumerate(nuevo_grafo.aristas):
    print(f"Nodos de control en arista {i} ({arista.origen.id} -> {arista.destino.id}):",
          [nodo.id for nodo in arista.nodos_control])
    print(f"Posiciones de nodos de control en arista {i}:",
          [nodo.posicion for nodo in arista.nodos_control])
