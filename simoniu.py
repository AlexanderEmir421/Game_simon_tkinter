import tkinter as tk
from tkinter import Menu, messagebox, Toplevel, OptionMenu
from gestor import GestorJugadores
from jugador import Jugador
from tkinter import ttk
from datetime import datetime
from dificultad import Experto, Principiante, SuperExperto
from simon import Simon

class SimonIU:
    def __init__(self, root, G, simon=Simon, jugador=Jugador):
        self.coloresc = ["red", "green", "yellow", "blue"]
        self.niveles = ["Principiante", "Experto", "SuperExperto"]
        self.root = root
        self.simon = Simon
        self.root.title("Simon dice")
        self.botones = {}
        self.crear()
        self.rank = G
        self.jugador = jugador
        
    def crear(self):
        # Crea Menu de opciones
        inicio = Menu(self.root)
        self.root.config(menu=inicio)
        puntos = Menu(self.root)
        inicio.add_cascade(label="Opciones", menu=puntos)
        puntos.add_command(label="Ver puntajes", command=self.ranking)
        puntos.add_command(label="Salir", command=self.root.quit)

        # Ingresa nombre
        self.output_nombre = tk.Label(self.root, text="Nombre ")
        self.output_nombre.pack(pady=10, padx=10)
        self.input_nombre = tk.Entry(self.root)
        self.input_nombre.pack(pady=10, padx=10)

        # Iniciar
        self.menu_juego = tk.Button(self.root, text="Jugar", command=self.menu_jugar)
        self.menu_juego.pack(pady=10, padx=10)
        
        # Cuadrados
        self.cuadrado = tk.Frame(self.root)
        for i, color in enumerate(self.coloresc):
            boton = tk.Canvas(self.cuadrado, bg=color, width=100, height=100)
            boton.bind("<Button-1>", lambda event, color=color: self.seleccion_y_verificar(color))
            boton.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            self.botones[color] = boton

        self.boton_jugar = tk.Button(self.root, text="Jugar", command=self.jugar)
        self.valor = tk.StringVar(self.root)
        self.valor.set("Seleccionar nivel ")
        self.select_nivel = OptionMenu(self.root, self.valor, *self.niveles)
        self.label_tiempo = tk.Label(self.root, text="Tiempo: --")
        
    def menu_jugar(self):
        nombre = self.input_nombre.get()
        if nombre:
            # Ocultar menu usuario
            self.output_nombre.pack_forget()
            self.input_nombre.pack_forget()
            self.menu_juego.pack_forget()
            self.puntaje_jugador = tk.Label(self.root, text=nombre)
            self.puntaje_jugador.pack(pady=5)
            self.select_nivel.pack()
            self.cuadrado.pack(pady=5, padx=5)
            self.boton_jugar.pack(pady=5, padx=5)
            
        else:
            messagebox.showwarning("Advertencia", "Ingrese Nombre")

    def jugar(self):
        nivel = self.valor.get()
        if nivel == "Principiante":
            self.simon = Principiante()
        elif nivel == "Experto":
            self.simon = Experto()
        elif nivel == "SuperExperto":
            self.simon = SuperExperto()
        self.simon.setnombre_jugador(self.input_nombre.get())        
        self.boton_jugar.pack_forget()
        self.generar_y_mostrar_secuencia()
    
    def seleccion_y_verificar(self, color):
        try:
            if isinstance(self.simon, Experto) or isinstance(self.simon, SuperExperto):
                self.contador_activo=False
                self.actualizar_contador()
            original_color = self.botones[color].cget("bg")
            self.botones[color].config(bg=self.simon.get_dark(color))
            self.root.after(500, lambda: self.botones[color].config(bg=original_color))
            resultado = self.simon.verificar_secuencia(color)
            
            if resultado is True:
                self.puntaje_jugador.config(text=f"{self.simon.getnombre_jugador()}: {self.simon.get_puntaje()}")
                self.root.after(1000, self.generar_y_mostrar_secuencia)
            elif resultado is False:
                raise ValueError("Secuencia incorrecta")
                
        except TimeoutError:
            messagebox.showinfo("Tiempo agotado", "Se ha agotado el tiempo para ingresar la secuencia")
            
        except ValueError as e:
            self.game_over()
            
    def generar_y_mostrar_secuencia(self):
        secuencia = self.simon.generar_secuencia()
        for boton in self.botones.values():
            boton.config(state=tk.DISABLED)
        for i, color in enumerate(secuencia):
            self.root.after(self.simon.get_tiempo() * (i + 1), lambda color=color: self.parpadear_boton(color))
        self.root.after(self.simon.get_tiempo_jugador() * (len(secuencia) + 1), self.permitir_jugada) 
        if isinstance(self.simon, Experto) or isinstance(self.simon, SuperExperto):
            self.tiempo_restante = self.simon.get_tiempo_jugador() // 1000
            self.label_tiempo.pack()
            self.contador_activo = True
            self.actualizar_contador()
    
    def actualizar_contador(self):
        if self.tiempo_restante >= 0 and self.contador_activo:
            self.label_tiempo.config(text=f"Tiempo: {self.tiempo_restante}")
            self.tiempo_restante -= 1
            self.root.after(1000, self.actualizar_contador)
        elif self.tiempo_restante < 0:
            self.game_over()
            raise TimeoutError
    
    
            
    def permitir_jugada(self):
        for boton in self.botones.values():
            boton.config(state=tk.NORMAL)
            
    def parpadear_boton(self, color):
        original_color = self.botones[color].cget("bg")
        self.botones[color].config(bg=self.simon.get_light(color))
        self.root.after(500, lambda: self.botones[color].config(bg=original_color))
              
    def game_over(self):
        for boton in self.botones.values():
            boton.config(state=tk.DISABLED)
        messagebox.showerror("Game Over", f"Perdiste! Tu puntaje fue: {self.simon.get_puntaje()}")
        self.jugador = Jugador(self.simon.getnombre_jugador(), self.simon.get_puntaje(), datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S"), self.simon.getnivel())
        self.rank.guardar_puntaje(self.jugador)
        del self.jugador
        self.boton_jugar.pack(pady=5, padx=5)
        self.label_tiempo.pack_forget()
        
    def ranking(self):
        top = Toplevel(self.root)
        top.title("Puntajes")
        tree = ttk.Treeview(top, columns=("Nombre", "Puntaje", "Fecha", "Hora", "Nivel"), show="headings")        
        tree.heading("Nombre", text="Nombre")
        tree.heading("Puntaje", text="Puntaje")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Hora", text="Hora")
        tree.heading("Nivel", text="Nivel")
        for jugadores in self.rank.ordenar():
            tree.insert("", "end", values=(jugadores.nombre, jugadores.puntos, jugadores.fecha, jugadores.hora, jugadores.nivel))
        tree.pack(expand=True, fill=tk.BOTH)
            
if __name__ == "__main__":
    root = tk.Tk()
    G = GestorJugadores()
    SimonIU(root, G)
    root.mainloop()
