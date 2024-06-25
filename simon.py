import random

class Simon:
    def __init__(self):
        self.colores = ["red", "green", "yellow", "blue"]
        self.secuencia = []
        self.secuencia_del_usuario = []
        self.puntos = 0
        self.nombre_jugador = ""
        self.tiempo = 0
        self.tiempojugador = 0
        self.setnivel()
                
    def generar_secuencia(self):
        self.secuencia_del_usuario = []
        self.secuencia.append(random.choice(self.colores))
        return self.secuencia
    
    def verificar_secuencia(self, color):
        self.secuencia_del_usuario.append(color)
        if self.secuencia_del_usuario == self.secuencia[:len(self.secuencia_del_usuario)]:
            if len(self.secuencia_del_usuario) == len(self.secuencia):
                self.puntos += 1
                return True
        else:
            return False
    
    def getniveles(self):
        return self.nivel
    
    def reiniciar_juego(self):
        self.secuencia = []
        self.secuencia_del_usuario = []
        self.puntos = 0
        
    def get_puntaje(self):
        return self.puntos
    
    def getnombre_jugador(self):
        return self.nombre_jugador
    
    def setnombre_jugador(self, nombre):
        self.nombre_jugador = nombre
    
    def getnivel(self):
        return self.nivel
    
    def setnivel(self):
        pass
    
    def get_tiempo(self):
        return self.tiempo
    
    def get_tiempo_jugador(self):
        return self.tiempojugador
        
    def get_light(self, color):
        light_colors = {
            "red": "#FFCCCC",
            "green": "#CCFFCC",
            "yellow": "#FFFFCC",
            "blue": "#CCCCFF"
        }
        return light_colors.get(color, color)

    def get_dark(self, color):
        dark_colors = {
            "red": "#990000",
            "green": "#009900",
            "yellow": "#999900",
            "blue": "#000099"
        }
        return dark_colors.get(color, color)
