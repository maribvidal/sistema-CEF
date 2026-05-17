from flask import Blueprint, request, jsonify

from services.usuario_service import *

usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route("/usuarios", methods=["POST"])
def registrar_usuario():
    data = request.get_json()

    dni = data.get("dni")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    contraseña = data.get("contraseña")
    correo = data.get("correo")
    telefono = data.get("telefono")
    genero = data.get("genero")
    edad = data.get("edad")

    respuesta, status = registrar_usuario_service(
        dni,
        nombre,
        apellido,
        contraseña,
        correo,
        telefono,
        genero,
        edad
    )

    return jsonify(respuesta), status

@usuario_bp.route("/usuarios/<int:usuario_id>/pagos", methods=["GET"])
def listar_pagos_usuario(usuario_id):
    respuesta, status = listar_pagos_usuario_service(usuario_id)

    return jsonify(respuesta), status

@usuario_bp.route("/usuarios/<int:usuario_id>/perfil", methods=["GET"])
def obtener_perfil_usuario(usuario_id):
    respuesta, status = obtener_perfil_usuario_service(usuario_id)

    return jsonify(respuesta), status

@usuario_bp.route("/usuarios/<int:usuario_id>/perfil", methods=["PUT"])
def editar_perfil_usuario(usuario_id):
    data = request.get_json()

    correo = data.get("correo")
    telefono = data.get("telefono")

    respuesta, status = editar_perfil_usuario_service(
        usuario_id,
        correo,
        telefono
    )

    return jsonify(respuesta), status


# endpoint para pruebas

from db.operaciones import listar_usuarios

@usuario_bp.route("/prueba", methods=["GET"])
def obtener_usuarios():
    lista = listar_usuarios()
    return jsonify(lista), 200