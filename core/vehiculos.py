import random

class Vehiculo:
    def __init__(self, id, via):
        self.id = id
        self.via = via
        self.estado = "esperando"  # puede ser: esperando, avanzando, cruzado
        self.posicion = 0          # posición en la vía (0 = al inicio de la cola)

    def avanzar(self, paso=1):
        if self.estado == "avanzando":
            self.posicion += paso
            if self.posicion >= 100:
                self.estado = "cruzado"


class ColaVehiculos:
    def __init__(self, via, distancia_entre_vehiculos=10):
        self.via = via
        self.vehiculos = []  # lista ordenada FIFO
        self.distancia_entre_vehiculos = distancia_entre_vehiculos

    def agregar_vehiculo(self, vehiculo):
        # Vehículo entra al final de la cola
        if len(self.vehiculos) == 0:
            vehiculo.posicion = 0
        else:
            # Posición atrás del último vehículo
            ultimo = self.vehiculos[-1]
            vehiculo.posicion = max(ultimo.posicion - self.distancia_entre_vehiculos, 0)
        self.vehiculos.append(vehiculo)

    def avanzar_vehiculos(self):
        """
        Avanza los vehículos en cola respetando distancia mínima.
        Solo el primer vehículo puede avanzar libremente.
        Los siguientes avanzan si mantienen distancia.
        """
        if not self.vehiculos:
            return

        # Avanzar primer vehículo si está en estado avanzando
        primero = self.vehiculos[0]
        if primero.estado == "avanzando":
            primero.avanzar()

        # Avanzar siguiente vehículos respetando distancia mínima
        for i in range(1, len(self.vehiculos)):
            actual = self.vehiculos[i]
            delante = self.vehiculos[i-1]
            if actual.estado == "avanzando":
                # Solo avanzar si mantiene distancia mínima con vehículo delante
                if actual.posicion + self.distancia_entre_vehiculos < delante.posicion:
                    actual.avanzar()
                # Si no puede avanzar, se queda en su lugar

        # Remover vehículos que ya cruzaron
        self.vehiculos = [v for v in self.vehiculos if v.estado != "cruzado"]

    def iniciar_avance(self):
        """
        Cambiar estado del primer vehículo a avanzando cuando el semáforo está en verde.
        """
        if self.vehiculos:
            self.vehiculos[0].estado = "avanzando"

    def __str__(self):
        return f"Cola {self.via}: " + ", ".join(f"[ID:{v.id} Pos:{v.posicion} Est:{v.estado}]" for v in self.vehiculos)
