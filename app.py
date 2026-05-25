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
    # CONTAR ADOPCIONES
    # ======================================

    cursor.execute(

        "SELECT COUNT(*) FROM adopciones"

    )

    total_adopciones = cursor.fetchone()[0]

    return render_template(

        "index.html",

        mascotas=mascotas,

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
    # FILTRO
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
    # OBJETO
    # ======================================

    mascota = Mascota(

        nombre,
        edad,
        tipo,
        raza,
        estado_salud,
        descripcion,
        nombre_foto

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

        if mascota.id == id:

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
    # GUARDAR ADOPCION
    # ======================================

    cursor.execute(

        """

        INSERT INTO adopciones
        (

            nombre,
            telefono,
            correo,
            direccion,
            mascota_nombre

        )

        VALUES (%s,%s,%s,%s,%s)

        """,

        (

            nombre,
            telefono,
            correo,
            direccion,
            mascota

        )

    )

    # ======================================
    # ELIMINAR MASCOTA ADOPTADA
    # ======================================

    cursor.execute(

        """

        DELETE FROM mascotas

        WHERE nombre = %s

        """,

        (mascota,)

    )

    # ======================================
    # GUARDAR CAMBIOS
    # ======================================

    conexion.commit()

    return redirect("/")

# =========================================================
# EJECUTAR FLASK
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)