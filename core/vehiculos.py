class Vehiculo:
    DIRECCIONES = {
        "NORTE": (0, 1),
        "SUR": (0, -1),
        "ESTE": (-1, 0),
        "OESTE": (1, 0)
    }

    def __init__(self, id, via):
        self.id = id
        self.via = via
        self.estado = "esperando"
        self.posicion = 0 
        self.direccion = Vehiculo.DIRECCIONES[via]

    def avanzar(self, paso):
        if self.estado == "avanzando":
            self.posicion += paso
            if self.posicion >= 200:  
                self.estado = "cruzado"
