from flask import Blueprint, request, jsonify

from services.usuario_service import (
    registrar_usuario_service,
    listar_pagos_usuario_service,
    obtener_perfil_usuario_service,
    editar_perfil_usuario_service,
)

usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route("/usuarios", methods=["POST"])
def registrar_usuario():
    """Este endpoint registra un nuevo usuario en el sistema. 
        Recibe los datos del usuario en formato JSON, incluyendo 
        su DNI, nombre, apellido, contraseña, fecha de nacimiento, 
        correo electrónico, teléfono y género. Luego, llama al 
        servicio correspondiente para procesar el registro y devuelve 
        una respuesta con el resultado de la operación."""
    data = request.get_json()

    dni = data.get("dni")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    contraseña = data.get("contraseña")
    fecha_nac = data.get("fecha_nac")
    correo = data.get("correo")
    telefono = data.get("telefono")
    genero = data.get("genero")
    rol = data.get("rol")

    respuesta, status = registrar_usuario_service(
        dni,
        nombre,
        apellido,
        contraseña,
        fecha_nac,
        correo,
        telefono,
        genero,
        rol
    )

    return jsonify(respuesta), status

@usuario_bp.route("/usuarios/<int:usuario_id>/pagos", methods=["GET"])
def listar_pagos_usuario(usuario_id):
    """Este endpoint permite listar los pagos realizados 
        por un usuario específico."""
    respuesta, status = listar_pagos_usuario_service(usuario_id)

    return jsonify(respuesta), status

@usuario_bp.route("/usuarios/<int:usuario_id>/perfil", methods=["GET"])
def obtener_perfil_usuario(usuario_id):
    """Este endpoint permite obtener el perfil de un usuario 
        específico."""
    respuesta, status = obtener_perfil_usuario_service(usuario_id)

    return jsonify(respuesta), status

@usuario_bp.route("/usuarios/<int:usuario_dni>/perfil", methods=["PUT"])
def editar_perfil_usuario(usuario_dni):
    """Este endpoint permite editar el perfil de un usuario específico.
        Recibe los datos actualizados del usuario en formato JSON, 
        incluyendo su correo electrónico y teléfono. Luego, llama al 
        servicio correspondiente para procesar la actualización y devuelve 
        una respuesta con el resultado de la operación."""
    data = request.get_json()

    correo = data.get("correo")
    telefono = data.get("telefono")
    print("correo:", correo)
    print("telefono:", telefono)

    respuesta, status = editar_perfil_usuario_service(
        usuario_dni,
        correo,
        telefono
    )

    return jsonify(respuesta), status


# endpoint para pruebas

from db.operaciones import listar_usuarios
from db.operaciones import conectarse_db

@usuario_bp.route("/prueba", methods=["GET"])
def obtener_usuarios():
    cursor = conectarse_db()
    lista = listar_usuarios(cursor)
    cursor.connection.close()
    if lista['status'] == 'error':
        return jsonify({"error": "Error al obtener usuarios", "message": lista['message']}), 500
    if lista['status'] == 'success' and lista['data'] is None:
        return jsonify({"error": "No se encontraron usuarios"}), 404
    return jsonify(lista['data']), 200