# importar modulo para interfaz grafica
import tkinter as tk
from tkinter import ttk
from tkinter import font
# importar operaciones matemáticas
from math import floor
from math import ceil
# importar procesos aleatorios
#     entero aleatorio
from random import randint
#     mezclar listas
from random import shuffle
#     elegir uno de una lista
from random import choice
# importar modulo juego
from jugador import JuegoCazador
from ajedrez import EMBRUJADO
from ajedrez import BLOQUEADO
from ajedrez import VACIO
from ajedrez import VISITADO
from ajedrez import GEMA
import threading

# tiempo de espera por "tic" de reloj
TIC_INTERVALO_MS = 2000
# actualizaciones a progreso por "tic"
TIC_CUADROS = 10
# generar jugador
jugador = JuegoCazador()
# variable global para caballo
caballo = None
# variable global para etiqueta de password
label_for_passwd = None
# variable global para botón de cofre
boton_abrir_cofre = None
# total de campos a bloquear
total_a_bloquear = 0
# total de campos a embrujar
total_a_embrujar = 0
# variable global para botón de cambio nivel 
boton_siguiente = None
# variable global para botón de reiniciar nivel
boton_reiniciar = None
# variable global para temporizador
progress_bar = None
# mensajes para ruido visual
mensajes = ["¡BU3N_SA1TO!", "¡JOP JOP?", "¡SÓLO UNO MÁS!", "¿AQUÍ?", "BARRAGE, BARRAGE", "KNOCK KNOCK", "WHO IS IT?", 
    "IT'S WILL", "WILL WHO", "WILL YOU?", "IT'S BILL", "BILL BURR-DEN YOU", "[NEIGH]",
    "SOMETIME", "ANYTIME NOW", "I NEED A COFFEE"]

# iniciar interfaz
root = tk.Tk()
# definit titulo de ventana
root.title('Juego Contraseñas')
# definir el tamaño de la ventana
root.geometry('340x480')
# no cambiar tamaño
root.resizable(False, False)
# definir icono de aplicacion
root.iconbitmap('./assets/chess_knight_icon_199399.ico')
# definir fuente para campo contraseña
custom_font = font.Font(family="Courier New", size=12, weight="bold")

# cargar imágenes
# imagen de campo bloqueado
img_bloqueado = tk.PhotoImage(file='assets/bloqueado.png')
# imagen de caballo
img_caballo = tk.PhotoImage(file='assets/caballo.png')
# imagen de campo embrujado
img_bill_burr = tk.PhotoImage(file='assets/bill_burr.png')
# imagen de punto inicial
img_inicio = tk.PhotoImage(file='assets/inicio.png')
# imagen de campo libre
img_libre = tk.PhotoImage(file='assets/libre.png')
# imagen de campo visitado
img_visitado = tk.PhotoImage(file='assets/visitado.png')
# imagen de campo indefinido
img_indefinido = tk.PhotoImage(file='assets/indefinido.png')
# imagen de meta
img_cofre = tk.PhotoImage(file='assets/cofre.png')
# imagen de campo gema
img_gema = tk.PhotoImage(file='assets/gema.png')
# imagen de boton "abrir cofre"
img_abrir = tk.PhotoImage(file='assets/abrir.png')

# accion de campo siguiente
def siguiente():
    """Cambiar al siguiente nivel"""
    # usar el caballo global
    global caballo
    # contar puntos a jugador
    # usar el campo total a bloquear global
    global total_a_bloquear
    # usar el campo total a bloquear global
    global total_a_embrujar
    jugador.pasar_nivel()
    if JuegoCazador.cofre:
        # sumar puntaje y cofres
        jugador.abrir_cofre(JuegoCazador.cofre)
        # generar archivo
        try:
            threading.Thread(
                target=lambda: jugador.guardar_resultados(caballo=caballo, total_a_embrujar=total_a_embrujar, total_a_bloquear=total_a_bloquear)
            )
        except:
            mostrar_mensaje_animado("Fallo registro puntaje")
        # quitar cofre
        JuegoCazador.cofre = None
    # usar el boton siguiente global
    global boton_siguiente
    # bono aleatorio de gemas
    dado_gemas = randint(0, 100)
    if dado_gemas < 90:
        total_gemas = 1
    elif dado_gemas < 99:
        total_gemas = 2
    else:
        total_gemas = 3
    # variacion aleatoria de saltos
    dado_saltos = randint(0, 100)
    if dado_saltos < 80:
        max_saltos = 15
    elif dado_saltos < 96:
        max_saltos = 20
    else:
        max_saltos = 10
    # aumentar los campos a bloquear en uno por cada dos niveles
    total_a_bloquear = total_a_bloquear + .5
    # aunmentar los campos a embrujar en uno por cada tres niveles aprox
    total_a_embrujar = total_a_embrujar + 0.4
    # iniciar la ronda de juego y obtener el caballo
    caballo = jugador.iniciar_ronda()
    # generar el reto
    jugador.trazar_ruta(
        caballo, 
        max_saltos=max_saltos,
        total_bloquear=floor(total_a_bloquear), 
        total_embrujar=floor(total_a_embrujar),
        total_gemas=total_gemas
    )
    # dibujar el contenido de la ventana
    dibujar_ventana()
    # mostrar un mensaje
    mostrar_mensaje_animado("¡Buena suerte!")

def reiniciar():
    """Reiniciar el nivel"""
    # usar la barra de progreso general
    global progress_bar
    # eliminarla para detener el cronómetro
    progress_bar = None
    # poner valores iniciales de jugador
    jugador.valores_iniciales()
    # devolver al jugador a la posición inicial
    jugador._fila, jugador._col = caballo.historia[0]
    # desmarcar los visitados
    caballo.desmarcar_visitados()
    # dibujar contenido de la ventana
    dibujar_ventana()
    # mostrar un mensaje
    mostrar_mensaje_animado("¡Vamos otra vez!")

def iniciar_tiempo():
    """Iniciar cronómetro para nivel"""
    # utilizar barra de progreso global
    global progress_bar
    # agregar una etiqueta a la barra de progreso
    label = ttk.Label(text="Tiempo:")
    # agregarla en la fila 12
    label.grid(row=12, column=0, columnspan=2, padx=10, pady=10)
    # instanciar una barra de progreso
    # y agregarla en la fila 12
    progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=200)
    progress_bar.grid(row=12, column=2, columnspan=6, padx=10, pady=10)
    #definir la función para el "tic" del reloj
    def update_pg():
        # si se eliminó la barra de progreso ignorar el reloj
        if not progress_bar:
            return
        # agregar un tic al jugador
        jugador.marcar_tiempo(1 / TIC_CUADROS)
        # fijar la posición de la barra del progreso según la razón
        # entre los tics registrados y el tope de movimientos 
        progress_bar['value'] = ceil((jugador._tiempo / (caballo.tope)) * 100)
        # si llegó al tope mostrar que el tiempo se agotó
        if jugador._tiempo >= caballo.tope:
            label_2 = ttk.Label(text="Bono Tiempo Agotado")
            label_2.grid(row=12, column=2, columnspan=6, padx=10, pady=10)
        elif jugador._tiempo < caballo.tope:
            # si no ha llegado al tope programar un tic más en 1300 ms
            root.after(round(TIC_INTERVALO_MS / TIC_CUADROS), update_pg)
    # programar un tic en 300ms
    root.after(10, update_pg)

# accion para botón abrir cofre
# abrir cofre es lo que permite terminar el nivel
def abrir_cofre():
    # redibujar el tablero
    dibujar_ventana()
    # # desactivar el botón de reiniciar nivel
    # boton_reiniciar.state(['disabled'])
    # generar una contraseña con los datos del jugador y del "caballo"
    # (la ruta seguida por el pc)
    contraseña = jugador.generar_contraseña_bonos(caballo=caballo)
    # puntuar la contraseña
    puntos = jugador.contraseña.puntuar_contraseña(contraseña)
    # obtener la instancia del cofre que
    # corresponde a ese puntaje
    cofre = jugador.cofres.dar_cofre(puntos=puntos, contraseña=contraseña)
    # usar el botón generar para abrir cofre
    global boton_abrir_cofre
    # eliminarlo de la vista para evitar más clics
    boton_abrir_cofre.destroy()
    # eliminar referencia 
    boton_abrir_cofre = None
    # **animación de final de nivel**
    # función para mostrar el tipo de cofre obtenido
    def mostrar_evaluacion():
        # agregar una etiqueta para titulo
        label_new_1 = tk.Label(root, text="Cofre abierto", bg="white", fg="green", font=custom_font)
        label_new_1.grid(row=2, column=0, columnspan=8)
        # agregar una etiqueta para tipo cofre
        label_new_2 = tk.Label(root, text=f" * * * {cofre.tipo} * * * ", bg="white", fg="black", font=custom_font)
        label_new_2.grid(row=3, column=0, columnspan=8)
        # agregar una etiqueta para puntos obtenidos
        label_new_3 = tk.Label(root, text=f"puntos: {cofre.puntos}", bg="white", fg="black", font=custom_font)
        label_new_3.grid(row=5, column=0, columnspan=8)
        # habilitar botón para pasar nivel
        boton_siguiente.state(['!disabled'])
        # guardar cofre en clase
        JuegoCazador.cofre = cofre
    # mostrar contraseña generada
    mostrar_mensaje_animado(contraseña)
    # cuando termine esa animación mostrar tipo cofre
    root.after(1000, mostrar_evaluacion)

# función para ejecutar al llegar al cofre
def llego_a_cofre():
    # usar botón abrir cofre global
    global boton_abrir_cofre
    # quitar referencia a progress_bar
    # para interrumpir animación de reloj
    global progress_bar
    progress_bar = None
    # generar botón para abrir cofre
    boton_abrir_cofre = ttk.Button(root, text="Abrir cofre", image=img_abrir, command=abrir_cofre)
    # generar y agregar etiqueta de titulo
    label_new_0 = tk.Label(root, text=f"BONOS", bg="white", fg="green", font=custom_font)
    label_new_0.grid(row=1, column=0, columnspan=8)
    # generar y agregar etiqueta de bono de gema
    label_new_1 = tk.Label(root, text=f"GEMA/ +{jugador.ver_bono_gema()} GRUPO CARACTERES", bg="white", fg="black", font=custom_font)
    label_new_1.grid(row=2, column=0, columnspan=8)
    # generar y agregar etiqueta de bono de saltos
    if jugador.ver_bono_saltos(caballo=caballo):
        label_new_3 = tk.Label(root, text=f"SALTO/ S0LO ÚNICoS", bg="white", fg="black", font=custom_font)
        label_new_3.grid(row=3, column=0, columnspan=8)
    # generar y agregar etiqueta de bono de tiempo
    label_new_4 = tk.Label(root, text=f"TIEMPO/ +{jugador.ver_bono_tiempo(caballo)} caracteres", bg="white", fg="black", font=custom_font)
    label_new_4.grid(row=4, column=0, columnspan=8)
    # generar y agregar etiqueta de penalizacion
    if jugador.ver_embrujo() > 0:
        label_new_5 = tk.Label(root, text=f"PENALIZACION/ {-jugador.ver_embrujo()}", bg="white", fg="red", font=custom_font)
        label_new_5.grid(row=5, column=0, columnspan=8)
    # agregar botó de abrir cofre
    boton_abrir_cofre.grid(row=6, column=0, columnspan=8, rowspan=2, padx=5, pady=5)
    # desahbilitar botón de reiniciar
    boton_reiniciar.state(['disabled'])
    # impedir movimiento
    jugador.bloqueado = True

# hacer clic en campo
def mover_a(fila, col):
    """Devuelve una función que evalúa el movimiento a la fila y columna dadas. 
    Si no se puede mover por estar bloqueado no realiza el movimiento"""
    
    # función mover a una celda particular
    def saltar():
        if jugador.bloqueado:
            return
        # evaluar si es gema (antes de marcarlo como pisado)
        es_gema = caballo.es_gema(fila=fila, col=col)
        # evaluar si es embrujo (antes de marcarlo como pisado)
        es_embrujo = caballo.es_embrujo(fila=fila, col=col)
        try:
            # intentar movimiento
            jugador.saltar_a(caballo.tablero, fila, col)
        except Exception as e:
            # si falla mostrar mensaje
            mostrar_mensaje_animado(str(e))
            return
        # dibujar contenido de la ventana
        dibujar_ventana()
        # iniciar contador de tiempo con el movimiento
        iniciar_tiempo()
        # si es gema
        if es_gema:
            # marcar bono
            jugador.obtener_bono_gema()
            # mostrar mensaje
            mostrar_mensaje_animado("+ BONO GEMA")
        # si es embrujo
        if es_embrujo:
            # contar embrujo
            total_penas = jugador.obtener_embrujo()
            # mostrar embrujo
            mostrar_mensaje_animado(f"+ PENALIZACIÓNES {total_penas}")
        # revisar si llegó al final del nivel
        if jugador.esta_en(fila=caballo.fila, col=caballo.col):
            # mostrar mensaje
            mostrar_mensaje_animado("¡¡¡META ALCANZADA!!!")
            # mostrar resultados nivel
            llego_a_cofre()
        elif not es_gema and not es_embrujo:
            # mostrar mensaje
            mostrar_mensaje_animado(choice(mensajes))
    # devolver la función para la fila y columna dadas
    return saltar

# dibujar el contenido de la ventana
# el tablero, los botones y puntaje
def dibujar_ventana():
    """Dibujar el tablero y los botónes y estadísticas"""
    # eliminar el contenido existente
    # iterar por cada widget
    for widget in root.winfo_children():
        # destruirlo
        widget.destroy()
    # usar la etiqueta para contraseñas
    global label_for_passwd
    # y borrarla para interrumpir las
    # animaciones existentes
    label_for_passwd = None
    # dibujar tablero
    # recorrer todas las celdas posibles
    for i in range(0, 64):
        # obtener fila y columma de posicion
        f = floor(i / 8)
        c = i % 8
        # si el tablero es menor de 8x8 bloquear las celdas que quedan por fuera
        if c >= caballo.tablero.ancho:
            button = ttk.Button(root, text=".", image=img_bloqueado, command=mover_a(f, c))
            button.grid(row=f, column=c, sticky="NW", padx=0, pady=0)
            continue
        if f >= caballo.tablero.alto:
            button = ttk.Button(root, text=".", image=img_bloqueado, command=mover_a(f, c))
            button.grid(row=f, column=c, sticky="NW", padx=0, pady=0)
            continue
        # leer el valor del tablero en la fila y columna dadas
        val = caballo.tablero.leer_valor_en(fila=f, col=c)
        # gemera botónes con imágenes según la situación
        if jugador.esta_en(f, c):
            # --si el jugador está en la celda
            button = ttk.Button(root, text="K", image=img_caballo, command=mover_a(f, c))
        elif caballo.termina_en(f, c):
            # --si la ruta termina en la celda
            button = ttk.Button(root, text="o", image=img_cofre, command=mover_a(f, c))
        elif caballo.inicia_en(f, c) and val != GEMA:
            # --si la ruta inicia en la celda (y no tiene gema)
            button = ttk.Button(root, text="o", image=img_inicio, command=mover_a(f, c))
        elif caballo.inicia_en(f, c) and val == GEMA:
            # --si la ruta inicia en la celda (y tiene gema)
            button = ttk.Button(root, text="W", image=img_gema, command=mover_a(f, c))
        elif val == EMBRUJADO:
            # --si la la celda esta embrujada
            button = ttk.Button(root, text=".", image=img_bill_burr, command=mover_a(f, c))
        elif val == VISITADO:
            # --si la la celda fue visitada
            button = ttk.Button(root, text=".", image=img_visitado, command=mover_a(f, c))
        elif val == BLOQUEADO:
            # --si la la celda esta bloqueada
            button = ttk.Button(root, text="X", image=img_bloqueado, command=mover_a(f, c))
        elif val == VACIO:
            # --si la la celda esta vacía
            button = ttk.Button(root, text=" ", image=img_libre, command=mover_a(f, c))
        elif val == GEMA:
            # --si la la celda contiene una gema
            button = ttk.Button(root, text="W", image=img_gema, command=mover_a(f, c))
        else:
            # --otras situaciones
            button = ttk.Button(root, text="?", image=img_indefinido, command=mover_a(f, c))
        # agrega el botón dado en la fila y columna dadas
        button.grid(row=f, column=c)
    # contador de saltos
    label_1 = tk.Label(root, text=f"SALTOS {jugador._saltos} | LÍMITE {caballo.tope}")
    label_1.grid(row=10, column=0, columnspan=8)
    global boton_reiniciar
    # botón reiniciar
    boton_reiniciar = ttk.Button(root, text="Reiniciar", command=reiniciar)
    boton_reiniciar.grid(row=11, column=0, columnspan=2, padx=5, pady=5)
    global boton_siguiente
    # botón siguiente
    boton_siguiente = ttk.Button(root, text="Siguiente »", command=siguiente)
    boton_siguiente.grid(row=11, column=2, columnspan=2, padx=5, pady=5)
    boton_siguiente.state(['disabled'])
    # botón puntaje
    label_3 = tk.Label(root, text=f"Puntos: {jugador.ver_puntaje()}", font=font.Font(weight="bold"))
    label_3.grid(row=11, column=4, columnspan=4)

    # label_4 = tk.Label(root, text=str(jugador.totales))
    # label_4.grid(row=14, column=0, columnspan=8)

# mostrar un mensaje animado
def mostrar_mensaje_animado(mensaje="Hola", animar=True):
    # iniciar animación
    jugador.animacion = 6
    # usar etiqueta para password general
    global label_for_passwd
    # interrumpir animaciones anteriores
    if label_for_passwd:
        label_for_passwd.destroy()
    # cambiar color para aumentar ruido visual
    # colores oscuros para fondo
    bg = choice(["darkblue", "darkred", "brown", "black"])
    # colores claros para letra
    fg = choice(["lightgray", "yellow", "cian", "pink"])
    # generar espacio para etiqueta vacío
    label_for_passwd = tk.Label(root, text="          ", bg=bg, fg="lightgray", font=custom_font)
    # agregar espacio para etiqueta
    label_for_passwd.grid(row=13, column=0, columnspan=8)
    # caracteres para mostrar
    texto_p = list("ABDEFGHIJKLMNÑOPQRSTUVWXYZabdefghijklmnñopqrstuvwxyz0123456789¿¡?=)(/¨*+-%&$#!.")
    
    # funcion para generar un cuadro de animación
    def cambiar_texto():
        # restar cuadro de animación de fila
        jugador.animacion = jugador.animacion - 1
        # si todavía quedan cuadros
        if jugador.animacion > 0 and animar:
            # mezclar los caracteres posibles
            shuffle(texto_p)
            # elegir los primeros para llenar el largo del mensaje
            label_for_passwd.configure(text="".join(texto_p[0:len(mensaje)]))
            # programar el siguiente cuadro
            root.after(100, cambiar_texto)
        else:
            # si terminó la animación mostrar el mensaje
            label_for_passwd.configure(text=mensaje)
    # iniciar animación
    root.after(10, cambiar_texto)

# cargar el primer nivel
siguiente()
# abrir ventana prinicipal
root.mainloop()

def probar_conversiones():
    tablero = Tablero()
    print(tablero._tablero)
    for el in range(0, 8):
        f = random.randint(0, 8)
        c = random.randint(0, 8)
        p = tablero.fila_col_a_pos(f, c)
        print(">>", p, f, c)
        f, c = tablero.pos_a_fila_col(p)
        print("<<", p, f, c)
        p = tablero.fila_col_a_pos(f, c)
        print(">>", p, f, c)
        f, c = tablero.pos_a_fila_col(p)
        print("<<", p, f, c)
        print(" * * *")
