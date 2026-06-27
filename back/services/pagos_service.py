import time

from db.operaciones.pago_pagar_clase.insertar_db import insertar_pago_pagar_clase
from db.operaciones.pago_pagar_mensualidad.insertar_db import insertar_pago_pagar_mensualidad
from db.operaciones.pagos.borrar_db import borrar_pago
from db.operaciones.pagos import verificar_existencia_pago_por_id, actualizar_estado_pago, verificar_estado_pago_por_id, insertar_pago
from utils.operaciones_mp import consultar_datos_orden_qr_mp, crear_orden_qr_mp
from db.operaciones import listar_pagos, consultar_clase_por_id
from db.operaciones.conectar_db import conectarse_db

from services import _controlar_errores_query,_controlar_errores_query_sin_none, _msj_error_helper, _msj_exito_helper

def obtener_pagos_service():
    cursor = conectarse_db()
    pagos = listar_pagos(cursor)
    
    cursor.connection.close()
    
    control = _controlar_errores_query(pagos, 500, "Error al obtener pagos.", 400, cursor)
    if control is not None:
        return control

    return pagos['data'], 200

def crear_pago_service_mensualidad(usuario_id, descripcion, id_mensualidad):
    cursor = conectarse_db()
    
    if not usuario_id or not descripcion or not id_mensualidad:
        cursor.connection.close()
        return {
            "error": "Faltan datos requeridos para crear el pago."
        }, 400
    
    #verificar existancia de la mensualidad
    
    # Crear el pago en la base de datos con estado "pending"
    pago = insertar_pago(10000, usuario_id, cursor)
    
    control = _controlar_errores_query(pago, 500, "No se pudo crear el pago.", 400, cursor)
    if control is not None:
        return control
    
    id_pago_raw = pago['data']

    try:
        id_pago = int(id_pago_raw)
    except (TypeError, ValueError):
        cursor.connection.close()
        return {
            "error": "El id del pago creado no es válido."
        }, 500
    
    item = {
        "title": "Mensualidad",
        "unit_price": 10000.00,
        "quantity": 1,
        "unit_measure": "unit",
        "external_categories": [
        {"id": "gym-membership"}
        ]
    }
    
    # aca no estoy seguro si es con o sin none
    respuesta_json = crear_orden_qr_mp(id_pago, 10000, descripcion, item)
    
    control = _controlar_errores_query(respuesta_json, 500, "Error al crear la orden de pago en MercadoPago.", 400, cursor)
    if control is not None:
        return control
    
    respuesta = consultar_datos_orden_qr_mp(respuesta_json["data"]["id"])
    control = _controlar_errores_query(respuesta, 500, "Error al consultar los datos de la orden de pago en MercadoPago.", 400, cursor)
    if control is not None:
        return control
    
    while(respuesta['data']['status'] == "created"):
        time.sleep(2)
        respuesta = consultar_datos_orden_qr_mp(respuesta_json["data"]["id"])

        control = _controlar_errores_query(respuesta, 500, "Error al consultar los datos de la orden de pago en MercadoPago.", 400, cursor)
        if control is not None:
            return control
        
    if respuesta['data']['status'] == "expired" or respuesta['data']['status'] == "refunded":
        borrar_pago(cursor, id_pago)
        
        cursor.connection.close()
        return {
            "error": f"La orden de pago con id {respuesta_json['data']['id']} ha expirado o fue cancelada."
        }, 400    
    
    resultado = insertar_pago_pagar_mensualidad(id_pago, id_mensualidad, cursor)
    
    control = _controlar_errores_query(resultado, 500, "No se pudo crear el pago pagar mensualidad.", 400, cursor)
    if control is not None:
        return control
    
    # actuaizar estado del pago
    res_actualizar = actualizar_estado_pago(id_pago, respuesta['data'], cursor)
    
    control = _controlar_errores_query_sin_none(res_actualizar, 500, "Error al actualizar el estado del pago.", 400, cursor)
    if control is not None:
        return control
    
    cursor.connection.close()
        
    return {
        "message": "Orden de pago creada exitosamente.",
        "status_mp": respuesta_json.get("status")
    }, 200    
    
def crear_pago_service_particular(usuario_id, descripcion, clase_id):
    cursor = conectarse_db()
    
    if not clase_id or not usuario_id or not descripcion:
        cursor.connection.close()
        return {
            "error": "Faltan datos requeridos para crear el pago."
        }, 400
    
    clase = consultar_clase_por_id(clase_id, cursor)
    
    control = _controlar_errores_query(clase, 500, "No se encontro la clase.", 400, cursor)
    if control is not None:
        return control
    
    # Crear el pago en la base de datos con estado "pending"
    pago = insertar_pago(clase['data']['monto'], usuario_id, cursor)
    control = _controlar_errores_query(pago, 500, "No se pudo crear el pago.", 400, cursor)
    if control is not None:
        return control
    
    id_pago_raw = pago['data']

    # lo agregue por errores de tipado que me saltaban
    try:
        id_pago = int(id_pago_raw)
    except (TypeError, ValueError):
        cursor.connection.close()
        return {
            "error": "El id del pago creado no es válido."
        }, 500
    
    item = {
        "title": "Clase particular",
        "unit_price": str(clase['data']['monto']),
        "quantity": 1,
        "unit_measure": "unit",
        "external_categories": [
        {"id": "personal-training"}
        ]
    }
    
    respuesta_json = crear_orden_qr_mp(id_pago, clase['data']['monto'], descripcion, item)
    
    # aca no estoy seguro si es con o sin none
    control = _controlar_errores_query(respuesta_json, 500, "Error al crear la orden de pago en MercadoPago.", 400, cursor)
    if control is not None:
        return control
    
    respuesta = consultar_datos_orden_qr_mp(respuesta_json["data"]["id"])
    control = _controlar_errores_query(respuesta, 500, "Error al consultar los datos de la orden de pago en MercadoPago.", 400, cursor)
    if control is not None:
        return control
    
    while(respuesta['data']['status'] == "created"):
        time.sleep(2)
        respuesta = consultar_datos_orden_qr_mp(respuesta_json["data"]["id"])

        control = _controlar_errores_query(respuesta, 500, "Error al consultar los datos de la orden de pago en MercadoPago.", 400, cursor)
        if control is not None:
            return control
        
    if respuesta['data']['status'] == "expired" or respuesta['data']['status'] == "refunded":
        borrar_pago(cursor, id_pago)
        
        cursor.connection.close()
        return {
            "error": f"La orden de pago con id {respuesta_json['data']['id']} ha expirado o fue cancelada."
        }, 400    
    
    resultado = insertar_pago_pagar_clase(id_pago, clase_id, cursor)
    
    control = _controlar_errores_query(resultado, 500, "No se pudo crear el pago pagar clase.", 400, cursor)
    if control is not None:
        return control
    
    # actuaizar estado del pago
    res_actualizar = actualizar_estado_pago(id_pago, respuesta['data'], cursor)
    
    control = _controlar_errores_query_sin_none(res_actualizar, 500, "Error al actualizar el estado del pago.", 400, cursor)
    if control is not None:
        return control
    
    cursor.connection.close()
        
    return {
        "message": "Orden de pago creada exitosamente.",
        "status_mp": respuesta_json.get("status")
    }, 200    
    
# def actualizar_estado_pago_service(id_pago, estado):
#     cursor = conectarse_db()
    
#     # verificar que el pago exista
#     verificacion = verificar_existencia_pago_por_id(id_pago, cursor)
    
#     if verificacion['status'] == 'error':
#         cursor.connection.close()
#         return {
#             "error": "Error al verificar la existencia del pago.",
#             "message": verificacion['message']
#         }, 500
        
#     if verificacion['status'] == 'success' and not verificacion['data']:
#         cursor.connection.close()
#         return {
#             "error": f"No se encontró un pago con el id {id_pago}."
#         }, 400
    
#     # actuaizar estado del pago
#     res_actualizar = actualizar_estado_pago(id_pago, estado, cursor)
    
#     if res_actualizar['status'] == 'error':
#         cursor.connection.close()
#         return {
#             "error": "Error al actualizar el estado del pago.",
#             "message": res_actualizar['message']
#         }, 500
    
#     cursor.connection.close()
    
#     return {
#         "message": f"Estado del pago con id {id_pago} actualizado a {estado}."
#     }, 200
    
# def obtener_estado_pago_service(id_pago):
    cursor = conectarse_db()
    
    # verificar que el pago exista
    verificacion = verificar_existencia_pago_por_id(id_pago, cursor)
    
    if verificacion['status'] == 'error':
        cursor.connection.close()
        return {
            "error": "Error al verificar la existencia del pago.",
            "message": verificacion['message']
        }, 500
        
    if verificacion['status'] == 'success' and not verificacion['data']:
        cursor.connection.close()
        return {
            "error": f"No se encontró un pago con el id {id_pago}."
        }, 400
    
    # obtener datos de la orden de pago desde MercadoPago
    estado = verificar_estado_pago_por_id(id_pago, cursor)
    
    if estado['status'] == 'error':
        cursor.connection.close()
        return {
            "error": "Error al consultar los datos de la orden de pago en MercadoPago.",
            "message": estado['message']
        }, 500
    
    cursor.connection.close()
    
    return {
        "message": "Datos de la orden de pago obtenidos exitosamente.",
        "data": estado['data']
    }, 200