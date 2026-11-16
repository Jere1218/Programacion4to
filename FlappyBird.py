# Flappy Bird en Python usando tkinter
# tkinter viene incluido con Python, así que no hay que instalar nada extra.

import tkinter as tk
import random

# ---------- 1. CONFIGURACIÓN ----------

ANCHO = 400              # ancho de la ventana
ALTO = 600               # alto de la ventana

GRAVEDAD = 0.35          # cuánto lo tira hacia abajo en cada cuadro
SALTO = -6               # impulso hacia arriba (negativo = sube)

ANCHO_TUBO = 60         # ancho de cada tubo
HUECO = 150             # espacio por donde pasa el pájaro
VELOCIDAD_TUBOS = 2     # cuántos píxeles se mueven los tubos por cuadro

# ---------- 2. VENTANA Y LIENZO ----------

ventana = tk.Tk()
ventana.title("Flappy Bird")
ventana.resizable(False, False)

# El canvas (lienzo) es donde dibujamos todo el juego
canvas = tk.Canvas(ventana, width=ANCHO, height=ALTO, bg="#70c5ce", highlightthickness=0)
canvas.pack()

# ---------- 3. VARIABLES DEL JUEGO ----------

pajaro_x = 80            # posición horizontal del pájaro (no cambia)
pajaro_y = 300           # posición vertical del pájaro
TAMANO = 30              # tamaño de la "caja" del pájaro (para los choques)
velocidad = 0            # velocidad vertical del pájaro

tubos = []               # lista con todos los tubos que hay en pantalla
contador = 0             # sirve para saber cuándo crear un tubo nuevo
puntos = 0
juego_terminado = False


# ---------- 4. FUNCIONES ----------

def reiniciar():
    """Vuelve todo a como estaba al principio."""
    global pajaro_y, velocidad, tubos, contador, puntos, juego_terminado
    pajaro_y = 300
    velocidad = 0
    tubos = []
    contador = 0
    puntos = 0
    juego_terminado = False


def crear_tubo():
    """Crea un tubo nuevo a la derecha con el hueco en una altura al azar."""
    altura_hueco = random.randint(100, 400)
    tubos.append({
        "x": ANCHO,              # arranca en el borde derecho
        "hueco": altura_hueco,   # dónde empieza el hueco
        "pasado": False          # todavía no lo pasamos (para sumar puntos)
    })


def saltar(evento=None):
    """Hace saltar al pájaro. Si perdiste, reinicia el juego."""
    global velocidad
    if juego_terminado:
        reiniciar()
    else:
        velocidad = SALTO


def actualizar():
    """Mueve las cosas y revisa los choques (se ejecuta en cada cuadro)."""
    global pajaro_y, velocidad, tubos, contador, puntos, juego_terminado

    if juego_terminado:
        return   # si perdiste, no se mueve nada

    # El pájaro cae: la gravedad aumenta su velocidad y la velocidad cambia su posición
    velocidad += GRAVEDAD
    pajaro_y += velocidad

    # Cada 90 cuadros creamos un tubo nuevo
    contador += 1
    if contador % 90 == 0:
        crear_tubo()

    # Recorremos todos los tubos
    for tubo in tubos:
        tubo["x"] -= VELOCIDAD_TUBOS   # el tubo se mueve hacia la izquierda

        # ¿Chocó con el tubo?
        toca_en_horizontal = (pajaro_x + TAMANO > tubo["x"] and
                              pajaro_x < tubo["x"] + ANCHO_TUBO)

        esta_en_el_hueco = (pajaro_y > tubo["hueco"] and
                            pajaro_y + TAMANO < tubo["hueco"] + HUECO)

        if toca_en_horizontal and not esta_en_el_hueco:
            juego_terminado = True

        # ¿Pasó el tubo? Entonces suma un punto (una sola vez)
        if not tubo["pasado"] and tubo["x"] + ANCHO_TUBO < pajaro_x:
            tubo["pasado"] = True
            puntos += 1

    # Borramos los tubos que ya salieron de la pantalla
    tubos = [t for t in tubos if t["x"] + ANCHO_TUBO > 0]

    # ¿Chocó con el piso o con el techo?
    if pajaro_y + TAMANO > ALTO or pajaro_y < 0:
        juego_terminado = True


def dibujar_pajaro():
    """Dibuja el pájaro usando óvalos y un triángulo."""
    # Centro del pájaro (punto de referencia para dibujar todo)
    cx = pajaro_x + TAMANO / 2
    cy = pajaro_y + TAMANO / 2

    # Cuerpo: un óvalo amarillo
    canvas.create_oval(cx - 18, cy - 14, cx + 18, cy + 14, fill="#ffd23f", outline="")

    # Ala: si el pájaro sube (velocidad negativa), el ala se dibuja más arriba
    ala_y = cy - 2 if velocidad < 0 else cy + 4
    canvas.create_oval(cx - 14, ala_y - 5, cx + 2, ala_y + 5, fill="#f4a300", outline="")

    # Ojo: círculo blanco con una pupila negra
    canvas.create_oval(cx + 3, cy - 10, cx + 13, cy, fill="white", outline="")
    canvas.create_oval(cx + 8, cy - 8, cx + 12, cy - 4, fill="black", outline="")

    # Pico: un triángulo naranja (3 puntos: arriba, punta, abajo)
    canvas.create_polygon(cx + 15, cy - 1, cx + 26, cy + 3, cx + 15, cy + 7,
                          fill="#ff6b2c", outline="")


def dibujar():
    """Dibuja todo en pantalla (se ejecuta en cada cuadro)."""
    # Borramos el cuadro anterior
    canvas.delete("all")

    # Dibujamos los tubos (verdes)
    for tubo in tubos:
        # Tubo de arriba: desde el techo hasta donde empieza el hueco
        canvas.create_rectangle(tubo["x"], 0, tubo["x"] + ANCHO_TUBO, tubo["hueco"],
                                fill="#2e9e44", outline="")
        # Tubo de abajo: desde donde termina el hueco hasta el piso
        canvas.create_rectangle(tubo["x"], tubo["hueco"] + HUECO, tubo["x"] + ANCHO_TUBO, ALTO,
                                fill="#2e9e44", outline="")

    # Dibujamos el pájaro
    dibujar_pajaro()

    # Dibujamos el puntaje
    canvas.create_text(ANCHO / 2, 60, text=str(puntos), fill="white",
                       font=("Arial", 36, "bold"))

    # Si perdiste, mostramos un mensaje
    if juego_terminado:
        # Rectángulo oscuro semitransparente (el stipple simula la transparencia)
        canvas.create_rectangle(0, 0, ANCHO, ALTO, fill="black", stipple="gray50")
        canvas.create_text(ANCHO / 2, 270, text="Perdiste", fill="white",
                           font=("Arial", 40, "bold"))
        canvas.create_text(ANCHO / 2, 310, text="Puntos: " + str(puntos), fill="white",
                           font=("Arial", 20))
        canvas.create_text(ANCHO / 2, 350, text="Tocá o apretá espacio para reiniciar",
                           fill="white", font=("Arial", 14))


def bucle():
    """El bucle del juego: actualiza, dibuja y se vuelve a llamar solo."""
    actualizar()
    dibujar()
    ventana.after(16, bucle)   # espera 16 milisegundos (unos 60 cuadros por segundo)


# ---------- 5. CONTROLES ----------

ventana.bind("<space>", saltar)        # barra espaciadora
canvas.bind("<Button-1>", saltar)      # click del mouse

# ---------- 6. ARRANQUE ----------

bucle()
ventana.mainloop()   # mantiene la ventana abierta