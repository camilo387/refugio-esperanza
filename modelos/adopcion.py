# modelos/adopcion.py

import uuid
from datetime import datetime

class Adopcion:

    def __init__(
        self,
        mascota,
        adoptante,
        observaciones=""
    ):

        self.id = str(uuid.uuid4())
        self.fecha_adopcion = datetime.now()
        self.mascota = mascota
        self.adoptante = adoptante
        self.observaciones = observaciones

    def registrar(self):

        self.mascota.cambiar_estado("Adoptada")

    def cancelar(self):

        self.mascota.cambiar_estado("Disponible")

    def get_resumen(self):

        return {
            "id": self.id,
            "fecha": str(self.fecha_adopcion),
            "mascota": self.mascota.nombre,
            "adoptante": self.adoptante.nombre,
            "observaciones": self.observaciones
        }

    def to_dict(self):

        return {
            "id": self.id,
            "fecha_adopcion": str(self.fecha_adopcion),
            "mascota": self.mascota.nombre,
            "adoptante": self.adoptante.nombre,
            "observaciones": self.observaciones
        }