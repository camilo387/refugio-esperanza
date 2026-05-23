# modelos/adoptante.py

import uuid
from datetime import datetime

class Adoptante:

    def __init__(
        self,
        nombre,
        identificacion,
        telefono,
        email,
        direccion
    ):

        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.identificacion = identificacion
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.fecha_registro = datetime.now()

    def actualizar_datos(
        self,
        telefono,
        email,
        direccion
    ):

        self.telefono = telefono
        self.email = email
        self.direccion = direccion

    def solicitar_adopcion(self, id_mascota):

        return f"Solicitud enviada para la mascota {id_mascota}"

    def to_dict(self):

        return {
            "id": self.id,
            "nombre": self.nombre,
            "identificacion": self.identificacion,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion,
            "fecha_registro": str(self.fecha_registro)
        }