import uuid

from datetime import datetime


class Mascota:

    def __init__(
        self,
        nombre,
        edad,
        tipo,
        raza,
        estado_salud,
        descripcion,
        foto
    ):

        self.id = str(uuid.uuid4())

        self.nombre = nombre

        self.edad = edad

        self.tipo = tipo

        self.raza = raza

        self.estado_salud = estado_salud

        self.descripcion = descripcion

        self.foto = foto

        self.estado_adopcion = "Disponible"

        self.fecha_registro = datetime.now()

    def cambiar_estado(self, estado):

        self.estado_adopcion = estado

    def esta_disponible(self):

        return self.estado_adopcion == "Disponible"