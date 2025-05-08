import numpy as np
import variables as vr

def crear_tablero(x = 10):
    tablero = np.full((x, x), "_")
    return tablero

'''
########## NO NOS HACE FALTA ESTA FUNCIÓN ##############
def crear_barco(eslora):
    barco = np.full(eslora, "O")
    return (barco)
########## NO NOS HACE FALTA ESTA FUNCIÓN ##############
'''

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

'''
########## NO NOS HACE FALTA ESTA FUNCIÓN ##############
def crear_todos_los_barcos (lista_barcos_eslora):
    todos_los_barcos = []

    for num_barcos, eslora in lista_barcos_eslora:
        for _ in range(num_barcos):
            barco = colocar_barco(eslora)
            todos_los_barcos.append(barco)
    
    return todos_los_barcos
########## NO NOS HACE FALTA ESTA FUNCIÓN ##############
'''

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

'''
def disparar(casilla,tablero):
    if tablero[casilla] in ('O', 'X'):
        tablero[casilla] = "X"
    elif tablero[casilla] in ("_", 'A'):
        tablero[casilla] = "A"
    return tablero
'''

def disparar(tablero):
    '''
    función que recibe el tablero de un jugador,
    pide una casilla (coordenadas x, y) y actualiza el tablero según el disparo.
    '''
    while True:
        try:
            fila = int(input("Introduce la fila: "))
            columna = int(input("Introduce la columna: "))
            
            # Compruebo que están dentro del rango del tablero
            if 0 <= fila < len(tablero) and 0 <= columna < len(tablero[0]):
                break
            else:
                print("Las coordenadas deben estar entre 0 y 9.")
        except ValueError:
            print("Introduce un número válido.")

    coordenadas = tablero[fila][columna]

    if coordenadas in ('O', 'X'):
        tablero[fila][columna] = "X"  # Tocado o ya disparado
    elif coordenadas in ("_", 'A'):
        tablero[fila][columna] = "A"  # Agua o ya fallado
    
    return tablero