from flask import Blueprint, request, jsonify
from services.pagos_service import verificar_poder_pagar_mensualidad_service
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

@mensualidad_bp.route('/verificar_mensualidad', methods=['GET'])
def verificar_mensualidad():
    """
        Endpoint para verificar poder pagar una mensualidad (verifica que no se den los escenarios fallidos de la hu pagar mensualidad), 
        si no se da caso fallido se ejecuta el pago con mp.
    """
    dni_cliente = request.args.get("dni_cliente")
    clase_id = request.args.get("clase_id")
    
    respuesta, status = verificar_poder_pagar_mensualidad_service(dni_cliente, clase_id)
    
    return jsonify(respuesta), status