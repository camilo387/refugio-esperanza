from flask import Flask, render_template, request, redirect

import os

from werkzeug.utils import secure_filename

# =========================================================
# MODELOS
# =========================================================

from modelos.mascota import Mascota

# =========================================================
# BASE DE DATOS
# =========================================================

from database.mascotas_db import *
from database.conexion import conexion, cursor

# =========================================================
# INICIAR FLASK
# =========================================================

app = Flask(__name__)

# =========================================================
# PAGINA PRINCIPAL
# =========================================================

@app.route("/")
def inicio():

    mascotas = obtener_mascotas()

    # ======================================
    # SOLO MASCOTAS DISPONIBLES
    # ======================================

    mascotas_disponibles = [

        mascota

        for mascota in mascotas

        if mascota.estado == "Disponible"

    ]

    # ======================================
    # CONTAR ADOPCIONES APROBADAS
    # ======================================

    cursor.execute(

        """

        SELECT COUNT(*)

        FROM adopciones

        WHERE estado = 'Aprobada'

        """

    )

    total_adopciones = cursor.fetchone()[0]

    return render_template(

        "index.html",

        mascotas=mascotas_disponibles,

        total_adopciones=total_adopciones

    )

# =========================================================
# PAGINA ANIMALES
# =========================================================

@app.route("/animales")
def animales():

    tipo = request.args.get("tipo")

    mascotas = obtener_mascotas()

    # ======================================
    # FILTRO POR TIPO
    # ======================================

    if tipo and tipo != "Todos":

        mascotas = [

            mascota

            for mascota in mascotas

            if mascota.tipo.lower() == tipo.lower()

        ]

    return render_template(

        "animales.html",

        mascotas=mascotas,

        tipo_actual=tipo

    )

# =========================================================
# PANEL ADMIN
# =========================================================

@app.route("/admin")
def admin():

    mascotas = obtener_mascotas()

    return render_template(

        "admin.html",

        mascotas=mascotas

    )

# =========================================================
# FORMULARIO REGISTRAR
# =========================================================

@app.route("/registrar-mascota")
def formulario_mascota():

    return render_template(

        "registrar_mascota.html"

    )

# =========================================================
# GUARDAR MASCOTA
# =========================================================

@app.route("/guardar-mascota", methods=["POST"])
def guardar_mascota():

    nombre = request.form["nombre"]

    edad = request.form["edad"]

    tipo = request.form["tipo"]

    raza = request.form["raza"]

    estado_salud = request.form["estado_salud"]

    descripcion = request.form["descripcion"]

    # ======================================
    # FOTO
    # ======================================

    foto = request.files["foto"]

    nombre_foto = secure_filename(

        foto.filename

    )

    ruta = os.path.join(

        "static/img/mascotas",

        nombre_foto

    )

    foto.save(ruta)

    # ======================================
    # CREAR OBJETO
    # ======================================

    mascota = Mascota(

        None,
        nombre,
        edad,
        tipo,
        raza,
        estado_salud,
        descripcion,
        nombre_foto,
        "Disponible"

    )

    # ======================================
    # GUARDAR EN DB
    # ======================================

    insertar_mascota(mascota)

    return redirect("/admin")

# =========================================================
# ELIMINAR MASCOTA
# =========================================================

@app.route("/eliminar/<id>")
def eliminar(id):

    eliminar_mascota(id)

    return redirect("/admin")

# =========================================================
# EDITAR MASCOTA
# =========================================================

@app.route("/editar/<id>")
def editar(id):

    mascotas = obtener_mascotas()

    mascota_encontrada = None

    for mascota in mascotas:

        if str(mascota.id) == str(id):

            mascota_encontrada = mascota

            break

    return render_template(

        "editar.html",

        mascota=mascota_encontrada

    )

# =========================================================
# ACTUALIZAR MASCOTA
# =========================================================

@app.route("/actualizar/<id>", methods=["POST"])
def actualizar(id):

    datos = {

        "nombre": request.form["nombre"],

        "edad": request.form["edad"],

        "tipo": request.form["tipo"],

        "raza": request.form["raza"],

        "estado_salud": request.form["estado_salud"],

        "descripcion": request.form["descripcion"]

    }

    actualizar_mascota(id, datos)

    return redirect("/admin")

# =========================================================
# FORMULARIO ADOPCION
# =========================================================

@app.route("/adoptar/<nombre>")
def adoptar(nombre):

    return render_template(

        "adoptar.html",

        nombre=nombre

    )

# =========================================================
# GUARDAR ADOPCION
# =========================================================

@app.route("/guardar-adopcion", methods=["POST"])
def guardar_adopcion():

    nombre = request.form["nombre"]

    telefono = request.form["telefono"]

    correo = request.form["correo"]

    direccion = request.form["direccion"]

    mascota = request.form["mascota"]

    # ======================================
    # GUARDAR SOLICITUD
    # ======================================

    cursor.execute(

        """

        INSERT INTO adopciones
        (

            nombre,
            telefono,
            correo,
            direccion,
            mascota_nombre,
            estado

        )

        VALUES (%s,%s,%s,%s,%s,%s)

        """,

        (

            nombre,
            telefono,
            correo,
            direccion,
            mascota,
            "Pendiente"

        )

    )

    # ======================================
    # CAMBIAR ESTADO MASCOTA
    # ======================================

    cursor.execute(

        """

        UPDATE mascotas

        SET estado = 'En proceso'

        WHERE LOWER(nombre) = LOWER(%s)

        """,

        (mascota,)

    )

    conexion.commit()

    return redirect("/")

# =========================================================
# VER SOLICITUDES
# =========================================================

@app.route("/solicitudes")
def solicitudes():

    cursor.execute(

        """

        SELECT *

        FROM adopciones

        """

    )

    solicitudes = cursor.fetchall()

    return render_template(

        "solicitudes.html",

        solicitudes=solicitudes

    )

# =========================================================
# APROBAR ADOPCION
# =========================================================

@app.route("/aprobar-adopcion/<id>/<mascota>")
def aprobar_adopcion(id, mascota):

    # ======================================
    # CAMBIAR ESTADO SOLICITUD
    # ======================================

    cursor.execute(

        """

        UPDATE adopciones

        SET estado = 'Aprobada'

        WHERE id = %s

        """,

        (id,)

    )

    # ======================================
    # CAMBIAR ESTADO MASCOTA
    # ======================================

    cursor.execute(

        """

        UPDATE mascotas

        SET estado = 'Adoptado'

        WHERE LOWER(nombre) = LOWER(%s)

        """,

        (mascota,)

    )

    conexion.commit()

    return redirect("/solicitudes")

# =========================================================
# CAMBIAR ESTADO TRATAMIENTO
# =========================================================

@app.route("/tratamiento/<id>")
def tratamiento(id):

    # ======================================
    # OBTENER ESTADO ACTUAL
    # ======================================

    cursor.execute(

        """

        SELECT estado, estado_anterior

        FROM mascotas

        WHERE id = %s

        """,

        (id,)

    )

    mascota = cursor.fetchone()

    estado_actual = mascota[0]

    estado_anterior = mascota[1]

    # ======================================
    # SI YA ESTA EN TRATAMIENTO
    # VOLVER AL ESTADO ANTERIOR
    # ======================================

    if estado_actual == "En tratamiento":

        nuevo_estado = estado_anterior

        cursor.execute(

            """

            UPDATE mascotas

            SET estado = %s,
                estado_anterior = NULL

            WHERE id = %s

            """,

            (

                nuevo_estado,
                id

            )

        )

    # ======================================
    # SI NO ESTA EN TRATAMIENTO
    # GUARDAR ESTADO ANTERIOR
    # ======================================

    else:

        cursor.execute(

            """

            UPDATE mascotas

            SET estado = 'En tratamiento',
                estado_anterior = %s

            WHERE id = %s

            """,

            (

                estado_actual,
                id

            )

        )

    conexion.commit()

    return redirect("/admin")

# =========================================================
# EJECUTAR FLASK
# =========================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )