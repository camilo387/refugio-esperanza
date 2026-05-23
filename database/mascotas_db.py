from database.conexion import conexion

from modelos.mascota import Mascota

cursor = conexion.cursor()


# =====================================================
# INSERTAR MASCOTA
# =====================================================

def insertar_mascota(mascota):

    sql = """

    INSERT INTO mascotas
    (
        id,
        nombre,
        edad,
        tipo,
        raza,
        estado_salud,
        descripcion,
        foto
    )

    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s
    )

    """

    valores = (

        mascota.id,
        mascota.nombre,
        mascota.edad,
        mascota.tipo,
        mascota.raza,
        mascota.estado_salud,
        mascota.descripcion,
        mascota.foto

    )

    cursor.execute(sql, valores)

    conexion.commit()


# =====================================================
# OBTENER MASCOTAS
# =====================================================

def obtener_mascotas():

    sql = "SELECT * FROM mascotas"

    cursor.execute(sql)

    datos = cursor.fetchall()

    mascotas = []

    for fila in datos:

        mascota = Mascota(

            fila[1],
            fila[2],
            fila[3],
            fila[4],
            fila[5],
            fila[6],
            fila[7]

        )

        mascota.id = fila[0]

        mascotas.append(mascota)

    return mascotas


# =====================================================
# ELIMINAR
# =====================================================

def eliminar_mascota(id):

    sql = "DELETE FROM mascotas WHERE id = %s"

    cursor.execute(sql, (id,))

    conexion.commit()


# =====================================================
# ACTUALIZAR
# =====================================================

def actualizar_mascota(id, datos):

    sql = """

    UPDATE mascotas

    SET

    nombre=%s,
    edad=%s,
    tipo=%s,
    raza=%s,
    estado_salud=%s,
    descripcion=%s

    WHERE id=%s

    """

    valores = (

        datos["nombre"],
        datos["edad"],
        datos["tipo"],
        datos["raza"],
        datos["estado_salud"],
        datos["descripcion"],
        id

    )

    cursor.execute(sql, valores)

    conexion.commit()