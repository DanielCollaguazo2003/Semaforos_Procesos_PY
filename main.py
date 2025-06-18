import multiprocessing
from core.configuracion import VIAS
from core.semaforo import Semaforo
from core.controlador import ControladorTrafico
from gui.gui import GUI

def main():
    multiprocessing.set_start_method("spawn")
    queue_gui = multiprocessing.Queue()
    parent_conns, child_conns = {}, {}

    for via in VIAS:
        p, c = multiprocessing.Pipe()
        parent_conns[via] = p
        child_conns[via] = c

    barrier = multiprocessing.Barrier(len(VIAS) + 1)
    semaforos = [Semaforo(via, child_conns[via], barrier, queue_gui) for via in VIAS]
    controlador = ControladorTrafico(parent_conns, barrier, queue_gui)

    for s in semaforos:
        s.start()
    controlador.start()

    gui = GUI(queue_gui)
    gui.start()

    controlador.join()
    for s in semaforos:
        s.terminate()
        s.join()

if __name__ == "__main__":
    main()
