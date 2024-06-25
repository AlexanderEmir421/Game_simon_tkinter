class Jugador:
    def __init__(self, nombre, puntos, fecha, hora, nivel):
        self.nombre = nombre
        self.puntos = puntos
        self.fecha = fecha
        self.hora = hora
        self.nivel = nivel

    def __gt__(self, other):
        return self.puntos > other.puntos

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "puntos": self.puntos,
            "fecha": self.fecha,
            "hora": self.hora,
            "nivel": self.nivel
        }
