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

# =========================================================
# INICIAR FLASK
# =========================================================

app = Flask(__name__)

# =========================================================
# PAGINA PRINCIPAL
# =========================================================

@app.route("/")
def inicio():

    return render_template("index.html")

# =========================================================
# PAGINA ANIMALES
# =========================================================

@app.route("/animales")
def animales():

    # ======================================
    # OBTENER FILTRO
    # ======================================

    tipo = request.args.get("tipo")

    # ======================================
    # OBTENER ANIMALES
    # ======================================

    mascotas = obtener_mascotas()

    # ======================================
    # FILTRAR
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
# PANEL ADMINISTRADOR
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

    # ======================================
    # DATOS FORMULARIO
    # ======================================

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

        nombre,
        edad,
        tipo,
        raza,
        estado_salud,
        descripcion,
        nombre_foto

    )

    # ======================================
    # GUARDAR EN POSTGRESQL
    # ======================================

    insertar_mascota(mascota)

    # ======================================
    # REDIRECCION
    # ======================================

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
# EJECUTAR FLASK
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)