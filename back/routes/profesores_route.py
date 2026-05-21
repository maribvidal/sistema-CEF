from flask import Blueprint, jsonify
from services.clases_service import listar_profesores_service

profesores_route = Blueprint('profesores', __name__)

@profesores_route.route('/profesores', methods=['GET'])
def listar_profesores():
    """Endpoint para obtener la lista de profesores."""
    respuesta, status = listar_profesores_service()
    
    return jsonify(respuesta), status
