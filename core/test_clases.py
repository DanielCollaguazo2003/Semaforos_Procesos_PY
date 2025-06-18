from core.semaforo import Semaforo
from core.controlador import ControladorTrafico
import time

class SemaforoTest(Semaforo):
    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        print(f"[{self.nombre}] Cambia a: {self.estado}")
        self.queue_gui.put((self.nombre, self.estado))

class ControladorTest(ControladorTrafico):
    def run(self):
        for i in range(2):
            print(f"[Controlador] Ciclo {i+1} - NORTE-SUR VERDE")
            self._cambiar_estados(["NORTE", "SUR"], "VERDE", ["ESTE", "OESTE"], "ROJO")
            time.sleep(2)
            self._cambiar_estados(["NORTE", "SUR"], "AMARILLO", [], "")
            time.sleep(1)

            print(f"[Controlador] Ciclo {i+1} - ESTE-OESTE VERDE")
            self._cambiar_estados(["ESTE", "OESTE"], "VERDE", ["NORTE", "SUR"], "ROJO")
            time.sleep(2)
            self._cambiar_estados(["ESTE", "OESTE"], "AMARILLO", [], "")
            time.sleep(1)

        print("[Controlador] Terminado")
