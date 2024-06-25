import json
from jugador import Jugador

class GestorJugadores:
    def __init__(self):
        self.archivo = 'pysimonpuntajes.json'

    def guardar_puntaje(self,usuario):
        # Leer puntajes existentes para no sobrescribirlos
        puntajes = self.leer_puntajes()
        puntajes.append(usuario.to_dict())
        with open(self.archivo, 'w') as a:
            json.dump(puntajes, a,indent=4)
            a.close()
    def leer_puntajes(self):
        try:
            with open(self.archivo, 'r') as a:
                diccionario = json.load(a)
                # Devuelve lista de objetos Jugador
                a.close()
                return [jug for jug in diccionario]
                
        except FileNotFoundError:
            return []
        except json.decoder.JSONDecodeError as e:
            print("Error al decodificar el contenido JSON:", e)
            return []

    def ordenar(self):
        diccionario=self.leer_puntajes()
        jugadores = [Jugador(**jug) for jug in diccionario]
        return sorted(jugadores, reverse=True)
