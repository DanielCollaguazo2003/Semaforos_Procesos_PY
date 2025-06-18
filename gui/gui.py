import tkinter as tk
from queue import Empty

class GUI:
    def __init__(self, queue_gui):
        self.queue = queue_gui
        self.root = tk.Tk()
        self.root.title("Simulación de Tráfico")
        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="white")
        self.canvas.pack()
        self.semaforos = {}
        self.vehiculos = {}
        self._dibujar_interseccion()
        self.root.after(100, self.actualizar)

    def _dibujar_interseccion(self):
        coords = {
            "NORTE": (280, 100, 320, 140),
            "SUR": (280, 460, 320, 500),
            "ESTE": (460, 280, 500, 320),
            "OESTE": (100, 280, 140, 320)
        }
        for via, (x1, y1, x2, y2) in coords.items():
            self.semaforos[via] = self.canvas.create_oval(x1, y1, x2, y2, fill="red")

    def actualizar(self):
        while True:
            try:
                nombre, contenido = self.queue.get_nowait()
                if nombre in self.semaforos:
                    color = {"ROJO": "red", "AMARILLO": "yellow", "VERDE": "green"}.get(contenido, "gray")
                    self.canvas.itemconfig(self.semaforos[nombre], fill=color)
                elif nombre.endswith("_vehiculos"):
                    self._dibujar_vehiculos(nombre.replace("_vehiculos", ""), contenido)
                elif nombre == "FINALIZADO":
                    print("Simulación completada.")
                    self.root.destroy()
            except Empty:
                break
        self.root.after(100, self.actualizar)

    def _dibujar_vehiculos(self, via, lista):
        if via not in self.vehiculos:
            self.vehiculos[via] = {}
        for rect in self.vehiculos[via].values():
            self.canvas.delete(rect)
        self.vehiculos[via] = {}

        base = {
            "NORTE": (300, 140),
            "SUR": (300, 460),
            "ESTE": (460, 300),
            "OESTE": (140, 300)
        }
        dxdy = {
            "NORTE": (0, 1),
            "SUR": (0, -1),
            "ESTE": (-1, 0),
            "OESTE": (1, 0)
        }
        x0, y0 = base[via]
        dx, dy = dxdy[via]

        for v_id, pos, estado in lista:
            x = x0 + dx * pos
            y = y0 + dy * pos
            color = "blue" if estado == "avanzando" else "gray"
            self.vehiculos[via][v_id] = self.canvas.create_rectangle(x - 6, y - 6, x + 6, y + 6, fill=color)


    def start(self):
        self.root.mainloop()
