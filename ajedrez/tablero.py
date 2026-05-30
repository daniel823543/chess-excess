from math import ceil
from math import floor
import random

# valores posibles para el tablero
# campos que penalizan
EMBRUJADO = -2
# campos que no se pueden usar
BLOQUEADO = -1
# campos disponibles
VACIO = 0
# campos visitados
VISITADO = 1
# campos con gemas
GEMA = 2
# campos visitados que estaban embrujados
VISITADO_EMBRUJADO = 3
# campos visitados que tenían gema
VISITADO_GEMA = 4

# el tablero guarda información sobre el tablero
class Tablero:

    def __init__(self, alto=8, ancho=8):
        # el alto y ancho son configurables
        self.alto = alto
        self.ancho = ancho
        # inicialmente todas las celdas están vacías
        self._tablero = [VACIO for el in range(0, alto * ancho)]

    def bloquear(self, total=0, evitar=None):
        """repartir aleatoriamente obstáculos en el tablero
        total: el número de obstaculos
        evitar: celdas que deben permanecer libres"""
        # iniciar listado de campos a bloquear
        campos = []
        max_stop = 1000
        # iniciar un bucle hasta tener el total requerido
        while len(campos) < total and max_stop > 0:
            max_stop = max_stop - 1
            # obtener una posicion aleatoria en el tablero
            pos = random.randint(0, self.alto * self.ancho - 1)
            # si está en los que debe evitar no hacer nada
            if pos in evitar:
                continue
            # si ya está en los que se bloquearon no hacer nada
            if pos in campos:
                continue
            # si pasó los chequeos anteriores agregarlo a los bloqueados
            campos.append(pos)
        # recorrer los campos bloqueados
        for el in campos:
            # marcar como bloqueado
            self._tablero[el] = BLOQUEADO
    
    def embrujar(self, total=0, evitar=None):
        """ repartir aleatoriamente campos embrujados en el tablero
        total: el número de obstaculos
        evitar: celdas que deben permanecer libres """
        # iniciar listado de campos a bloquear
        campos = []
        max_stop = 1000
        # iniciar un bucle hasta tener el total requerido
        while len(campos) < total and max_stop > 0:
            max_stop = max_stop - 1
            # obtener una posicion aleatoria en el tablero
            pos = random.randint(0, self.alto * self.ancho - 1)
            # si está en los que debe evitar no hacer nada
            if pos in evitar:
                continue
            # si ya está en los que se bloquearon no hacer nada
            if self._tablero[pos] != VACIO:
                continue
            # si ya está en los que se embrujaron no hacer nada
            if pos in campos:
                continue
            # si pasó los chequeos anteriores agregarlo a los embrujados
            campos.append(pos)
        # recorrer los campos embrujados
        for el in campos:
            # marcar como embrujado
            self._tablero[el] = EMBRUJADO

    # marcar campos como visitados
    def marcar_visitado(self, fila=None, col=None, pos=None):
        """Marcar un campo dado como visitado. Puede indicarse
        la posición por el índice en el tablero o con
        la fila y la columna"""
        # si el valor que hay en la celda dada es vacio
        if self.leer_valor_en(fila=fila, col=col, pos=pos) == VACIO:
            # marcar  como visitados
            self.fijar_valor_en(fila=fila, col=col, pos=pos, valor=VISITADO)
        elif self.leer_valor_en(fila=fila, col=col, pos=pos) == EMBRUJADO:
            # marcar son visitados & embrujados si son embrujados
            self.fijar_valor_en(fila=fila, col=col, pos=pos, valor=VISITADO_EMBRUJADO)
        elif self.leer_valor_en(fila=fila, col=col, pos=pos) == GEMA:
            # marcar como visitados & gema si tienen gema
            self.fijar_valor_en(fila=fila, col=col, pos=pos, valor=VISITADO_GEMA)

    def poner_gema_en(self, fila=None, col=None, pos=None):
        """Fijar en el tablero la presencia de una gema"""
        if pos is not None:
            # si recibe el índice en el tablero lo usa
            fila, col = self.pos_a_fila_col(pos=pos)

        # si recibe filas y columnas usa esos valores 
        # para poner una gema
        self.fijar_valor_en(fila=fila, col=col, valor=GEMA)
    
    def quitar_visitados(self):
        """Remover el estatus de visitado de todos los campos
        libres para salto"""
        for el, val in enumerate(self._tablero):
            if self._tablero[el] == VISITADO:
                # reiniciar los valores los visitados como vacíos
                self._tablero[el] = VACIO
            elif self._tablero[el] == VISITADO_EMBRUJADO:
                # reiniciar los valores los visitados&embrujados como embrujadps
                self._tablero[el] = EMBRUJADO
            elif self._tablero[el] == VISITADO_GEMA:
                # reiniciar los valores los visitados&gema como gema
                self._tablero[el] = GEMA

    def __iter__(self):
        # permitir iterar sobre el tablero directamente
        return enumerate(self._tablero)
    
    # convertir un indice en la tabla a coordenadas
    # fila columna
    def pos_a_fila_col(self, pos):
        """Devulve un par con la fila y columna que
        corresponden al índice dado en pos"""
        return (floor(pos / self.ancho), pos % self.ancho)
    
    # convertir una fila y columna a un índice en
    # el list _tablero
    def fila_col_a_pos(self, fila, col):
        """Devuelve el índice en _tablero que corresponde
        a la fila y col dadas"""
        return fila * self.ancho + col

    def leer_valor_en(self, fila=None, col=None, pos=None):
        """Permite obtener el valor en una celda del tablero.
        Permite leer indice (pos) o coordenadas (fila, col)"""
        if pos is not None:
            return self._tablero[pos]
        else:
            return self._tablero[self.fila_col_a_pos(fila, col)]

    def fijar_valor_en(self, fila=None, col=None, pos=None, valor=None):
        """Permite escribir valores en una celda del tablero.
        Permite escribir con indice (pos) o coordenadas (fila, col)"""
        if pos is None:
            self._tablero[self.fila_col_a_pos(fila, col)] = valor
        else:
            self._tablero[pos] = valor

    @classmethod
    def generar_aleatorio(self):
        """Genera un tablero aleatorio con un tamaño variable de 5 a 8"""
        ancho = random.randint(5, 8)
        alto = random.randint(5, 8)
        return Tablero(alto, ancho)

    def __str__(self):
        els = ""
        for i, val in enumerate(self._tablero):
            els += f"{val}"
            if i % self.ancho == self.ancho - 1:
                els += "\n"
            else:
                els += " | "
        return els