# Crear un grafo
import src.models.grafo as grafo
grafo = grafo.Grafo()

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