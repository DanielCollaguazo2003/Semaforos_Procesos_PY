from multiprocessing import Process
import time
import random
from model.vehiculo import Vehiculo, GeneradorVehiculos

class Semaforo(Process):
    def __init__(self, nombre, pipe_conn, barrier, queue_gui):
        super().__init__()
        self.nombre = nombre
        self.pipe = pipe_conn
        self.barrier = barrier 
        self.queue_gui = queue_gui
        self.estado = "ROJO"
        self.vehiculos_esperando = []
        self.vehiculos_moviendo = []
        self.generador = GeneradorVehiculos()
        self.total_vehiculos_cruzados = 0
        self.tiempos_espera = []
        self.max_vehiculos_por_via = 12  
        self.ultimo_envio_gui = 0
        self.intervalo_gui = 0.1
        self.contador_frames = 0

    def run(self):
        while True:
            self.contador_frames += 1
            
            if (len(self.vehiculos_moviendo) < self.max_vehiculos_por_via and 
                random.random() < 0.025):
                nuevo_vehiculo = self.generador.generar_vehiculo(self.nombre)
                if nuevo_vehiculo:
                    self.vehiculos_moviendo.append(nuevo_vehiculo)
            
            if self.pipe.poll():
                try:
                    mensaje = self.pipe.recv()
                    self.estado = mensaje
                except:
                    pass
            
            self._procesar_vehiculos()
            
            if self.contador_frames % 1 == 0:
                self._enviar_datos_gui()
            
            try:
                self.barrier.wait()
            except:
                pass
            
            time.sleep(0.05) 

    def _procesar_vehiculos(self):
        """Procesamiento optimizado de vehículos"""
        vehiculos_activos = []
        vehiculos_esperando_count = 0
        
        for vehiculo in self.vehiculos_moviendo:
            se_movio = vehiculo.mover(self.estado)
            
            if not se_movio:
                vehiculos_esperando_count += 1
            
            if (vehiculo.en_interseccion and 
                not hasattr(vehiculo, 'ya_contado')):
                vehiculo.tiempo_salida = time.time()
                self.tiempos_espera.append(vehiculo.tiempo_espera())
                self.total_vehiculos_cruzados += 1
                vehiculo.ya_contado = True
            
            if not vehiculo.ha_salido_de_pantalla():
                vehiculos_activos.append(vehiculo)
        
        self.vehiculos_moviendo = vehiculos_activos

    def _enviar_datos_gui(self):
        """Envío optimizado de datos a GUI"""
        tiempo_actual = time.time()
        
        if tiempo_actual - self.ultimo_envio_gui < self.intervalo_gui:
            return
        
        datos_gui = {
            'nombre': self.nombre,
            'estado': self.estado,
            'vehiculos_esperando': sum(1 for v in self.vehiculos_moviendo 
                                     if v.esta_en_zona_parada() and not v.puede_avanzar(self.estado)),
            'vehiculos_cruzados': self.total_vehiculos_cruzados,  # AGREGAR ESTA LÍNEA
            'vehiculos_moviendo': [(v.posicion_x, v.posicion_y, v.color, v.id) 
                                 for v in self.vehiculos_moviendo]
        }
        
        # Envío no bloqueante al Queue
        try:
            self.queue_gui.put_nowait(datos_gui)
            self.ultimo_envio_gui = tiempo_actual
        except:
            pass