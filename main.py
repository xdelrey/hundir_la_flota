from utils import *
import variables as vr


# ------------- CREAMOS TABLEROS VACÍOS ------------- #

#Tablero 1 Jugador (barcos Jug con disparos Rival)
tablero_barcos_jugador = crear_tablero()

#Tablero 2 Jugador (disparos Jug)
tablero_disparos_jugador = crear_tablero()

#Tablero 1 Rival (barcos Rival con disparos Jug)
tablero_barcos_rival = crear_tablero()

#Tablero 2 Rival (disparos Rival)
tablero_disparos_rival = crear_tablero()


# ------------- COLOCAMOS LOS BARCOS DE CADA JUGADOR  ------------- #

barcos_jugador = inicializar_barcos()
print("TABLERO BARCOS JUGADOR")
print(dibujar_tablero_con_barcos(tablero_barcos_jugador, barcos_jugador))

barcos_rival = inicializar_barcos()
print("TABLERO BARCOS RIVAL")
print(dibujar_tablero_con_barcos(tablero_barcos_rival, barcos_rival))