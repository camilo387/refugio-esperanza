# modelos/administrador.py

from modelos.usuario import Usuario

class Administrador(Usuario):

    def __init__(self, nombre, email, telefono):

        super().__init__(nombre, email, telefono)

        self.permisos = [
            "registrar",
            "eliminar",
            "adoptar"
        ]

    def registrar_mascota(self, refugio, mascota):

        refugio.agregar_mascota(mascota)

    def eliminar_mascota(self, refugio, id_mascota):

        refugio.eliminar_mascota(id_mascota)

    def registrar_adoptante(self, refugio, adoptante):

        refugio.registrar_adoptante(adoptante)

    def adoptar_mascota(self, refugio, id_mascota, id_adoptante):

        refugio.adoptar_mascota(
            id_mascota,
            id_adoptante
        )

    def ver_historial_adopciones(self, refugio):

        return refugio.ver_historial_adopciones()