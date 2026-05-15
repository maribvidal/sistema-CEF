
from flask import Blueprint, request, jsonify

from services.autenticacion_service import login_service

autenticacion_bp = Blueprint("autenticacion", __name__)

@autenticacion_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    correo = data.get("correo")
    contraseña = data.get("contraseña")

    respuesta, status = login_service(
        correo,
        contraseña
    )

    return jsonify(respuesta), status