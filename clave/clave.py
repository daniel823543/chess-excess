import random

class ContraseñaException(Exception):
    pass

# clase para gestionar las contraseñas
class Contraseña:
    # listado de las categorías de caracteres
    grupos = {
        'mayuscula': "ABDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚ",
        'minuscula': "abdefghijklmnñopqrstuvwxyzáéíóú",
        'numeros': "0123456789",
        'especial': "¿¡?=)(/¨*+-%&$#!.",
    }

    def __init__(self):
        # longitud como propiedad privada
        self._longitud = 8
    
    # permite escribir la longitud
    def fijar_longitud(self, longitud):
        self._longitud = longitud

    # permite leer la longitud
    def leer_logintud(self):
        return self._longitud

    # validacion 
    def caracter_repetido(self, clave):
        """Dice si la clave tiene un caracter repetido"""
        # listado de letras usadas
        letras = {}
        # por cada caracter en la clave
        for el in clave:
            # si ya está en el diccionario -está repetido
            if letras.get(el) is not None:
                # hay repetidos
                return True
            # si no está en el diccionario agregarlo
            letras[el] = 0
        # si encuentra repetidos devuelve false
        return False

    # generación de contraseñas
    def generar_contraseña(self, grupos, permitir_repetidos=False, forzar_repetidos=False):
        """Genera una contraseña con las opciones dadas.
        grupos: cuáles grupos de caracteres usar (numeros, minusculas, etc)
        permitir_repetidos: si debe evitar usar un caracter dos veces
        forzar_repetidos: si debe usar al menos un caracter dos veces
        """
        # list que contiene los caracteres de la contraseña
        componentes = []
        # aglutinador de los caracteres de los grupos utilizados
        todos = []
        # recorrer todos los grupos requeridos y tomar un caracter de cada uno
        # para asegurar la presencia de al menos un caracter de cada clase
        for el in grupos:
            # agregar el grupo entero al aglutinador
            todos.extend(list(self.grupos[el]))
            # elegir un caracter al azar de los caracteres del grupo
            letra = random.choice(list(self.grupos[el]))
            # si no permite repetidos y el caracter ya está incluido
            # no hacer nada
            if not permitir_repetidos and letra in componentes:
                continue
            # si pasó el chequeo anterior agregarlo a los caracteres a usar
            componentes.append(letra)
        
        # hasta aquí la clave tiene un elemento de cada grupo
        # ahora se llena el resto de la longitud con caracteres de todos
        # los grupos requeridos

        max_stop = 1000
        # repetir mientras no se tengan los caracteres suficientes
        # y en tanto hay a grupos de donde seleccionar
        while len(grupos) > 0 and len(componentes) < self._longitud and max_stop > 0:
            max_stop = max_stop - 1
            # tomar una caracter de todos los requeriods
            letra = random.choice(todos)
            # si no esta repetido ignorar
            if not permitir_repetidos and letra in componentes:
                continue
            # si es nuevo agregar a los caracteres a utilizar
            componentes.append(letra)
        # si se fuerza la presencia de un repetido
        if forzar_repetidos:
            # sacar un caracter al azar para abrir campo al repetido
            componentes.pop(random.randint(0, len(componentes) - 1))
            # duplicar un caracter al azar
            componentes.append(componentes[random.randint(0, len(componentes) - 1)])
        # dar un orden aleatorio al listado de caracteres a usar
        random.shuffle(componentes)
        # convertir el listado de caracteres en un str
        return "".join(componentes)

    def validar_mayuscula(self, clave):
        """Dice si la clave tiene una letra mayúscula"""
        return self.validar_grupo('mayuscula', clave)

    def validar_minuscula(self, clave):
        """Dice si la clave tiene una letra minuscula"""
        return self.validar_grupo('minuscula', clave)

    def validar_numeros(self, clave):
        """Dice si la clave tiene un numero"""
        return self.validar_grupo('numeros', clave)

    def validar_especial(self, clave):
        """Dice si la clave tiene un caracter especial"""
        return self.validar_grupo('especial', clave)

    def puntuar_contraseña(self, clave):
        """Da una puntuación numérica a la clave dada"""
    
        puntos = 0
        if len(clave) >= 8:
            # si tiene 8 o más de largo dar un punto
            # print("len(clave) >= 8:")
            puntos += 1
        if len(clave) >= 14:
            # si tiene 14 o más de largo dar un punto
            # print("len(clave) >= 14:")
            puntos += 1
        if self.validar_mayuscula(clave):
            # si tiene mayúscula dar un punto
            # print("self.validar_mayuscula(clave):")
            puntos += 1
        if self.validar_minuscula(clave):
            # si tiene minúscula dar un punto
            # print("self.validar_minuscula(clave):")
            puntos += 1
        if self.validar_numeros(clave):
            # si tiene un numero dar un punto
            # print("self.validar_numeros(clave):")
            puntos += 1
        if self.validar_especial(clave):
            # si tiene un caracter especial dar un punto
            # print("self.validar_especial(clave):")
            puntos += 1
        if not self.caracter_repetido(clave):
            # si no tiene caracteres repetidos un punto
            # print("not self.caracter_repetido(clave):")
            puntos += 1
        return puntos

    def es_valida(self, clave):
        """Validar contraseñas"""
        if not self.validar_mayuscula(clave):
            raise ContraseñaException("Contraseña no valida: falta mayúscula")
        if not self.validar_minuscula(clave):
            raise ContraseñaException("Contraseña no valida: falta minúscula")
        if not self.validar_numeros(clave):
            raise ContraseñaException("Contraseña no valida: falta numero")
        if not self.validar_especial(clave):
            raise ContraseñaException("Contraseña no valida: falta caracter especial")
        if self.caracter_repetido(clave):
            raise ContraseñaException("Contraseña no valida: tiene caracteres repetidos")
        return True

    def validar_grupo(self, grupo, clave):
        """Validar que la clave tenga al menos un elemento del grupo dado"""
        # recorrer los caracteres del grupo
        for el in self.grupos[grupo]:
            # uno por uno revisar si están en clave
            if el in clave:
                # si están es válido
                return True
        # si no hay caracteres del grupo es no válido
        return False
