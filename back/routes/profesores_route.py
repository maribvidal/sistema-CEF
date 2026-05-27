from flask import Blueprint, jsonify
from services.profesores_service import listar_profesores_service, crear_profesor_service

profesores_bp = Blueprint('profesores', __name__)

@profesores_bp.route('/profesores', methods=['GET'])
def listar_profesores():
    """Endpoint para obtener la lista de profesores."""
    respuesta, status = listar_profesores_service()
    
    return jsonify(respuesta), status

@profesores_bp.route('/profesores', methods=['POST'])
def crear_profesor():
    """Endpoint para crear un profesor."""
    data = request.get_json()

    dni = data.get("dni")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    genero = data.get("genero")

    respuesta, status = crear_profesor_service(dni, nombre, apellido, genero)

    return jsonify(respuesta), status
