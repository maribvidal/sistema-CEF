from flask import Blueprint, request, jsonify
from services.mensualidad_service import configurar_fin_mensualidad_service

mensualidad_bp = Blueprint('mensualidad', __name__)

@mensualidad_bp.route('/configurar_fin_mensualidad', methods=['POST'])
def configurar_fin_mensualidad():
    """Endpoint para configurar el fin de la mensualidad."""
    data = request.get_json()

    dni_cliente = data.get("dni_cliente")    
    fecha_fin = data.get("fecha_fin")    
    mensualidad_id = data.get("id_mensualidad")
    
    respuesta, status = configurar_fin_mensualidad_service(dni_cliente, mensualidad_id, fecha_fin)
    
    return jsonify(respuesta), status