from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv

from services.pagos_service import *

pagos_bp = Blueprint("pagos", __name__)

@pagos_bp.route("/pagos", methods=["GET"])
def obtener_pagos():
    respuesta, status = obtener_pagos_service()
    
    return jsonify(respuesta), status

# para hacer el pago primero llaman desde el front para obtener el qr y luego llaman para crear la orden de pago y luego preguntan por el estado del pago hasta que cambie de created
@pagos_bp.route("/pagos/obtenerQR", methods=["GET"])
def obtener_qr_mp():    
    load_dotenv()
    
    return os.getenv("QR")

@pagos_bp.route("/pagos", methods=["POST"])
def crear_pago():
    data = request.get_json()
    monto = data.get("monto")
    usuario_id = data.get("usuario_id")
    descripcion = data.get("descripcion")
    
    # aca tiene que venir si es 'mensualidad' o 'clase_particular'
    # mensualidad seria para la renovacion o pago de esta y la clase_particular para cuando se llama a pagar con mp en 'confirmar asistencia lista espera individual'
    tipo_pago = data.get("tipo_pago") 
    
    # es necesario el id del item a pagar, sea de la mensualidad o de la instancia clase
    id_item = data.get("id_item")
    
    respuesta, status = crear_pago_service(monto, usuario_id, descripcion, tipo_pago, id_item)
    
    # TODO: Crear la orden, y loopear hasta que se llegue a un 'status_detail' que sea distinto de
    #       'created' o 'partially_refunded'

    return jsonify(respuesta), status

@pagos_bp.route("/webhook/qr", methods=["POST"])
def recibir_webhook_qr():
    data = request.json
    
    id_pago = data['data']['external_reference']
    estado_pago = data['data']['status']
    
    respuesta, status = actualizar_estado_pago_service(id_pago, estado_pago)
    
    return respuesta, status

@pagos_bp.route("/pagos/estado/<int:id_pago>", methods=["GET"])
def obtener_estado_pago(id_pago):
    respuesta, status = obtener_estado_pago_service(id_pago)
    
    return jsonify(respuesta), status