# IMPORTAMOS LO NECESARIO
from utils import *
import variables as vr
import time
import random
import copy 

# Activación del Modo Demo
modo_demo = True
modo_demo = input("En qué MODO jugamos? Enter para REAL. Cualquier tecla para DEMO.")

# CREAMOS TABLEROS VACÍOS
#Tablero 1 Jugador (barcos Jugador con disparos Rival)
tablero_barcos_jugador = crear_tablero()

#Tablero 2 Jugador (disparos Jugador y aciertos)
tablero_disparos_jugador = crear_tablero()

#Tablero 1 Rival (barcos Rival con disparos Jugador)
tablero_barcos_rival = crear_tablero()

#Tablero 2 Rival (disparos Rival y aciertos)
tablero_disparos_rival = crear_tablero()



# INICIALIZAMOS JUEGO

# Inicializar los barcos del Jugador en Tablero 1 Jugador (barcos Jugador con disparos Rival)
if modo_demo:
    #barcos_jugador = vr.barcos_demo
    barcos_jugador = [barco.copy() for barco in vr.barcos_demo]
else:
    barcos_jugador = inicializar_barcos()
print("TABLERO BARCOS JUGADOR")
print(dibujar_tablero_con_barcos(tablero_barcos_jugador, barcos_jugador))

# Inicializar los barcos del Rival en Tablero 1 Rival (barcos Rival con disparos Jugador)
# En modo demo, utilizamos barcos fijos (conocidos)
if modo_demo:
    #barcos_rival = vr.barcos_demo
    barcos_rival = [barco.copy() for barco in vr.barcos_demo]
else:
    barcos_rival = inicializar_barcos()
print("TABLERO BARCOS RIVAL")
print(dibujar_tablero_con_barcos(tablero_barcos_rival, barcos_rival))

# Inicializo la lista de impactos para cada jugador
barcos_impactados_por_jugador = [[] for _ in barcos_jugador]
barcos_impactados_por_rival = [[] for _ in barcos_jugador]



# JUGAMOS

# 1. QUIÉN EMPIEZA? DE MOMENTO, EMPIEZA SIEMPRE EL JUGADOR
jugando = True
turno_jugador = True # de momento, siempre empieza el jugador ⌛⌛⌛⌛⌛

# DISPAROS POSIBLES: ALEATORIO O A POSICIONES FIJAS EN MODO DEMO
if modo_demo:
    disparos_posibles_rival = [
        [1, 1], [1, 2], [4, 5], [5, 5]  # para que hundan los barcos de posiciones conocidas
    ]
else:
    disparos_posibles_rival = []
    for i in range(10):
        for j in range(10):
            disparos_posibles_rival.append([i, j])
    # El Rival disaparará en posiciones aleatorias sin repetir,
    # ya que las sacamos una a una de esta lista.
    random.shuffle(disparos_posibles_rival)

# 2. MIENTRAS NO HAYA UN GANADOR, EL JUEGO CONTINUA ⌛⌛⌛⌛⌛
while jugando:

    if turno_jugador:
        # 3. TURNO DEL JUGADOR
        limpiar_pantalla()
        print("\n ▓▓▓▓▓▓▓▓▓▓▓▓ TURNO DEL JUGADOR ▓▓▓▓▓▓▓▓▓▓▓▓\n")

        # 4. Mostrar los tableros de BARCOS     del Jugador y del Rival
        print("TABLERO BARCOS JUGADOR")
        print(tablero_barcos_jugador, "\n")
        print("TABLERO DISPAROS JUGADOR")
        print(tablero_disparos_jugador, "\n")
        print("TABLERO BARCOS RIVAL (como pista ;-) ")
        print(tablero_barcos_rival, "\n")
        print("\n ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n")
        #   4.. DISPARAR Y COMPROBAR SI EL DISPARO ES AGUA O TOCADO, Y SI SE HA HUNDIDO UN BARCO
        tocado, barcos_impactados_por_jugador, ganador = disparar(
            barcos_rival,
            barcos_impactados_por_jugador,
            tablero_barcos_rival,
            tablero_disparos_jugador
            )
        
        #   4.2. MOSTRAR Tablero 2 Jugador (disparos y aciertos de Jugador)
        print("TABLERO DISPAROS JUGADOR")
        print(tablero_disparos_jugador)

        # Comprobar si el Jugador ha ganado
        if ganador:
            print("\033[33m████████████████████████████████████████████████████████████\033[0m")
            print("\033[33m██████████████████████ ¡¡HAS GANADO!! ██████████████████████\033[0m")
            print("\033[33m████████████████████████████████████████████████████████████\033[0m")
            break

        # Si acierta, puede disparar de nuevo (sólo si no ha ganado)
        elif tocado:
            continue  # Repite el turno del jugador
            
        turno_jugador = False  # Cambiar turno a Rival

    else:
        # 3. TURNO DEL RIVAL
        limpiar_pantalla()
        print("\n ░░░░░░░░░░░ TURNO DEL RIVAL ░░░░░░░░░░░\n")
        pensando(2)
        
        #   4.. DISPARO ALEATORIO DEL RIVAL o para MODO DEMO
        if modo_demo:
            tocado, ganador = disparo_demo(
                tablero_barcos_jugador,
                barcos_jugador,
                barcos_impactados_por_rival,
                disparos_posibles_rival
            )
        else:
            tocado, ganador = disparo_aleatorio(
                tablero_barcos_jugador,
                barcos_jugador,
                barcos_impactados_por_rival,
                disparos_posibles_rival
            )
        
        # Comprobar si el Rival ha ganado
        if ganador:
            print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
            print("░░░░░░░░░░░░░░░░░░░░░░ ¡¡HAS PERDIDO!! ░░░░░░░░░░░░░░░░░░░░░░")
            print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
            break

        # Si acierta, puede disparar de nuevo (si no es el ganador)
        elif tocado:
            continue  # Repite el turno del Rival

        # 6. TURNO DEL SIGUIENTE JUGADOR
        turno_jugador = True # Cambiamos de turno