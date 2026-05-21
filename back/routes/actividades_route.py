from flask import Blueprint, jsonify
from services.clases_service import listar_actividades_service

actividades_bp = Blueprint('actividades', __name__)

@actividades_bp.route('/actividades', methods=['GET'])
def listar_actividades():
    """Endpoint para obtener la lista de actividades."""
    respuesta, status = listar_actividades_service()
    
    return jsonify(respuesta), status
