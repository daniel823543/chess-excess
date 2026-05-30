# clase base de los cofres
# tienen el número y el número de puntos que otorgan

class Cofre():
    tipo = "Cofre Base"
    
    def __init__(self, contraseña=None):
        self.contraseña = contraseña

    def __str__(self):
        return f"--{self.tipo}--"

