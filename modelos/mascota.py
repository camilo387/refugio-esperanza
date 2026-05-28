class Mascota:

    def __init__(

        self,
        id,
        nombre,
        edad,
        tipo,
        raza,
        estado_salud,
        descripcion,
        foto,
        estado="Disponible"

    ):

        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.tipo = tipo
        self.raza = raza
        self.estado_salud = estado_salud
        self.descripcion = descripcion
        self.foto = foto
        self.estado = estado

    # =========================================
    # CONVERTIR A DICCIONARIO
    # =========================================

    def to_dict(self):

        return {

            "id": self.id,
            "nombre": self.nombre,
            "edad": self.edad,
            "tipo": self.tipo,
            "raza": self.raza,
            "estado_salud": self.estado_salud,
            "descripcion": self.descripcion,
            "foto": self.foto,
            "estado": self.estado

        }

    # =========================================
    # CAMBIAR ESTADO
    # =========================================

    def cambiar_estado(self, nuevo_estado):

        self.estado = nuevo_estado