from multiprocessing import Process
import time
from vehiculos import ColaVehiculos

class Semaforo(Process):
    def __init__(self, nombre, pipe_conn, barrier, queue_gui):
        super().__init__()
        self.nombre = nombre
        self.pipe = pipe_conn
        self.barrier = barrier
        self.queue_gui = queue_gui
        self.estado = "ROJO"
        self.cola_vehiculos = ColaVehiculos(nombre)

    def run(self):
        ciclo = 0
        while True:
            if self.pipe.poll():
                mensaje = self.pipe.recv()
                self.estado = mensaje
                if self.estado == "VERDE":
                    self.cola_vehiculos.iniciar_avance()
                self.queue_gui.put((self.nombre, self.estado))  # Notifica estado semáforo

            if self.estado == "VERDE":
                self.cola_vehiculos.avanzar_vehiculos()
                # Enviar info de vehículos a la GUI
                self.queue_gui.put((self.nombre + "_vehiculos", 
                                    [(v.id, v.posicion, v.estado) for v in self.cola_vehiculos.vehiculos]))

            self.barrier.wait()
            time.sleep(0.5)
