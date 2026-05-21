from flask import Blueprint, request, jsonify
from services.clases_service import (
    listar_salas_service
)

salas_bp = Blueprint('salas', __name__)

@salas_bp.route('/salas', methods=['GET'])
def listar_salas():
    """Este endpoint permite listar todas las salas disponibles 
        en el sistema."""
    respuesta, status = listar_salas_service()
    
    return jsonify(respuesta), status
