from multiprocessing import Process
import time

class Semaforo(Process):
    def __init__(self, nombre, pipe_conn, barrier, queue_gui):
        super().__init__()
        self.nombre = nombre
        self.pipe = pipe_conn
        self.barrier = barrier
        self.queue_gui = queue_gui
        self.estado = "ROJO"

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        self.queue_gui.put((self.nombre, self.estado))

    def run(self):
        while True:
            if self.pipe.poll():
                mensaje = self.pipe.recv()
                self.cambiar_estado(mensaje)
            self.barrier.wait()
