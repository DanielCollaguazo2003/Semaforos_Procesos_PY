# controlador.py
from multiprocessing import Process
import time

class ControladorTrafico(Process):
    def __init__(self, conexiones, queue_gui):
        super().__init__()
        self.conexiones = conexiones
        self.queue_gui = queue_gui
        self.ciclos_completados = 0

    def run(self):
        while True:
            print(f"[Controlador] Ciclo {self.ciclos_completados + 1}: NORTE-SUR en verde")
            self._enviar_estado_controlador("NORTE-SUR VERDE")
            self._cambiar_estados(["NORTE", "SUR"], "VERDE", ["ESTE", "OESTE"], "ROJO")
            time.sleep(5)
            
            self._cambiar_estados(["NORTE", "SUR"], "AMARILLO", [], "")
            time.sleep(2)

            print(f"[Controlador] Ciclo {self.ciclos_completados + 1}: ESTE-OESTE en verde")
            self._enviar_estado_controlador("ESTE-OESTE VERDE")
            self._cambiar_estados(["ESTE", "OESTE"], "VERDE", ["NORTE", "SUR"], "ROJO")
            time.sleep(5)
            
            self._cambiar_estados(["ESTE", "OESTE"], "AMARILLO", [], "")
            time.sleep(2)
            
            self.ciclos_completados += 1

    def _cambiar_estados(self, vias_verde, estado_verde, vias_rojo, estado_rojo):
        for via in vias_verde:
            self.conexiones[via].send(estado_verde)
        for via in vias_rojo:
            self.conexiones[via].send(estado_rojo)
    
    def _enviar_estado_controlador(self, mensaje):
        datos_controlador = {
            'tipo': 'controlador',
            'mensaje': mensaje,
            'ciclos': self.ciclos_completados
        }
        self.queue_gui.put(datos_controlador)