# gui.py - Versión optimizada
import tkinter as tk
from tkinter import ttk
from multiprocessing import Queue
import threading
import time

class InterfazSemaforos:
    def __init__(self, queue):
        self.queue = queue
        self.root = tk.Tk()
        self.root.title("Simulación de Tráfico - Cuenca")
        self.root.geometry("800x700")
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas para la simulación
        self.canvas = tk.Canvas(main_frame, width=500, height=500, bg="#f0f0f0")
        self.canvas.pack(side=tk.LEFT, padx=(0, 10))
        
        # Panel de información
        self.info_frame = ttk.Frame(main_frame)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self._crear_panel_info()
        self._dibujar_interseccion()
        
        # Diccionario para almacenar elementos gráficos
        self.semaforos = {
            "NORTE": {"rojo": None, "amarillo": None, "verde": None},
            "SUR": {"rojo": None, "amarillo": None, "verde": None},
            "ESTE": {"rojo": None, "amarillo": None, "verde": None},
            "OESTE": {"rojo": None, "amarillo": None, "verde": None}
        }
        
        # OPTIMIZACIONES GUI
        self.vehiculos_canvas = {}  # Cambiar a dict para mejor gestión
        self.ultimo_update_vehiculos = {}  # Tracking de actualizaciones
        self.estado_actual = "Iniciando..."
        self.ciclos_completados = 0
        self.estadisticas = {via: {"esperando": 0, "cruzados": 0} for via in ["NORTE", "SUR", "ESTE", "OESTE"]}
        
        # Crear semáforos
        self._crear_semaforos()
        
        # Hilo optimizado para actualizar GUI
        self.thread = threading.Thread(target=self._actualizar_gui_optimizado)
        self.thread.daemon = True
        self.thread.start()
        
        # Actualizar información cada segundo
        self._actualizar_info()
        
        self.root.mainloop()

    def _crear_panel_info(self):
        # Título
        titulo = ttk.Label(self.info_frame, text="SIMULACIÓN DE TRÁFICO", 
                          font=("Arial", 14, "bold"))
        titulo.pack(pady=(0, 10))
        
        # Información del sistema
        ttk.Label(self.info_frame, text="Estado del Sistema:", 
                 font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.label_estado = ttk.Label(self.info_frame, text="Iniciando...")
        self.label_estado.pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(self.info_frame, text="Ciclos Completados:", 
                 font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.label_ciclos = ttk.Label(self.info_frame, text="0")
        self.label_ciclos.pack(anchor=tk.W, pady=(0, 10))
        
        # Estadísticas por vía
        ttk.Label(self.info_frame, text="Estadísticas por Vía:", 
                 font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        
        self.labels_stats = {}
        for via in ["NORTE", "SUR", "ESTE", "OESTE"]:
            frame_via = ttk.Frame(self.info_frame)
            frame_via.pack(fill=tk.X, pady=2)
            
            ttk.Label(frame_via, text=f"{via}:", 
                     font=("Arial", 9, "bold")).pack(side=tk.LEFT)
            
            label_stats = ttk.Label(frame_via, text="Esperando: 0 | Cruzados: 0")
            label_stats.pack(side=tk.LEFT, padx=(10, 0))
            self.labels_stats[via] = label_stats
        
        # Leyenda
        ttk.Label(self.info_frame, text="Leyenda:", 
                 font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(20, 5))
        
        leyenda_frame = ttk.Frame(self.info_frame)
        leyenda_frame.pack(fill=tk.X)
        
        colores_leyenda = [
            ("🔴", "Semáforo en Rojo"),
            ("🟡", "Semáforo en Amarillo"),
            ("🟢", "Semáforo en Verde"),
            ("🚗", "Vehículos en Movimiento")
        ]
        
        for emoji, descripcion in colores_leyenda:
            frame_item = ttk.Frame(leyenda_frame)
            frame_item.pack(fill=tk.X, pady=1)
            ttk.Label(frame_item, text=emoji).pack(side=tk.LEFT)
            ttk.Label(frame_item, text=descripcion, font=("Arial", 8)).pack(side=tk.LEFT, padx=(5, 0))

    def _dibujar_interseccion(self):
        # Carreteras
        self.canvas.create_rectangle(0, 220, 500, 280, fill="#555", outline="#333", width=2)
        self.canvas.create_rectangle(220, 0, 280, 500, fill="#555", outline="#333", width=2)
        
        # Líneas divisorias
        self.canvas.create_line(250, 0, 250, 220, fill="white", width=2, dash=(5, 5))
        self.canvas.create_line(250, 280, 250, 500, fill="white", width=2, dash=(5, 5))
        self.canvas.create_line(0, 250, 220, 250, fill="white", width=2, dash=(5, 5))
        self.canvas.create_line(280, 250, 500, 250, fill="white", width=2, dash=(5, 5))
        
        # Líneas de parada
        self.canvas.create_line(220, 160, 280, 160, fill="red", width=3)
        self.canvas.create_line(220, 340, 280, 340, fill="red", width=3)
        self.canvas.create_line(160, 220, 160, 280, fill="red", width=3)
        self.canvas.create_line(340, 220, 340, 280, fill="red", width=3)
        
        # Etiquetas de direcciones
        self.canvas.create_text(250, 30, text="NORTE", fill="black", font=("Arial", 12, "bold"))
        self.canvas.create_text(250, 470, text="SUR", fill="black", font=("Arial", 12, "bold"))
        self.canvas.create_text(470, 250, text="ESTE", fill="black", font=("Arial", 12, "bold"))
        self.canvas.create_text(30, 250, text="OESTE", fill="black", font=("Arial", 12, "bold"))

    def _crear_semaforos(self):
        configuracion = {
            "NORTE": (230, 190),
            "SUR": (270, 310),
            "ESTE": (310, 270),
            "OESTE": (190, 230)
        }

        for nombre, (x, y) in configuracion.items():
            self._crear_poste_semaforo(nombre, x, y)

    def _crear_poste_semaforo(self, nombre, x, y):
        r = 8
        
        # Fondo del semáforo
        self.canvas.create_rectangle(x-r-3, y-3*r-3, x+r+3, y+3*r+3, 
                                   fill="black", outline="gray", width=2)
        
        # Luces
        rojo = self.canvas.create_oval(x-r, y-2.5*r, x+r, y-0.5*r, fill="gray", outline="black")
        amarillo = self.canvas.create_oval(x-r, y-0.5*r, x+r, y+1.5*r, fill="gray", outline="black")
        verde = self.canvas.create_oval(x-r, y+0.5*r, x+r, y+2.5*r, fill="gray", outline="black")
        
        self.semaforos[nombre]["rojo"] = rojo
        self.semaforos[nombre]["amarillo"] = amarillo
        self.semaforos[nombre]["verde"] = verde

    def _actualizar_gui_optimizado(self):
        """Versión optimizada del hilo de actualización GUI"""
        contador = 0
        while True:
            mensajes_procesados = 0
            
            # Procesar múltiples mensajes del queue por iteración
            while not self.queue.empty() and mensajes_procesados < 10:
                try:
                    datos = self.queue.get_nowait()
                    
                    if isinstance(datos, dict):
                        if datos.get('tipo') == 'controlador':
                            self.estado_actual = datos['mensaje']
                            self.ciclos_completados = datos['ciclos']
                        else:
                            nombre = datos['nombre']
                            estado = datos['estado']
                            vehiculos_esperando = datos['vehiculos_esperando']
                            vehiculos_moviendo = datos['vehiculos_moviendo']
                            vehiculos_cruzados = datos.get('vehiculos_cruzados', 0)  # AGREGAR ESTA LÍNEA
                            
                            # Actualizar semáforo
                            self._actualizar_semaforo(nombre, estado)
                            
                            # Actualizar estadísticas
                            self.estadisticas[nombre]['esperando'] = vehiculos_esperando
                            self.estadisticas[nombre]['cruzados'] = vehiculos_cruzados  # AGREGAR ESTA LÍNEA
                            
                            # Actualizar vehículos con throttling
                            if contador % 1 == 0:  # Solo cada 2 iteraciones
                                self._actualizar_vehiculos_via_optimizado(nombre, vehiculos_moviendo)
                    
                    mensajes_procesados += 1
                    
                except:
                    break  # Queue vacío o error
            
            contador += 1
            time.sleep(0.02)  # 20 FPS máximo

    def _actualizar_vehiculos_via_optimizado(self, via, vehiculos_moviendo):
        """Actualización optimizada de vehículos por vía"""
        # Inicializar tracking si no existe
        if via not in self.vehiculos_canvas:
            self.vehiculos_canvas[via] = {}
        
        vehiculos_actuales = set()
        
        # Actualizar/crear vehículos existentes
        for x, y, color, vehiculo_id in vehiculos_moviendo:
            vehiculos_actuales.add(vehiculo_id)
            
            if vehiculo_id in self.vehiculos_canvas[via]:
                # Actualizar posición existente
                canvas_id = self.vehiculos_canvas[via][vehiculo_id]['rect']
                self.canvas.coords(canvas_id, x-8, y-5, x+8, y+5)
                
                # Actualizar flecha si existe
                if 'flecha' in self.vehiculos_canvas[via][vehiculo_id]:
                    flecha_id = self.vehiculos_canvas[via][vehiculo_id]['flecha']
                    self._actualizar_flecha(flecha_id, x, y, via)
            else:
                # Crear nuevo vehículo
                canvas_id = self.canvas.create_rectangle(
                    x-8, y-5, x+8, y+5, 
                    fill=color, outline="black", width=1
                )
                
                # Crear flecha de dirección
                flecha_id = self._crear_flecha(x, y, via)
                
                self.vehiculos_canvas[via][vehiculo_id] = {
                    'rect': canvas_id,
                    'flecha': flecha_id
                }
        
        # Eliminar vehículos que ya no existen
        vehiculos_a_eliminar = []
        for vehiculo_id in self.vehiculos_canvas[via]:
            if vehiculo_id not in vehiculos_actuales:
                # Eliminar del canvas
                self.canvas.delete(self.vehiculos_canvas[via][vehiculo_id]['rect'])
                if 'flecha' in self.vehiculos_canvas[via][vehiculo_id]:
                    self.canvas.delete(self.vehiculos_canvas[via][vehiculo_id]['flecha'])
                vehiculos_a_eliminar.append(vehiculo_id)
        
        for vehiculo_id in vehiculos_a_eliminar:
            del self.vehiculos_canvas[via][vehiculo_id]

    def _crear_flecha(self, x, y, via):
        """Crear flecha de dirección para el vehículo"""
        if via == "NORTE":
            return self.canvas.create_polygon(x, y-8, x-3, y-2, x+3, y-2, 
                                            fill="white", outline="black", width=1)
        elif via == "SUR":
            return self.canvas.create_polygon(x, y+8, x-3, y+2, x+3, y+2, 
                                            fill="white", outline="black", width=1)
        elif via == "ESTE":
            return self.canvas.create_polygon(x+8, y, x+2, y-3, x+2, y+3, 
                                            fill="white", outline="black", width=1)
        elif via == "OESTE":
            return self.canvas.create_polygon(x-8, y, x-2, y-3, x-2, y+3, 
                                            fill="white", outline="black", width=1)

    def _actualizar_flecha(self, flecha_id, x, y, via):
        """Actualizar posición de la flecha"""
        if via == "NORTE":
            self.canvas.coords(flecha_id, x, y-8, x-3, y-2, x+3, y-2)
        elif via == "SUR":
            self.canvas.coords(flecha_id, x, y+8, x-3, y+2, x+3, y+2)
        elif via == "ESTE":
            self.canvas.coords(flecha_id, x+8, y, x+2, y-3, x+2, y+3)
        elif via == "OESTE":
            self.canvas.coords(flecha_id, x-8, y, x-2, y-3, x-2, y+3)

    def _actualizar_semaforo(self, nombre, estado):
        colores = {"rojo": "gray", "amarillo": "gray", "verde": "gray"}
        
        if estado == "ROJO":
            colores["rojo"] = "#e74c3c"
        elif estado == "AMARILLO":
            colores["amarillo"] = "#f1c40f"
        elif estado == "VERDE":
            colores["verde"] = "#2ecc71"
        
        for luz, item_id in self.semaforos[nombre].items():
            self.canvas.itemconfig(item_id, fill=colores[luz])

    def _actualizar_info(self):
        # Actualizar labels
        self.label_estado.config(text=self.estado_actual)
        self.label_ciclos.config(text=str(self.ciclos_completados))
        
        for via, stats in self.estadisticas.items():
            texto = f"Esperando: {stats['esperando']} | Cruzados: {stats['cruzados']}"
            self.labels_stats[via].config(text=texto)
        
        # Programar siguiente actualización
        self.root.after(1000, self._actualizar_info)