from flask import Blueprint, request, jsonify

from services.usuario_service import registrar_usuario_service

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

    respuesta, status = registrar_usuario_service(
        dni,
        nombre,
        apellido,
        contraseña,
        correo,
        telefono,
        genero
    )

    return jsonify(respuesta), status