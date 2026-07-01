from flask import Blueprint, request, jsonify
from services.reservas_service import crear_reserva_individual_service, agregar_usuario_a_lista_espera_abonados, cancelar_reserva_service, agregar_usuario_a_lista_espera_individual

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas/<int:reserva_id>/cancelar', methods=['DELETE'])
def cancelar_reserva(reserva_id):
    """Endpoint para cancelar una reserva."""
    respuesta, status = cancelar_reserva_service(reserva_id)
    
    return jsonify(respuesta), status

@reservas_bp.route('/reservas/individual/<int:usuario_id>/<int:inst_clase_id>', methods=['POST'])
def crear_reserva_individual(usuario_id, inst_clase_id):
    """Endpoint para crear una reserva para un usuario individual."""
    respuesta, status = crear_reserva_individual_service(usuario_id, inst_clase_id)
    return jsonify(respuesta), status

@reservas_bp.route('/reservas/individual/<int:usuario_id>/<int:inst_clase_id>/confirmar', methods=['POST'])
def confirmar_agregar_lista_espera(usuario_id, inst_clase_id):
    """Endpoint para crear una reserva para un usuario individual."""
    respuesta, status = agregar_usuario_a_lista_espera_individual(usuario_id, inst_clase_id)
    return jsonify(respuesta), status

@reservas_bp.route('/reservas/abonado/<int:dni_usuario>/<int:clase_id>/confirmar', methods=['POST'])
def crear_reserva_abonado(dni_usuario, clase_id):
    """Endpoint para crear una reserva para un usuario abonado."""
    respuesta, status = agregar_usuario_a_lista_espera_abonados(dni_usuario, clase_id)
    return jsonify(respuesta), status
