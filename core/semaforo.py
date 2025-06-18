import multiprocessing
import time
import random
from core.vehiculos import Vehiculo
from core.configuracion import VELOCIDAD_AVANCE, DISTANCIA_ENTRE_VEHICULOS

class ColaVehiculos:
    def __init__(self, via):
        self.via = via
        self.vehiculos = []
        self.contador = 0

    def agregar(self):
        v = Vehiculo(f"{self.via}_{self.contador}", self.via)
        self.contador += 1
        if self.vehiculos:
            ultimo = self.vehiculos[-1]
            v.posicion = ultimo.posicion - DISTANCIA_ENTRE_VEHICULOS
        else:
            v.posicion = 0
        self.vehiculos.append(v)

    def avanzar(self):
        for i, v in enumerate(self.vehiculos):
            if v.estado == "avanzando":
                if i == 0 or (self.vehiculos[i - 1].posicion - v.posicion) > DISTANCIA_ENTRE_VEHICULOS:
                    v.avanzar(VELOCIDAD_AVANCE)
        self.vehiculos = [v for v in self.vehiculos if v.estado != "cruzado"]

    def iniciar_avance(self):
        if self.vehiculos and self.vehiculos[0].estado != "avanzando":
            self.vehiculos[0].estado = "avanzando"

    def actualizar_estados(self):
        for i, v in enumerate(self.vehiculos):
            if v.estado == "esperando":
                if i == 0 or (self.vehiculos[i - 1].posicion - v.posicion) > DISTANCIA_ENTRE_VEHICULOS:
                    v.estado = "avanzando"
                else:
                    break

class Semaforo(multiprocessing.Process):
    def __init__(self, via, pipe, barrier, queue_gui):
        super().__init__()
        self.via = via
        self.pipe = pipe
        self.barrier = barrier
        self.queue_gui = queue_gui
        self.estado = "ROJO"
        self.cola = ColaVehiculos(via)

    def run(self):
        while True:
            if self.pipe.poll():
                self.estado = self.pipe.recv()
                if self.estado == "VERDE":
                    self.cola.iniciar_avance()
                self.queue_gui.put((self.via, self.estado))

            if random.random() < 0.3 and self.estado != "VERDE":
                self.cola.agregar()

            if self.estado == "VERDE":
                self.cola.avanzar()
                self.cola.actualizar_estados()

            vehiculos_data = [(v.id, v.posicion, v.estado) for v in self.cola.vehiculos]
            self.queue_gui.put((self.via + "_vehiculos", vehiculos_data))

            self.barrier.wait()
            time.sleep(0.1)
