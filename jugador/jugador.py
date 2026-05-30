from clave import Contraseña
from cofre import AbrirCofre
from ajedrez import Tablero
from ajedrez import Caballo
from ajedrez import GEMA
from ajedrez import VISITADO_GEMA
from math import floor
from math import ceil
import csv
import random
from datetime import datetime

# clase para gestionar los valores de juego
class JuegoCazador:
    animacion = 0
    cofre = None

    def __init__(self, longitud=8):
        # propiedad privada 
        # guarda los niveles recorridos
        self._nivel = 0
        # propiedad privada 
        # total de cofres
        self.totales = {}
        # propiedad privada 
        # el puntaje es 0 al iniciar
        self._puntaje = 0
        # valores al inicio de cada nivel
        self.valores_iniciales()
        # instancia para puntuar claves
        self.cofres = AbrirCofre()
        # instancia para generar claves
        self.contraseña = Contraseña()
        self.contraseña.fijar_longitud(longitud=longitud)

    def pasar_nivel(self):
        """Cambiar la cuenta de nivel"""
        self._nivel = self._nivel + 1

    def valores_iniciales(self):
        """Valores para inicio de nivel"""
        # permitir movimiento
        self.bloqueado = False
        # propiedad privada 
        # total de caidas en embrujos
        self._cuenta_embrujos = 0
        # propiedad privada 
        # total de saltos realizados
        self._saltos = 0
        # propiedad privada 
        # tiempo transcurrido medido en enteros
        self._tiempo = 0
        # propiedad privada 
        # si ha recogido la gema
        self._bono_gema = 0
    
    def marcar_tiempo(self, cambio=1):
        """Marcar un ciclo de tiempo para la jugada"""
        self._tiempo += cambio

    def ver_puntaje(self):
        """Devolver el puntaje"""
        return self._puntaje

    def ver_bono_gema(self):
        """Devolver el estado del bono de gema"""
        return self._bono_gema

    def obtener_bono_gema(self):
        """Obtener gema"""
        # las gemas dan un grupo de caracteres pero
        # solo hay cuatro solo puede tomar cuatro
        self._bono_gema = min(4, self._bono_gema + 1)

    def ver_bono_saltos(self, caballo):
        """Devolver el valor del bono de saltos"""
        # hay un bono de saltos si los saltos
        # realizados son menos que los que realizó
        # el computador
        return  self._saltos <= caballo.tope

    def ver_bono_tiempo(self, caballo):
        """Devolver el valor del bono de tiempo"""
        # el bono del tiempo es la diferencia entre la
        # cantidad de movimientos requeridos por el pc
        # y los 'tics' de reloj
        return max(0, floor(caballo.tope - self._tiempo))

    def ver_embrujo(self):
        """Mostrar embrujos encontrados"""
        # la cuentra de cuantos embrujos encontró
        return self._cuenta_embrujos

    def obtener_embrujo(self):
        """Agregar un embrujo"""
        # la cuenta aumenta uno por cada embrujo encontrado
        self._cuenta_embrujos = self._cuenta_embrujos + 1
        return self._cuenta_embrujos

    def abrir_cofre(self, cofre):
        """Agregar el puntaje del cofre al jugador"""
        # inicializar total por tipo
        if self.totales.get(cofre.tipo) is None:
            self.totales[cofre.tipo] = 0
        # contar total
        self.totales[cofre.tipo] = self.totales[cofre.tipo] + 1
        self._puntaje = self._puntaje + cofre.puntos

    def generar_contraseña_bonos(self, caballo):
        """Genera una contraseña según los bonos
        que adquirió durante el juego.
        La gema mantiene al menos dos categorías de caracter.
        El bono de tiempo agrega caracteres a la contraseña.
        El bono de saltos evita caracteres repetidos
        Las penalidades de embrujo 
            >= 3 usar a lo mucho 3 grupos de caracteres
            >= 5 usar solo un grupo de caracteres
            >= 6 forzar repetidos
            + pierde un caracter por cada 3 embrujos
        """
        # cuantos grupos de caracteres evitar
        # se elige al azar un número entre
        # minimo
        excluir = [0, 1, 2, 3]
        # si hay bono gema -- excluir preferentemente pocos
        if self.ver_bono_gema() >= 0:
            # agregar una posibilidad de usar todos los grupos por cada gema
            excluir.extend([0 for x in range(0, self.ver_bono_gema())])
        # si hay tres o mas embrujos excluir tres
        if self._cuenta_embrujos >= 3:
            excluir.append(3)
        # si hay cinco o más usar solo una clase de caracter
        if self._cuenta_embrujos >= 5:
            excluir.extend([3 for x in range(4, self._cuenta_embrujos)])
            
        # elegir al azar cuántos excluir 
        largo = random.choice(excluir)
        # listar los grupos
        els = [el for el in Contraseña.grupos]
        # excluir la cantidad que se debe excluir
        for el in range(0, largo):
            # elegir al azar cuál excluir
            pos = random.randint(0, len(els) - 1)
            g = els.pop(pos)

        # calcular la penalidad de caracteres por embrujos
        penalidad_embrujo = ceil(self._cuenta_embrujos / 3)
        # calcular la longitud de la contraseña
        self.contraseña.fijar_longitud(8 + self.ver_bono_tiempo(caballo=caballo) - penalidad_embrujo)
        # generarla con las condiciones dadas
        return self.contraseña.generar_contraseña(
            els, 
            permitir_repetidos=self.ver_bono_saltos(caballo=caballo) and self._cuenta_embrujos > 5, 
            forzar_repetidos=self._cuenta_embrujos >= 6
        )
    
    # para pruebas
    # genera una contraseña con condiciones aleatorias
    def generar_contraseña_variable(self):
        largo = random.randint(0, 3)
        els = [el for el in Contraseña.grupos]
        for el in range(0, largo):
            pos = random.randint(0, len(els) - 1)
            g = els.pop(pos)
        return self.contraseña.generar_contraseña(els, permitir_repetidos=random.choice([True, False]))

    ## para pruebas
    # genera una serie de pasos para validad contraseñas
    def prueba_ciclo(self):
        clave = self.generar_contraseña_variable()
        print(clave)
        puntos = self.contraseña.puntuar_contraseña(clave)
        print(f"puntos {puntos}")
        cofre = self.cofres.dar_cofre(puntos=puntos)
        print(cofre.tipo)
        print(cofre.puntos)
        self.abrir_cofre(cofre)
        print(self._puntaje)
    
    # inicia una ronda
    def iniciar_ronda(self):
        """Inicializa los valores para un nivel"""
        # genera un tablero vacío
        tablero = Tablero()
        # posiciona el caballo al azar en el punto inicial
        caballo = Caballo.posicionar_al_azar(tablero)
        # posiciona al jugador en la posicion inicial del computador
        self._fila = caballo.fila
        # posiciona al jugador en la posicion inicial del computador
        self._col = caballo.col
        # marca la primera posición como visitada
        tablero.marcar_visitado(caballo.fila, caballo.col)
        # inicia los valores iniciales
        self.valores_iniciales()
        # devuelve el caballo (la ruta realizada por el pc)
        return caballo

    def trazar_ruta(self, caballo, min_saltos=5, max_saltos=None, total_bloquear=None, total_embrujar=None, total_gemas=None):
        """Genera los obstáculos para el nivel"""
        n_saltos = random.randint(min_saltos, max_saltos)
        # genera una ruta aleatoria
        caballo.marcar_ruta(total_saltos=n_saltos, num_gemas=total_gemas)
        # si no se envía cuántos bloquear lo determina aleatoriamente
        if total_bloquear is None:
            total_bloquear = floor(random.uniform(0, .75 * caballo.tablero.ancho * caballo.tablero.alto))
        # bloquea campos entre los no requeridos por la ruta
        caballo.tablero.bloquear(total_bloquear, evitar=[caballo.tablero.fila_col_a_pos(fila, col) for fila, col in caballo.historia])
        # embruja los campos no requeridos por la ruta
        caballo.tablero.embrujar(total_embrujar, evitar=[caballo.tablero.fila_col_a_pos(fila, col) for fila, col in caballo.historia])

    def esta_en(self, fila, col):
        """Revisar la posición del jugador respecto a la fila y columna dadas"""
        return self._fila == fila and self._col == col
    
    def saltar_a(self, tablero, fila, col):
        """Realizar una movida"""
        # obtener movimientos válidos
        saltos = Caballo.ver_saltos_desde(tablero, self._fila, self._col)
        # si el movimiento es válido
        if (fila, col) in saltos:
            # actualizar la posición del jugador
            self._fila = fila
            self._col = col
            # marcar el campo actual como visitado
            tablero.marcar_visitado(fila, col)
            # contar el salto dado
            self._saltos = self._saltos + 1
            # terminar
            return 
        else:
            # informar del error
            raise Exception("No se puede saltar ahí")

    def guardar_resultados(self, caballo, total_a_bloquear=None, total_a_embrujar=None):
        columnas = ['fecha', 'nivel', 'inicio', 'final', 'total_a_bloquear', 'total_a_embrujar', 
        'total_gemas', 'gemas', 'contraseña', 
        'cofre_maldito', 'cofre_comun', 'cofre_raro', 'cofre_legendario', 'puntaje']
        try:
            # intentar leerlo
            with open('results.log', 'r', encoding='utf-8') as data_file:
                pass
        except:
            # si no existe generar cabeceras
            with open('results.log', 'a', encoding='utf-8') as data_file:
                csv_writer = csv.DictWriter(data_file, fieldnames=columnas, lineterminator="\n")
                # generar titulos de columna
                csv_writer.writeheader()
                pass
        with open('results.log', 'a', encoding='utf-8') as data_file:
            csv_writer = csv.DictWriter(data_file, fieldnames=columnas, lineterminator="\n")
            csv_writer.writerow({
                'fecha': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                'nivel': self._nivel,
                'inicio': str(caballo.historia[0]),
                'final': str(caballo.historia[0]),
                'total_a_bloquear': floor(total_a_bloquear),
                'total_a_embrujar': floor(total_a_embrujar),
                'total_gemas': len([x for x in caballo.tablero if x == GEMA]),
                'gemas': self.ver_bono_gema(),
                'contraseña': self.cofre.contraseña,
                'cofre_maldito': self.totales.get(AbrirCofre.nombre_cofre_maldito(), 0),
                'cofre_comun': self.totales.get(AbrirCofre.nombre_cofre_comun(), 0),
                'cofre_raro': self.totales.get(AbrirCofre.nombre_cofre_raro(), 0),
                'cofre_legendario': self.totales.get(AbrirCofre.nombre_cofre_legendario(), 0),
                'puntaje': self._puntaje,
            })

