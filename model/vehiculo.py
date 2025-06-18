# vehiculo.py
import random
import time
from dataclasses import dataclass
from typing import List

@dataclass
class Vehiculo:
    def __init__(self, direccion, id_vehiculo=None):
        self.direccion = direccion
        self.id = id_vehiculo or random.randint(1000, 9999)
        self.tiempo_llegada = time.time()
        self.tiempo_salida = None
        self.posicion_x = 0
        self.posicion_y = 0
        self.velocidad = random.uniform(2, 20) 
        self.color = random.choice(['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6'])
        self.puede_moverse = False  
        self.en_interseccion = False 
        
        self._establecer_posicion_inicial()
    
    def _establecer_posicion_inicial(self):
        if self.direccion == "NORTE":
            self.posicion_x = 250
            self.posicion_y = 50
        elif self.direccion == "SUR":
            self.posicion_x = 250
            self.posicion_y = 450
        elif self.direccion == "ESTE":
            self.posicion_x = 450
            self.posicion_y = 250
        elif self.direccion == "OESTE":
            self.posicion_x = 50
            self.posicion_y = 250
    
    def puede_avanzar(self, estado_semaforo):
        """Determina si el vehículo puede moverse según el estado del semáforo"""
        if self.en_interseccion:
            return True
        return estado_semaforo == "VERDE"
    
    def esta_en_zona_parada(self):
        """Determina si el vehículo está en la zona donde debe parar por el semáforo"""
        zona_parada = 30
        
        if self.direccion == "NORTE" and self.posicion_y >= 190 - zona_parada and self.posicion_y < 190:
            return True
        elif self.direccion == "SUR" and self.posicion_y <= 310 + zona_parada and self.posicion_y > 310:
            return True
        elif self.direccion == "ESTE" and self.posicion_x <= 310 + zona_parada and self.posicion_x > 310:
            return True
        elif self.direccion == "OESTE" and self.posicion_x >= 190 - zona_parada and self.posicion_x < 190:
            return True
        
        return False
    
    def actualizar_estado_interseccion(self):
        """Actualiza si el vehículo está en la intersección"""
        if (self.direccion == "NORTE" and self.posicion_y >= 190 and self.posicion_y <= 310) or \
           (self.direccion == "SUR" and self.posicion_y >= 190 and self.posicion_y <= 310) or \
           (self.direccion == "ESTE" and self.posicion_x >= 190 and self.posicion_x <= 310) or \
           (self.direccion == "OESTE" and self.posicion_x >= 190 and self.posicion_x <= 310):
            self.en_interseccion = True
        else:
            self.en_interseccion = False
    
    def mover(self, estado_semaforo):
        """Mueve el vehículo solo si puede avanzar"""
        self.actualizar_estado_interseccion()
        
        # Si está en zona de parada y el semáforo no permite avanzar, no se mueve
        if self.esta_en_zona_parada() and not self.puede_avanzar(estado_semaforo):
            return False  # No se movió
        
        # Mover el vehículo
        if self.direccion == "NORTE":
            self.posicion_y += self.velocidad
        elif self.direccion == "SUR":
            self.posicion_y -= self.velocidad
        elif self.direccion == "ESTE":
            self.posicion_x -= self.velocidad
        elif self.direccion == "OESTE":
            self.posicion_x += self.velocidad
        
        return True
    
    def ha_salido_de_pantalla(self):
        return (self.posicion_x < -20 or self.posicion_x > 520 or 
                self.posicion_y < -20 or self.posicion_y > 520)
    
    def tiempo_espera(self):
        return time.time() - self.tiempo_llegada
    
    def __str__(self):
        return f"Vehículo {self.id} en {self.direccion}"

class GeneradorVehiculos:
    def __init__(self):
        self.contador_id = 1000
        self.ultima_generacion = {via: time.time() for via in ["NORTE", "SUR", "ESTE", "OESTE"]}
        self.intervalo_generacion = 1.0  
    
    def generar_vehiculo(self, direccion):
        ahora = time.time()
        if ahora - self.ultima_generacion[direccion] >= self.intervalo_generacion:
            self.ultima_generacion[direccion] = ahora
            self.contador_id += 1
            return Vehiculo(direccion, self.contador_id)
        return None
