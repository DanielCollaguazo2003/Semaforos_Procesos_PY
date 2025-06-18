from multiprocessing import Pipe, Barrier, Queue, Process, Manager
from model.semaforo import Semaforo
from controller.controlador import ControladorTrafico
from gui.gui import InterfazSemaforos
import time
import signal
import sys

def lanzar_gui(queue):
    try:
        InterfazSemaforos(queue)
    except KeyboardInterrupt:
        pass

def generar_reporte(semaforos_data):
    print("\n" + "="*50)
    print("REPORTE FINAL DE SIMULACIÓN")
    print("="*50)
    
    total_cruzados = sum(data['total_cruzados'] for data in semaforos_data.values())
    print(f"Total de vehículos que cruzaron: {total_cruzados}")
    
    print("\nTiempos de espera promedio por vía:")
    for via, data in semaforos_data.items():
        if data['tiempos_espera']:
            promedio = sum(data['tiempos_espera']) / len(data['tiempos_espera'])
            print(f"  {via}: {promedio:.2f} segundos")
        else:
            print(f"  {via}: No hay datos")
    
    print(f"\nCiclos completados: {semaforos_data.get('ciclos', 0)}")
    print("="*50)

def signal_handler(sig, frame):
    print('\nDeteniendo simulación...')
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    vias = ["NORTE", "SUR", "ESTE", "OESTE"]
    procesos = {}
    conexiones = {}
    barrier = Barrier(len(vias)) 
    
    queue_gui = Queue(maxsize=50)
    
    manager = Manager()
    semaforos_data = manager.dict()
    for via in vias:
        semaforos_data[via] = manager.dict({
            'total_cruzados': 0,
            'tiempos_espera': manager.list()
        })
    
    try:
        gui_process = Process(target=lanzar_gui, args=(queue_gui,))
        gui_process.start()
        
        for via in vias:
            parent_conn, child_conn = Pipe()
            semaforo = Semaforo(via, child_conn, barrier, queue_gui)
            semaforo.start()
            procesos[via] = semaforo
            conexiones[via] = parent_conn
        
        controlador = ControladorTrafico(conexiones, queue_gui)
        controlador.start()
        
        print("Simulación iniciada. Presione Ctrl+C para detener.")
        print("OPTIMIZACIONES APLICADAS:")
        print("- Queue con límite de 50 elementos")
        print("- Límite de vehículos por vía")
        print("- Throttling de actualizaciones GUI")
        print("- Barrier mantenido para sincronización")
        
        # Esperar a que termine el proceso GUI
        gui_process.join()
        
    except KeyboardInterrupt:
        print("\nDeteniendo simulación...")
    finally:
        # Terminar todos los procesos
        for proceso in procesos.values():
            proceso.terminate()
        
        if 'controlador' in locals():
            controlador.terminate()
        
        if 'gui_process' in locals():
            gui_process.terminate()
        
        # Generar reporte final
        generar_reporte(semaforos_data)

if __name__ == "__main__":
    main()