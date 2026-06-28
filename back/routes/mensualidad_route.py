from flask import Blueprint, request, jsonify
from services.pagos_service import crear_pago_service_mensualidad, verificar_poder_pagar_mensualidad_service
from services.mensualidad_service import cancelar_mensualidad_service, configurar_fin_mensualidad_service, ver_estado_mensualidad_service

mensualidad_bp = Blueprint('mensualidad', __name__)

@mensualidad_bp.route('/mensualidad/configurar_fin_mensualidad', methods=['POST'])
def configurar_fin_mensualidad():
    """Endpoint para configurar el fin de la mensualidad."""
    data = request.get_json()

    dni_cliente = data.get("dni_cliente")    
    fecha_fin = data.get("fecha_fin")    
    mensualidad_id = data.get("id_mensualidad")
    
    respuesta, status = configurar_fin_mensualidad_service(dni_cliente, mensualidad_id, fecha_fin)
    
    return jsonify(respuesta), status

# HU pagar mensualidad
@mensualidad_bp.route('/mensualidad/verificar_mensualidad', methods=['POST'])
def verificar_mensualidad():
    """
        Endpoint para verificar poder pagar una mensualidad (verifica que no se den los escenarios fallidos de la hu pagar mensualidad), 
        si no se da caso fallido se ejecuta el pago con mp.
    """
    data = request.get_json()
    dni_cliente = data.get("dni_cliente")
    clase_id = data.get("clase_id")

    respuesta, status = verificar_poder_pagar_mensualidad_service(dni_cliente, clase_id)
    
    return jsonify(respuesta), status

# HU renovar mensualidad
@mensualidad_bp.route("/mensualidad/renovar_mensualidad", methods=["POST"])
def crear_pago_mensualidad():
    data = request.get_json()
    dni_cliente = data.get("dni_cliente")
    descripcion = data.get("descripcion")
    id_mensualidad = data.get("id_mensualidad")
    
    respuesta, status = crear_pago_service_mensualidad(dni_cliente, descripcion, id_mensualidad)
    if status != 200:
        return jsonify(respuesta), status
    
    respuesta, status = configurar_fin_mensualidad_service(dni_cliente, id_mensualidad)
    
    if status != 200:
        return jsonify(respuesta), status
    
    return jsonify({
        "message": "Pago de mensualidad realizado y fecha de fin configurada correctamente."
    }), 200
    
@mensualidad_bp.route("/mensualidad/ver_estado", methods=["GET"])
def ver_estado_mensualidad():
    """
        Endpoint para verificar el estado de la mensualidad de un usuario.
    """
    dni_cliente = request.args.get("dni_cliente")
    id_mensualidad = request.args.get("id_mensualidad")

    respuesta, status = ver_estado_mensualidad_service(dni_cliente, id_mensualidad)
    
    return jsonify(respuesta), status


@mensualidad_bp.route("/mensualidad/cancelar_mensualidad", methods=["POST"])
def cancelar_mensualidad_route():
    """
        Endpoint para cancelar la mensualidad de un usuario.
    """
    data = request.get_json()
    dni_cliente = data.get("dni_cliente")
    id_mensualidad = data.get("id_mensualidad")

    respuesta, status = cancelar_mensualidad_service(dni_cliente, id_mensualidad)
    
    return jsonify(respuesta), status