import tkinter as tk
from tkinter import messagebox
import math

# Crear la ventana principal
root = tk.Tk()
root.title("Tic Tac Toe Gamer Edition")

# Dimensiones de la ventana
root.geometry("400x450")

# Colores para un estilo más gamer
COLOR_FONDO = "#1c1c1c"  # Fondo oscuro
COLOR_BOTON_X = "#ff4747"  # Color para el jugador X (rojo)
COLOR_BOTON_O = "#47ff47"  # Color para el jugador O (verde)
COLOR_BOTON_VACIO = "#4a4a4a"  # Botones vacíos (gris oscuro)
COLOR_TEXTO = "#ffffff"  # Texto blanco

# Variables globales
jugador_humano = "X"
jugador_ia = "O"
tablero = [[" " for _ in range(3)] for _ in range(3)]
botones = [[None for _ in range(3)] for _ in range(3)]

# Configurar el color de fondo de la ventana principal
root.configure(bg=COLOR_FONDO)

# Función para verificar si hay un ganador
def verificar_ganador(jugador):
    global tablero
    # Verificar filas, columnas y diagonales
    for fila in range(3):
        if tablero[fila][0] == tablero[fila][1] == tablero[fila][2] == jugador:
            return True
    for col in range(3):
        if tablero[0][col] == tablero[1][col] == tablero[2][col] == jugador:
            return True
    if tablero[0][0] == tablero[1][1] == tablero[2][2] == jugador:
        return True
    if tablero[0][2] == tablero[1][1] == tablero[2][0] == jugador:
        return True
    return False

# Función para verificar si hay un empate
def verificar_empate():
    for fila in tablero:
        if " " in fila:
            return False
    return True

# Función que maneja los clics del jugador humano
def manejar_click(fila, col):
    global tablero
    if tablero[fila][col] == " ":
        tablero[fila][col] = jugador_humano
        botones[fila][col].config(text=jugador_humano, bg=COLOR_BOTON_X)

        # Verificar si el jugador humano ha ganado
        if verificar_ganador(jugador_humano):
            messagebox.showinfo("¡Ganador!", "¡Has ganado!")
            reiniciar_juego()
            return
        
        # Verificar si hay empate
        if verificar_empate():
            messagebox.showinfo("¡Empate!", "¡Es un empate!")
            reiniciar_juego()
            return

        # Turno de la IA
        turno_ia()

# Función para el turno de la IA utilizando el algoritmo Minimax
def turno_ia():
    global tablero
    mejor_puntaje = -math.inf
    mejor_movimiento = None

    for i in range(3):
        for j in range(3):
            if tablero[i][j] == " ":
                tablero[i][j] = jugador_ia
                puntaje = minimax(tablero, 0, False)
                tablero[i][j] = " "
                if puntaje > mejor_puntaje:
                    mejor_puntaje = puntaje
                    mejor_movimiento = (i, j)
    
    fila, col = mejor_movimiento
    tablero[fila][col] = jugador_ia
    botones[fila][col].config(text=jugador_ia, bg=COLOR_BOTON_O)

    # Verificar si la IA ha ganado
    if verificar_ganador(jugador_ia):
        messagebox.showinfo("¡Perdiste!", "¡La IA ha ganado!")
        reiniciar_juego()
        return

    # Verificar si hay empate
    if verificar_empate():
        messagebox.showinfo("¡Empate!", "¡Es un empate!")
        reiniciar_juego()
        return

# Implementación del algoritmo Minimax
def minimax(tablero, profundidad, es_maximizador):
    if verificar_ganador(jugador_ia):
        return 1
    if verificar_ganador(jugador_humano):
        return -1
    if verificar_empate():
        return 0

    if es_maximizador:
        mejor_puntaje = -math.inf
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == " ":
                    tablero[i][j] = jugador_ia
                    puntaje = minimax(tablero, profundidad + 1, False)
                    tablero[i][j] = " "
                    mejor_puntaje = max(mejor_puntaje, puntaje)
        return mejor_puntaje
    else:
        mejor_puntaje = math.inf
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == " ":
                    tablero[i][j] = jugador_humano
                    puntaje = minimax(tablero, profundidad + 1, True)
                    tablero[i][j] = " "
                    mejor_puntaje = min(mejor_puntaje, puntaje)
        return mejor_puntaje

# Función para reiniciar el juego
def reiniciar_juego():
    global tablero
    tablero = [[" " for _ in range(3)] for _ in range(3)]
    
    for i in range(3):
        for j in range(3):
            botones[i][j].config(text=" ", bg=COLOR_BOTON_VACIO)

# Crear los botones de la cuadrícula de 3x3 con estilo gamer
for i in range(3):
    for j in range(3):
        boton = tk.Button(root, text=" ", font=("Arial", 24, "bold"), width=5, height=2,
                          bg=COLOR_BOTON_VACIO, fg=COLOR_TEXTO,
                          command=lambda i=i, j=j: manejar_click(i, j))
        boton.grid(row=i, column=j, padx=5, pady=5)
        botones[i][j] = boton

# Iniciar el bucle de la ventana
root.mainloop()
