from flask import Blueprint, request, jsonify

from services.notificar_siguiente_service import notificar_siguiente_service

notificaciones_bp = Blueprint('notificaciones', __name__)

@notificaciones_bp.route('/notificaciones/<int:id_clase>', methods=['GET'])
def notificar_siguiente(id_clase):
    """Endpoint para notificar al siguiente usuario en la lista de espera de una clase."""
    respuesta, status = notificar_siguiente_service(id_clase)
    
    return jsonify(respuesta), status 
    
