from multiprocessing import Pipe, Barrier, Queue
from core.test_clases import SemaforoTest, ControladorTest

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
        sem = SemaforoTest(via, conexiones_semaforos[via], barrier, queue_gui)
        semaforos.append(sem)

    controlador = ControladorTest(conexiones_controlador)

    for s in semaforos:
        s.start()
    controlador.start()

    controlador.join()

    for s in semaforos:
        s.terminate()
        s.join()

    print("[MAIN] Fin de la prueba.")

if __name__ == "__main__":
    main()
