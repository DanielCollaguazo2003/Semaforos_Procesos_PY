import tkinter as tk
from multiprocessing import Queue

# Coordenadas para ubicar semáforos en la intersección (vista superior)
POSICIONES = {
    "NORTE": (100, 20),
    "SUR":   (100, 180),
    "ESTE":  (180, 100),
    "OESTE": (20, 100)
}

COLORES = {
    "ROJO": "red",
    "VERDE": "green",
    "AMARILLO": "yellow"
}

class InterfazSemaforos:
    def __init__(self, root: tk.Tk, queue_gui: Queue):
        self.root = root
        self.queue = queue_gui
        self.root.title("Simulación de Semáforos")
        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.pack()

        self.labels = {}
        self.dibujar_interseccion()
        self.actualizar_gui()

    def dibujar_interseccion(self):
        for via, (x, y) in POSICIONES.items():
            # Dibujar círculo del semáforo
            color_inicial = "gray"
            oval = self.canvas.create_oval(x, y, x+40, y+40, fill=color_inicial)
            # Dibujar texto con el nombre de la vía
            self.canvas.create_text(x + 20, y + 55, text=via, font=("Arial", 10))
            self.labels[via] = oval

    def actualizar_gui(self):
        while not self.queue.empty():
            via, estado = self.queue.get()
            color = COLORES.get(estado, "gray")
            self.canvas.itemconfig(self.labels[via], fill=color)

        self.root.after(100, self.actualizar_gui)
