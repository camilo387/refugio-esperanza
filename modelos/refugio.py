# modelos/refugio.py

from modelos.adopcion import Adopcion

class Refugio:

    def __init__(
        self,
        nombre,
        direccion,
        telefono
    ):

        self.id = 1
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono

        self.mascotas = []
        self.adoptantes = []
        self.adopciones = []

    def agregar_mascota(self, mascota):

        self.mascotas.append(mascota)

    def eliminar_mascota(self, id_mascota):

        for mascota in self.mascotas:

            if mascota.id == id_mascota:

                self.mascotas.remove(mascota)
                return True

        return False

    def listar_mascotas_disponibles(self):

        disponibles = []

        for mascota in self.mascotas:

            if mascota.esta_disponible():

                disponibles.append(mascota)

        return disponibles

    def registrar_adoptante(self, adoptante):

        self.adoptantes.append(adoptante)

    def buscar_adoptante(self, id_adoptante):

        for adoptante in self.adoptantes:

            if adoptante.id == id_adoptante:

                return adoptante

        return None

    def buscar_mascota(self, id_mascota):

        for mascota in self.mascotas:

            if mascota.id == id_mascota:

                return mascota

        return None

    def adoptar_mascota(
        self,
        id_mascota,
        id_adoptante
    ):

        mascota = self.buscar_mascota(id_mascota)

        adoptante = self.buscar_adoptante(id_adoptante)

        if mascota and adoptante:

            if mascota.esta_disponible():

                adopcion = Adopcion(
                    mascota,
                    adoptante,
                    "Adopción realizada"
                )

                adopcion.registrar()

                self.adopciones.append(adopcion)

                return adopcion

        return None

    def ver_historial_adopciones(self):

        return self.adopciones