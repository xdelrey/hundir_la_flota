# Hundir la Flota en Python ⚓️

Proyecto en Python inspirado en el clásico juego de **Hundir la Flota** (*Battleship*), creado como ejercicio para practicar lógica, estructuras de datos y control de flujo.

## Características principales

- 🎯 Juego por turnos: jugador vs. máquina.
- 📋 Tableros separados para barcos y disparos.
- 💥 Impactos, hundimientos y detección de ganador.
- 🧪 **Modo demo** para demostrar fácilmente que la máquina puede ganar.

## Modo Demo

Para activar el modo demostración:

- Selecciona el Modo Demo o Modo Normal en el inicio.
- El jugador tendrá solo 2 barcos pequeños.
- El rival usará disparos dirigidos a posiciones fijas para ganar rápidamente.

Ideal para presentaciones o correcciones sin necesidad de jugar la partida completa.

## Estructura del proyecto
```
Hundir la flota/
├── main.py         # script principal para la ejecución del juego
├── utils.py        # lógica del juego (funciones)
├── variables.py    # variables que utiliza el programa
└── README.md
```
## Requisitos

- Python 3.x
- Numpy (`pip install numpy`)

## Cómo ejecutar

```bash
python main.py
