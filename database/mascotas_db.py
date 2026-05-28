from database.conexion import conexion, cursor

from modelos.mascota import Mascota

# =========================================================
# INSERTAR MASCOTA
# =========================================================

def insertar_mascota(mascota):

    cursor.execute(

        """

        INSERT INTO mascotas
        (

            nombre,
            edad,
            tipo,
            raza,
            estado_salud,
            descripcion,
            foto,
            estado

        )

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

        """,

        (

            mascota.nombre,
            mascota.edad,
            mascota.tipo,
            mascota.raza,
            mascota.estado_salud,
            mascota.descripcion,
            mascota.foto,
            mascota.estado

        )

    )

    conexion.commit()

# =========================================================
# OBTENER MASCOTAS
# =========================================================

def obtener_mascotas():

    cursor.execute(

        """

        SELECT *

        FROM mascotas

        """

    )

    filas = cursor.fetchall()

    mascotas = []

    for fila in filas:

        mascota = Mascota(

            fila[0],  # id
            fila[1],  # nombre
            fila[2],  # edad
            fila[3],  # tipo
            fila[4],  # raza
            fila[5],  # estado_salud
            fila[6],  # descripcion
            fila[7],  # foto
            fila[8]   # estado

        )

        mascotas.append(mascota)

    return mascotas

# =========================================================
# ELIMINAR MASCOTA
# =========================================================

def eliminar_mascota(id):

    cursor.execute(

        """

        DELETE FROM mascotas

        WHERE id = %s

        """,

        (id,)

    )

    conexion.commit()

# =========================================================
# ACTUALIZAR MASCOTA
# =========================================================

def actualizar_mascota(id, datos):

    cursor.execute(

        """

        UPDATE mascotas

        SET

            nombre = %s,
            edad = %s,
            tipo = %s,
            raza = %s,
            estado_salud = %s,
            descripcion = %s

        WHERE id = %s

        """,

        (

            datos["nombre"],
            datos["edad"],
            datos["tipo"],
            datos["raza"],
            datos["estado_salud"],
            datos["descripcion"],
            id

        )

    )

    conexion.commit()