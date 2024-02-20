#Algoritmo de ordenamiento Merge Sort tanto de la forma Secuencial como Paralela.
#Además se pueden observar las métricas finales una vez se ejecuta todo el programa.

import os #para ver información referente al número de CPUs
import threading #para crear subprocesos
import time #para medir el tiempo de ejecucion
import random #generar los elementos aleatorios de nueestro arreglo
import math

#muestra el número de procesadroes con los que cuenta el sistema
NUM_CPU = os.cpu_count()
print("El número de CPU del sistema es igual a:", NUM_CPU)

#numero de elementos del arreglo
NUM_ELEMENTOS = 1666666
#el limite de la profundidad viene dada por el logaritmo en base 2 del número de procesadores
PROFUNDIDAD_MAXIMA = int(math.log2(NUM_CPU))
print("La profundidad límite es:",PROFUNDIDAD_MAXIMA)
#PROFUNDIDAD_MAXIMA=4

#Se crea un arreglo vacio con el tamaño de NUM_ELEMENTOS
arreglo = [0] * NUM_ELEMENTOS

# funcion que fusiona dos subarreglos
def merge(inicio, medio, fin):#inidice de posicion de inicio, medio y final
    
    #Se divide el arreglo original en 2 subarreglos: izquierda y derecha
    arreglo_izquierda = arreglo[inicio:medio + 1]
    arreglo_derecha = arreglo[medio + 1:fin + 1]

    #Se halla el tamaño de ambos subarreglos para poder recorrerlos
    longitud_izquierdo = len(arreglo_izquierda)
    longitud_derecho = len(arreglo_derecha)

    # Índices para recorrer los subarreglos
    indice_actual_izquierda = 0
    indice_actual_derecha = 0
    # Índice actual donde caeran los elementos en orden
    indice_actual_arreglo = inicio

    # Fusionar los subarreglos izquierdo y derecho en orden ascendente
    while indice_actual_izquierda < longitud_izquierdo and indice_actual_derecha < longitud_derecho:
        if arreglo_izquierda[indice_actual_izquierda] <= arreglo_derecha[indice_actual_derecha]:
            arreglo[indice_actual_arreglo] = arreglo_izquierda[indice_actual_izquierda]
            indice_actual_izquierda += 1
        else:
            arreglo[indice_actual_arreglo] = arreglo_derecha[indice_actual_derecha]
            indice_actual_derecha += 1
        indice_actual_arreglo += 1

    # Agregar los elementos restantes del subarreglo izquierdo, si los hay
    while indice_actual_izquierda < longitud_izquierdo:
        arreglo[indice_actual_arreglo] = arreglo_izquierda[indice_actual_izquierda]
        indice_actual_izquierda += 1
        indice_actual_arreglo += 1

    # Agregar los elementos restantes del subarreglo derecho, si los hay
    while indice_actual_derecha < longitud_derecho:
        arreglo[indice_actual_arreglo] = arreglo_derecha[indice_actual_derecha]
        indice_actual_derecha += 1
        indice_actual_arreglo += 1

def merge_sort_secuencial(inicio, fin):
    if inicio < fin:
        # Calcular el punto medio del subarreglo
        medio = inicio + (fin - inicio) // 2
        #Se llama al merge sort secuencial de forma recursiva para ordenar la mitad izquierda del subarreglo
        merge_sort_secuencial(inicio, medio)
        #Se llama al merge sort secuencial de forma recursiva para ordenar la mitad derecha del subarreglo
        merge_sort_secuencial(medio + 1, fin)
        #Se llama para fusionar las dos mitades ordenadas
        merge(inicio, medio, fin)


# Función merge_sort_paralelo utiliza subprocesos
def merge_sort_paralelo(inicio, fin, profundidad):

    #Verifica si hay más de un elemento en el subarreglo
    if inicio < fin:
        if profundidad <= PROFUNDIDAD_MAXIMA:
            medio = inicio + (fin - inicio) // 2 # Calcular el punto medio del subarreglo
            
            #Se crean 2 subprocesos, una por cada parte de la división del arreglo
            
            t1 = threading.Thread(target=merge_sort_paralelo, args=(inicio, medio, profundidad + 1))
            t2 = threading.Thread(target=merge_sort_paralelo, args=(medio + 1, fin, profundidad + 1))

            t1.start()
            t2.start()

            t1.join()
            t2.join()

            # Merge de los subarreglos
            merge(inicio, medio, fin)

if __name__ == '__main__':
    
    for i in range(NUM_ELEMENTOS):
        arreglo[i] = random.randint(-85000, 8500)

    print('El numero de elementos del arreglo es:', NUM_ELEMENTOS)

    print("\n\tAlgoritmo en Secuencial:")
    print("--------------------------------------------------------------------------------")
    print("Se esta ordenando en secuencial...")

    t1 = time.perf_counter()
    merge_sort_secuencial(0, NUM_ELEMENTOS - 1)
    t2 = time.perf_counter()
    ts = t2 - t1

    with open('arreglo_secuencial.txt', 'w') as file:
        file.write("Arreglo ordenado: ")
        file.write(str(arreglo))
        file.write(f"\nTiempo que tarda en ejecutarse el programa secuencialmente es: {ts:.6f} segundos")

    print("Se ha guardado el resultado en: 'arreglo_secuencial.txt'")
    print(f"Tiempo que tarda en ejecutarse el programa secuencialmente es: {ts:.6f} segundos")

    print("\n\tAlgoritmo en Paralelo:")
    print("--------------------------------------------------------------------------------")
    print("Se esta ordenando en paralelo...")

    t3 = time.perf_counter()
    merge_sort_paralelo(0, NUM_ELEMENTOS - 1, 0)
    t4 = time.perf_counter()
    tp = t4 - t3
    
    with open('arreglo_paralelo.txt', 'w') as file:
        file.write("Arreglo ordenado: ")
        file.write(str(arreglo))
        file.write(f"\nTiempo que tarda en ejecutarse el programa paralelamente es: {tp:.6f} segundos")

    print("Se ha guardado el resultado en: 'arreglo_paralelo.txt'")
    print(f"Tiempo que tarda en ejecutarse el programa paralelamente es: {tp:.6f} segundos")

    print("\n\tMedidas Resultantes")
    print("--------------------------------------------------------------------------------")
    aceleracion = ts / tp
    print(f"La aceleración = {aceleracion:.2f}")

    eficiencia = aceleracion / NUM_CPU
    eficiencia_porcentaje = eficiencia * 100
    print(f"La eficiencia = {eficiencia:.2f}", f"= {eficiencia_porcentaje:.2f}%")