from .tablero import BLOQUEADO
from .tablero import GEMA
from .tablero import EMBRUJADO
from math import ceil
import random

# clase para el generador de una ruta valida
# el caballo es el pc que traza una ruta viable
# inicial
class Caballo:

    def __init__(self, tablero, fila, col):
        # relacionar tablero
        self.tablero = tablero
        # relacionar posicion vertical
        self.fila = fila
        # posicion horizontal
        self.col = col
        # pasos dados
        self.historia = []
        # agregar la posición inicial
        self.historia.append((fila, col))
    
    def inicia_en(self, fila, col):
        """Dice si la fila y columna dadas son el punto
        de inicio -- para marcarlo en el tablero"""
        # revisar si la historia tiene algo
        if not len(self.historia): 
            return False
        # leer el primer paso dado
        i_fila, i_col = self.historia[0]
        # comparar
        return fila == i_fila and col == i_col

    def termina_en(self, fila, col):
        """Dice si la fila y columan dadas son el punto
        final de la ruta -- para tablero """
        # lo compara con la posición final
        return self.fila == fila and self.col == col
    
    def desmarcar_visitados(self):
        """Desmarcar visitados"""
        # reiniciar estado tablero al inicial
        self.tablero.quitar_visitados()
    
    # metodo de clase para generar un caballo posicionado al azar
    @classmethod
    def posicionar_al_azar(cls, tablero):
        """Devuelve un caballo en el una posicion 
        aleatoria en el tablero dado"""
        # fila al azar
        fila = random.randint(0, tablero.alto - 1)
        # col al azar
        col = random.randint(0, tablero.ancho - 1)
        return Caballo(tablero, fila, col)

    def ver_saltos(self):
        """Obtiene un listado de pares (fila, col) que
        son movimientos válidos de un caballo de ajedrez
        y que están disponibles para el caballo"""
        return self.ver_saltos_desde(self.tablero, self.fila, self.col)

    # metodo de clase para buscar saltos posibles    
    @classmethod
    def ver_saltos_desde(cls, tablero, fila, col):
        # crear un listado de todos los valores (fila, columna)
        # posibles para un salto
        saltos = [
            (fila - 2, col - 1), 
            (fila - 2, col + 1),
            (fila - 1, col - 2), 
            (fila - 1, col + 2),
            (fila + 1, col - 2), 
            (fila + 1, col + 2),
            (fila + 2, col - 1), 
            (fila + 2, col + 1),
        ]
        # inicializar resultado
        validos = []
        # recorrer todos los pares
        for fila, col in saltos:
            # descartar los pares que quedan fuera del tablero
            if not (0 <= fila < tablero.alto and 0 <= col < tablero.ancho):
                continue
            # descartar los pares que no están bloqueados
            if tablero.leer_valor_en(fila=fila, col=col) == BLOQUEADO:
                continue
            # agregar los pares que pasen los chequeos anteriores
            validos.append((fila, col))
        # devolver los pares válids
        return validos       

    def marcar_ruta(self, total_saltos=None, num_gemas=1):
        """Genera una ruta aleatoria en el tablero"""
        # si no recibe cuántos saltos dar
        # el número de saltos es aleatorio
        if total_saltos is None:
            total_saltos = random.randint(4, 10)
        # print("saltos", total_saltos, "gemas", num_gemas)
        espacio_gemas = ceil(total_saltos / (num_gemas + 1))
        # print("espacio_gemas", espacio_gemas)
        # repetir por cada salto
        for el in range(1, total_saltos):
            # si hay que n poner gemas y llega al salto cercano total/n
            # poner una gema
            if num_gemas >= 1 and el % espacio_gemas == 0:
                # print("Poner Gema", el, "en ", self.fila, self.col)
                self.tablero.poner_gema_en(fila=self.fila, col=self.col)
            # obtener listado de movidas posibles
            saltos = self.ver_saltos()
            if len(saltos) == 0:
                # si no hay nada salir
                self.tope = len(self.historia)
                break
            # elegir un salto al azar
            salto = random.choice(saltos)
            # evitar los repetidos la mitad de las veces
            # (decidido al azar)
            if salto in self.historia and random.randint(0, 10) < 5:
                continue
            # registrar el salto
            self.historia.append(salto)
            # mover el puntero a ese lugar
            self.fila, self.col = salto
        # ese es el número máximo de saltos
        # para el bono de saltos           
        self.tope = len(self.historia)

    # revisar el contenido del tablero por gemas
    def es_gema(self, fila=None, col=None, pos=None):
        return self.tablero.leer_valor_en(fila=fila, col=col, pos=pos) == GEMA

    # revisar el contenido del tablero por embrujo
    def es_embrujo(self, fila=None, col=None, pos=None):
        return self.tablero.leer_valor_en(fila=fila, col=col, pos=pos) == EMBRUJADO

    def __str__(self):
        els = ""
        for i, val in enumerate(self.tablero._tablero):
            if i == self.tablero.fila_col_a_pos(self.fila, self.col):
                els += "  X"
            else:
                els += f"{val:3.0f}"
            if i % self.tablero.ancho == self.tablero.ancho - 1:
                els += "\n"
            else:
                els += " | "
        return els
