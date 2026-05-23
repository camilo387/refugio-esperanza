# modelos/usuario.py

import uuid

class Usuario:

    def __init__(self, nombre, email, telefono):

        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    def iniciar_sesion(self):
        return True

    def cerrar_sesion(self):
        print("Sesión cerrada")

    def ver_mascotas_disponibles(self, mascotas):

        disponibles = []

        for mascota in mascotas:

            if mascota.esta_disponible():
                disponibles.append(mascota)

        return disponibles

    def ver_detalle_mascota(self, mascota):

        return mascota