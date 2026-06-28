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
    
    QR = os.getenv("QR")
    
    return jsonify(QR), 200

# Para la hu pagar mensualidad voy a suponer que la ruta /verificar_mensualidad se ejecuta para verificar que ya se puede pagar con mp la mensualidad y luego ejecutan esta
# este endpoint se puede llamar para pagar una mensualidad cuando todas las condiciones se cumplen, para renovar la mensualidad, 
# y para pagar una mensualidad cuando el usuario salga de la lista de espera de abonados (ultima escenario en hu pagar mensualidad)
@pagos_bp.route("/pagos/mensualidad", methods=["POST"])
def crear_pago_mensualidad():
    data = request.get_json()
    usuario_id = data.get("usuario_id")
    descripcion = data.get("descripcion")
    id_mensualidad = data.get("id_mensualidad")
    
    respuesta, status = crear_pago_service_mensualidad(usuario_id, descripcion, id_mensualidad)

    return jsonify(respuesta), status

@pagos_bp.route("/pagos/particular", methods=["POST"])
def crear_pago_particular():
    data = request.get_json()
    usuario_id = data.get("usuario_id")
    descripcion = data.get("descripcion")
    clase_id = data.get("clase_id")

    respuesta, status = crear_pago_service_particular(usuario_id, descripcion, clase_id)

    return jsonify(respuesta), status

#
# @pagos_bp.route("/webhook/qr", methods=["POST"])
# def recibir_webhook_qr():
#     data = request.json
    
#     id_pago = data['data']['external_reference']
#     estado_pago = data['data']['status']
    
#     respuesta, status = actualizar_estado_pago_service(id_pago, estado_pago)
    
#     return respuesta, status

# @pagos_bp.route("/pagos/estado/<int:id_pago>", methods=["GET"])
# def obtener_estado_pago(id_pago):
#     respuesta, status = obtener_estado_pago_service(id_pago)
    
#     return jsonify(respuesta), status