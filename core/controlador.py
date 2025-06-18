from multiprocessing import Process
import time

class ControladorTrafico(Process):
    def __init__(self, conexiones, ciclos=10):
        super().__init__()
        self.conexiones = conexiones
        self.ciclos = ciclos

    def run(self):
        for ciclo in range(self.ciclos):
            print(f"[Controlador] Ciclo {ciclo+1}: NORTE-SUR en verde")
            self._cambiar_estados(["NORTE", "SUR"], "VERDE", ["ESTE", "OESTE"], "ROJO")
            time.sleep(5)
            self._cambiar_estados(["NORTE", "SUR"], "AMARILLO", [], "")
            time.sleep(2)

            print(f"[Controlador] Ciclo {ciclo+1}: ESTE-OESTE en verde")
            self._cambiar_estados(["ESTE", "OESTE"], "VERDE", ["NORTE", "SUR"], "ROJO")
            time.sleep(5)
            self._cambiar_estados(["ESTE", "OESTE"], "AMARILLO", [], "")
            time.sleep(2)

        print("[Controlador] Simulación finalizada.")

    def _cambiar_estados(self, vias_verde, estado_verde, vias_rojo, estado_rojo):
        for via in vias_verde:
            self.conexiones[via].send(estado_verde)
        for via in vias_rojo:
            self.conexiones[via].send(estado_rojo)
