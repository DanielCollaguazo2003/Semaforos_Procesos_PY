import multiprocessing
import time
from core.configuracion import CICLOS_TOTALES, TIEMPO_VERDE, TIEMPO_AMARILLO, VIAS_PARES

class ControladorTrafico(multiprocessing.Process):
    def __init__(self, conexiones, barrier, queue_gui):
        super().__init__()
        self.conexiones = conexiones
        self.barrier = barrier
        self.queue_gui = queue_gui
        self.vehiculos_cruzados = 0

    def run(self):
        for _ in range(CICLOS_TOTALES):
            for par in VIAS_PARES:
                self._activar(par, "VERDE")
                self._esperar(TIEMPO_VERDE)
                self._activar(par, "AMARILLO")
                self._esperar(TIEMPO_AMARILLO)
                self._activar(par, "ROJO")
        self.queue_gui.put(("FINALIZADO", ""))
    
    def _activar(self, vias, estado):
        for via in self.conexiones:
            if via in vias:
                self.conexiones[via].send(estado)

    def _esperar(self, segundos):
        for _ in range(int(segundos / 0.1)):
            self.barrier.wait()
            time.sleep(0.1)
