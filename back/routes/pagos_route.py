from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv
import requests

from utils.operaciones_mp import Access_Token
from services.pagos_service import *
from db.operaciones.pagos.modificar_db import aprobar_pago

pagos_bp = Blueprint("pagos", __name__)

@pagos_bp.route("/pagos", methods=["GET"])
def obtener_pagos():
    respuesta, status = obtener_pagos_service()
    
    return jsonify(respuesta), status

@pagos_bp.route("/pagos/pagar_seleccionados", methods=["POST"])
def pagar_pagos_seleccionados():
    data = request.get_json() or {}
    usuario_id = data.get("usuario_id")
    payment_ids = data.get("payment_ids") or []

    respuesta, status = crear_preferencia_pagos_seleccionados_service(usuario_id, payment_ids)
    return jsonify(respuesta), status

# para hacer el pago primero llaman desde el front para obtener el qr y luego llaman para crear la orden de pago y luego preguntan por el estado del pago hasta que cambie de created
@pagos_bp.route("/pagos/obtenerQR", methods=["GET"])
def obtener_qr_mp():    
    load_dotenv()
    
    QR = os.getenv("QR")
    
    return jsonify(QR), 200

# esto se hace en el endpoint de reservas, cuando se crea la reserva individual
# @pagos_bp.route("/pagos/particular", methods=["POST"])
# def crear_pago_particular():
#     data = request.get_json()
#     usuario_id = data.get("usuario_id")
#     descripcion = data.get("descripcion")
#     # instancia de clase_id
#     instancia_clase_id = data.get("instancia_clase_id")

#     respuesta, status = crear_pago_service_particular(usuario_id, descripcion, instancia_clase_id)

#     return jsonify(respuesta), status

@pagos_bp.route("/webhook/pagoNormal", methods=["POST"])
def crear_pago_particular():
    payload = request.get_json(silent=True) or {}
    print("Payload:", payload)
    data = payload.get("data") or {}
    payment_id = data.get("id")
    if not payment_id:
        return "", 200

    r = requests.get(
        f"https://api.mercadopago.com/v1/payments/{payment_id}",
        headers={"Authorization": f"Bearer {Access_Token}"}
    )
    payment = r.json()

    id_pago = payment.get("external_reference")
    status = payment.get("status")  # approved / pending / rejected 

    print(f"Ext. Ref.: {id_pago} / Payment Status: {status}")

    # Comprobar el estado del pago, y si este es 'approved'
    if status == 'approved':
        cursor = conectarse_db()
        aprobar_pago(id_pago, cursor)
        cursor.connection.commit()
        cursor.connection.close()

    #id_pago, nuevo_estado, cursor
    # cursor = conectarse_db()
    # actualizar_estado_pago(external_reference, status, cursor)
    # cursor.connection.close()
    return "", 200


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