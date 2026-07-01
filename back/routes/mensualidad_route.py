from flask import Blueprint, request, jsonify
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_dni
from services import _controlar_errores_query
from services.pagos_service import crear_pago_service_mensualidad, verificar_poder_pagar_mensualidad_service
from services.mensualidad_service import cancelar_mensualidad_service, configurar_fin_mensualidad_service, obtener_mensualidad_service, obtener_mensualidad_usuario_service, renovar_mensualidad_service, ver_estado_mensualidad_service, obtener_todas_las_mensualidades_usuario_service

mensualidad_bp = Blueprint('mensualidad', __name__)

@mensualidad_bp.route('/mensualidad', methods=['GET'])
def get_mensualidad():
    """
        Endpoint para obtener todas las mensualidades.
    """

    respuesta, status = obtener_mensualidad_service()
    
    return jsonify(respuesta), status

@mensualidad_bp.route('/mensualidad/<int:dni_cliente>', methods=['GET'])
def get_mensualidad_usuario(dni_cliente):
    """
        Endpoint para obtener la mensualidad de un usuario.
    """

    respuesta, status = obtener_mensualidad_usuario_service(dni_cliente)
    
    return jsonify(respuesta), status

@mensualidad_bp.route('/mensualidad/configurar_fin_mensualidad', methods=['PUT'])
def configurar_fin_mensualidad():
    """Endpoint para configurar el fin de la mensualidad."""
    data = request.get_json()

    dni_cliente = data.get("dni_cliente")    
    fecha_fin = data.get("fecha_fin")    
    mensualidad_id = data.get("id_mensualidad")
    
    if not mensualidad_id:
        return jsonify({
            "error": "Debe proporcionar el id de la mensualidad."
        }), 407
    
    respuesta, status = configurar_fin_mensualidad_service(dni_cliente, mensualidad_id, fecha_fin)
    
    return jsonify(respuesta), status

# HU pagar mensualidad
@mensualidad_bp.route('/mensualidad/pagar_mensualidad', methods=['POST'])
def pagar_mensualidad():
    """
        Endpoint para verificar poder pagar una mensualidad (verifica que no se den los escenarios fallidos de la hu pagar mensualidad), 
        si no se da caso fallido se ejecuta el pago con mp.
    """
    data = request.get_json()
    usuario_id = data.get("usuario_id")
    clase_id = data.get("clase_id")

    respuesta, status = verificar_poder_pagar_mensualidad_service(usuario_id, clase_id)
    
    return jsonify(respuesta), status

# HU renovar mensualidad
@mensualidad_bp.route("/mensualidad/renovar_mensualidad", methods=["PUT"])
def crear_pago_mensualidad():
    data = request.get_json()
    dni_cliente = data.get("dni_cliente")
    descripcion = data.get("descripcion")
    id_mensualidad = data.get("id_mensualidad")
    
    respuesta, status = renovar_mensualidad_service(dni_cliente, id_mensualidad, descripcion)
    
    return jsonify(respuesta), status
    
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


@mensualidad_bp.route("/mensualidad/ver_mensualidades_usuario", methods=["GET"])
def ver_mensualidades_usuario():
    """
        Endpoint para obtener todas las mensualidades de un usuario.
    """
    data = request.get_json()
    dni_cliente = data.get("dni_usuario")
    respuesta, status = obtener_todas_las_mensualidades_usuario_service(dni_cliente)
    
    return jsonify(respuesta), status