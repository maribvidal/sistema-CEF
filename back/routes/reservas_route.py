from flask import Blueprint, request, jsonify
from services.reservas_service import crear_reserva_individual_service, crear_reserva_abonado_service, cancelar_reserva_service

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas/<int:reserva_id>/cancelar', methods=['DELETE'])
def cancelar_reserva(reserva_id):
    """Endpoint para cancelar una reserva."""
    respuesta, status = cancelar_reserva_service(reserva_id)
    
    return jsonify(respuesta), status

@reservas_bp.route('/reservas/individual/<int:usuario_id>/<int:inst_clase_id>/confirmar', methods=['POST'])
def crear_reserva_individual(usuario_id, inst_clase_id):
    """Endpoint para crear una reserva para un usuario individual."""
    respuesta, status = crear_reserva_individual_service(usuario_id, inst_clase_id)
    return jsonify(respuesta), status

@reservas_bp.route('/reservas/abonado/<int:usuario_id>/<int:clase_id>/confirmar', methods=['POST'])
def crear_reserva_abonado(usuario_id, clase_id):
    """Endpoint para crear una reserva para un usuario abonado."""
    respuesta, status = crear_reserva_abonado_service(usuario_id, clase_id)
    return jsonify(respuesta), status
