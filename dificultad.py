from simon import Simon
import random

class Principiante(Simon):
    def __init__(self):
        super().__init__()
        self.nivel = "Principiante"
        self.setnivel()
    
    def setnivel(self):
        self.tiempo = 1000
        self.tiempojugador = 5000


class Experto(Simon):
    def __init__(self):
        super().__init__()
        self.nivel = "Experto"
        self.setnivel()
    
    def setnivel(self):
        self.tiempo = 800
        self.tiempojugador = 4000


class SuperExperto(Experto):
    def __init__(self):
        super().__init__()
        self.nivel = "SuperExperto"
        self.setnivel()

    def generar_secuencia(self):
        super().generar_secuencia()
        self.secuencia.append(random.choice(self.colores))
        return self.secuencia
