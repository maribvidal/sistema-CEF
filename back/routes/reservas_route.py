from flask import Blueprint, request, jsonify
from services.reservas_service import cancelar_reserva_service
reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas/<int:reserva_id>/cancelar', methods=['DELETE'])
def cancelar_reserva(reserva_id):
    """Endpoint para cancelar una reserva."""
    respuesta, status = cancelar_reserva_service(reserva_id)
    
    return jsonify(respuesta), status

@reservas_bp.route('/reservas/<int:id_clase>/confirmar', methods=['POST'])
def confirmar_reserva(id_clase):
    """Endpoint para confirmar una reserva."""
    data = request.get_json()
    id_usuario = data.get("id_usuario")
    
    "respuesta, status = confirmar_reserva_service(id_clase, id_usuario)"
    
    return jsonify(respuesta), status