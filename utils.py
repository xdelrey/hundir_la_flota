import numpy as np
import variables as vr
import random
import time
import os
import sys

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pensando(segundos):
    print("...", end='', flush=True)
    time.sleep(segundos/3)
    print(".", end='', flush=True)
    time.sleep(segundos/3)
    print(".")
    time.sleep(segundos/3)

def dibujar():
    print("\033[30m■■■■■■■■■■■\033[0m") # negro
    print("\033[31m■■■■■■■■■■■\033[0m") # rojo
    print("\033[32m■■■■■■■■■■■\033[0m") # verde
    print("\033[33m■■■■■■■■■■■\033[0m") # amarillo
    print("\033[34m■■■■■■■■■■■\033[0m") # azul
    print("\033[35m■■■■■■■■■■■\033[0m") # magenta
    print("\033[36m■■■■■■■■■■■\033[0m") # cian
    print("\033[37m■■■■■■■■■■■\033[0m") # blanco
       
def crear_tablero(x = 10):
    tablero = np.full((x, x), "_")
    return tablero

def validar_casilla_inicial(casilla, eslora, es_vertical, tablero = 10):
    '''
    función que calcula si la casilla inicial es válida para un barco 
    de una longitud y una dirección (vertical/horizontal) dadas
    '''
    if (0 <= casilla[0] <= (tablero - 1)) and (0 <= casilla[1] <= (tablero - 1)):
        if es_vertical:
            if (casilla[0] + eslora - 1) < tablero:
                casilla_valida = True
            else:
                casilla_valida = False
        else:
            if (casilla[1] + eslora - 1) < tablero:
                casilla_valida = True
            else:
                casilla_valida = False
    else:
        print("¡La casilla inicial debe estar dentro del Tablero!")
        casilla_valida = False
    return casilla_valida


def colocar_barco (eslora,tablero = 10):
    '''
    función que recibe la longitud de un barco y la dimensión de un tablero de juego (por defecto 10x10)
    y devuelve una posición válida en la que se coloca el barco en vertical u horizontal, donde el barco no se saldrá del tablero
    '''
    casilla_valida = False
    coordenadas = []

    # obtengo una casilla inicial y una dirección válidas para la longitud del barco
    while not casilla_valida:
        casilla_inicial = np.random.randint(0, tablero, 2) # casilla inicial aleatoria
        direccion = np.random.randint(0,2) # obtengo una dirección (horizontal o vertical) aleatoriamente
        # 0: horizontal, 1: vertical
        casilla_valida = validar_casilla_inicial(casilla_inicial, eslora, bool(direccion))
    
    # convierto la casilla inicial en la primera casilla del barco a colocar
    coordenadas.append(casilla_inicial)
    
    # calculo la localización del barco en el tablero
    fila_sgte = coordenadas[0][0]
    columna_sgte = coordenadas[0][1]
    
    for i in range(1, eslora): #desde 1 hasta eslora-1
        if direccion: #direccion = 1, es vertical
            fila_sgte = fila_sgte + 1 # Vertical, Aumentamos la fila
        else: # direccion = 0, es horizontal
            columna_sgte = columna_sgte + 1 # Horizontal, Aumentamos la columna
        celda_siguiente = [fila_sgte, columna_sgte]
        coordenadas.append(celda_siguiente)

    barco_colocado = np.array(coordenadas) # convierto la lista en un array de numpy

    return barco_colocado

def colisiona(barco_actual, otros_barcos):
    '''
    función que comprueba si un barco colisiona con los barcos existentes 
    para un jugador
    '''
    for barco in otros_barcos: # para cada uno de los otros barcos
        for coordenadas_otro_barco in barco: # para cada pareja de coordenadas x,y del otro barco
            for coordenadas_barco_actual in barco_actual: # comprobar si coincide con las coordenadas del barco actual
                if (coordenadas_otro_barco[0] == coordenadas_barco_actual[0]) and (coordenadas_otro_barco[1] == coordenadas_barco_actual[1]):
                    return True
    return False

def inicializar_barcos():
    barcos = []
    for num_barcos, eslora in vr.barcos_eslora:
        for _ in range(num_barcos):
            barco_colisiona = False
            while not barco_colisiona:
                barco = colocar_barco(eslora)
                if not colisiona(barco, barcos):
                    barcos.append(barco)
                    barco_colisiona = True
    return barcos

def dibujar_barco(barco, tablero):
    for x, y in barco:
        tablero[x, y] = 'O'
    return tablero

def dibujar_tablero_con_barcos(tablero_barcos, barcos):
    for barco in barcos:
        tablero_barcos = dibujar_barco(barco, tablero_barcos)
    return tablero_barcos

def actualizar_impactos(disparo, barcos_jugador, barcos_impactados):
    #disparo es un array de [x,y], barcos es un array de [[[x,y],[w,z]],...]
    for i, barco in enumerate(barcos_jugador): # para cada barco del jugador
        if disparo in barco: # si las coordenadas del disparo coinciden
            if disparo not in barcos_impactados[i]: # si no está en barcos_impactados
                barcos_impactados[i].append(disparo) # añade las coordenadas a barcos_impactados
            break
    return barcos_impactados

def comprobar_hundido_y_ganador(barcos_jugador, barcos_impactados):
    todos_hundidos = True
    for i in range(len(barcos_jugador)): # para cada barco del jugador
        barco = barcos_jugador[i]
        impactos = barcos_impactados[i]

        if "_hundido" in impactos: # si ya está marcado como hundido, pasamos del barco
            continue
        
        if all(tuple(pos) in map(tuple,impactos) for pos in barco): # comprobamos que todas las casillas del barco estén impactadas
            print("\033[36m■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■\033[0m")
            print("\033[36m■■■■■■■■■■■ H U N D I D O ■■■■■■■■■■■\033[0m") # si hay alguno
            print("\033[36m■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■\033[0m")
            time.sleep(2)  # espera 2 segundos antes de continuar para que el usuario vea el mensaje
            impactos.append("_hundido") # añadimos el marcador

        else:
            todos_hundidos = False # si el barco no está aún hundido 

    return todos_hundidos

def disparar(
        barcos_objetivo,
        barcos_impactados, 
        tablero_barcos_rival, 
        tablero_disparos_jugador):
    '''
    función que recibe Tablero Barcos Rival y Tablero Disparos Jugador,
    pide las coordenadas a las que disparar y actualiza los tableros según el disparo.
    actualiza también si los barcos se están hundiendo
    '''
    
    while True:
        try:
            # Pido las coordenadas a las que disparar
            fila = int(input("Introduce la fila: "))
            columna = int(input("Introduce la columna: "))
            
            # Compruebo que están dentro del tablero
            if 0 <= fila < len(tablero_barcos_rival) and 0 <= columna < len(tablero_barcos_rival[0]):
                break
            else:
                print("Las coordenadas deben estar entre 0 y 9.")
        except ValueError:
            print("Introduce un número válido.")

    disparo = [fila, columna]
    coordenadas = tablero_barcos_rival[fila][columna]
    
    # Actualizo los tableros de disparos del jugador y de barcos del rival
    if coordenadas in ('O', 'X'):
        tablero_barcos_rival[fila][columna] = "X"  # Tocado o ya disparado
        tablero_disparos_jugador[fila][columna] = "X"
        tocado = True
        
        # actualizar barcos_impactados
        barcos_impactados = actualizar_impactos(disparo, barcos_objetivo, barcos_impactados)
        
    elif coordenadas in ("_", 'A'):
        tablero_barcos_rival[fila][columna] = "A"  # Agua o ya fallado
        tablero_disparos_jugador[fila][columna] = "A"
        tocado = False

    ganador = comprobar_hundido_y_ganador(barcos_objetivo, barcos_impactados)

    return tocado, barcos_impactados, ganador

# Función para disparo aleatorio del rival
def disparo_aleatorio(tablero, barcos_jugador, barcos_impactados, disparos_posibles):
    if not disparos_posibles:
        print("El rival se ha quedado sin disparos posibles.")
        return False, False # para cuando no queden disparos posibles (y no entre en bucle infinito)

    while True:
        fila, columna = disparos_posibles.pop()  # Usamos y eliminamos la siguiente posición
        
        disparo = [fila, columna]
        
        # Si es un barco (O), se marca como tocado (X)
        if tablero[fila][columna] == 'O':
            tablero[fila][columna] = 'X'
            barcos_impactados = actualizar_impactos(disparo, barcos_jugador, barcos_impactados)
            ganador = comprobar_hundido_y_ganador(barcos_jugador, barcos_impactados)
            return True, ganador
        else:  # Si es agua (_), se marca como fallado (A)
            tablero[fila][columna] = 'A'
            return False, False
        
# Para el MODO DEMO: Función para disparos guiados del rival
def disparo_demo(tablero, barcos_jugador, barcos_impactados, disparos_posibles):
    if not disparos_posibles:
        print("El rival se ha quedado sin disparos posibles.")
        return False, False # para cuando no queden disparos posibles (y no entre en bucle infinito)

    fila, columna = disparos_posibles.pop(0)
    disparo = [fila, columna]

    if tablero[fila][columna] == 'O':
        tablero[fila][columna] = 'X'
        barcos_impactados = actualizar_impactos(disparo, barcos_jugador, barcos_impactados)
        # 4. Mostrar los tableros de BARCOS del Jugador y del Rival
        print("TABLERO BARCOS JUGADOR")
        print(tablero)
        pensando(1)
        ganador = comprobar_hundido_y_ganador(barcos_jugador, barcos_impactados)
        return True, ganador
    else:
        tablero[fila][columna] = 'A'
        return False, False

