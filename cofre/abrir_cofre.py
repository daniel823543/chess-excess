from .comun import CofreComun
from .legendario import CofreLegendario
from .maldito import CofreMaldito
from .raro import CofreRaro

# clase para dar un cofre
# según el puntaje de la clave
class AbrirCofre:
    
    # devuelve el nombre del cofre maldito
    def nombre_cofre_maldito():
        return CofreMaldito.tipo

    # devuelve el nombre del cofre comun
    def nombre_cofre_comun():
        return CofreComun.tipo

    # devuelve el nombre del cofre raro
    def nombre_cofre_raro():
        return CofreRaro.tipo

    # devuelve el nombre del cofre legendario
    def nombre_cofre_legendario():
        return CofreLegendario.tipo

    def dar_cofre(self, puntos, contraseña):
        if puntos <= 1:
            # si la clave solo tiene un punto dar un cofre maldito
            return CofreMaldito(contraseña)
        elif puntos < 5:
            # si la clave solo tiene un punto dar un cofre comun
            return CofreComun(contraseña)
        elif puntos < 7:    
            # si la clave solo tiene un punto dar un cofre raro
            return CofreRaro(contraseña)
        else:
            # si la clave solo tiene un punto dar un cofre legendario
            return CofreLegendario(contraseña)
