from flask import Blueprint, request, jsonify
from services.permisos_service import cambiar_permiso_service

permisos_bp = Blueprint('permisos', __name__)

@permisos_bp.route('/permisos', methods=['POST'])
def cambiar_permiso():
    """Endpoint para cambiar el permiso de un usuario. 
        Recibe el DNI del usuario y el nuevo permiso en formato JSON."""
    data = request.get_json()
    
    dni = data.get("dni")
    permiso = data.get("rol_id")

    # Acá se llama al servicio correspondiente para cambiar el permiso del usuario
    respuesta, status = cambiar_permiso_service(dni, permiso)

    return jsonify(respuesta), status