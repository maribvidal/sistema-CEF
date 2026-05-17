from flask import Blueprint, request, jsonify

from services.pagos_service import *

pagos_bp = Blueprint("pagos", __name__)

@pagos_bp.route("/pagos", methods=["GET"])
def obtener_pagos():
    respuesta, status = obtener_pagos_service()

    return jsonify(respuesta), status