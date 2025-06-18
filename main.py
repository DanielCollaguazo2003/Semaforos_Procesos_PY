from multiprocessing import Process, Pipe, Barrier, Queue
from tkinter import Tk
from core.semaforo import Semaforo
from core.controlador import ControladorTrafico
from gui.gui import InterfazSemaforos

def main():
    vias = ["NORTE", "SUR", "ESTE", "OESTE"]
    conexiones_controlador = {}
    conexiones_semaforos = {}

    for via in vias:
        parent_conn, child_conn = Pipe()
        conexiones_controlador[via] = parent_conn
        conexiones_semaforos[via] = child_conn

    barrier = Barrier(parties=4)
    queue_gui = Queue()

    semaforos = []
    for via in vias:
        sem = Semaforo(via, conexiones_semaforos[via], barrier, queue_gui)
        semaforos.append(sem)

    controlador = ControladorTrafico(conexiones_controlador)

    for s in semaforos:
        s.start()
    controlador.start()

    root = Tk()
    app = InterfazSemaforos(root, queue_gui)
    root.mainloop()

    controlador.join()
    for s in semaforos:
        s.terminate()
        s.join()

if __name__ == "__main__":
    main()
