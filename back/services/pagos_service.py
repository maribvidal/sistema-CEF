from back.db.operaciones.pagos.consultar_db import verificar_existencia_pago_por_id
from back.db.operaciones.pagos.modificar_db import actualizar_estado_pago
from db.operaciones.pagos.insertar_db import insertar_pago
from utils.operaciones_mp import consultar_datos_orden_qr_mp, crear_orden_qr_mp
from db.operaciones import listar_pagos
from db.operaciones.conectar_db import conectarse_db

def obtener_pagos_service():
    cursor = conectarse_db()
    pagos = listar_pagos(cursor)
    print("pagos: ", pagos)

    cursor.connection.close()
    if pagos['status'] == 'error':
        return {
            "error": "Error al obtener pagos.",
            "message": pagos['message']
        }, 500
        
    if pagos['status'] == 'success' and not pagos['data']:
        return {
            "error": "No se encontraron pagos."
        }, 400

    return pagos['data'], 200

def crear_pago_service(monto, usuario_id, descripcion, tipo_pago, id_item):
    cursor = conectarse_db()
    
    if not monto or not usuario_id or not descripcion or not tipo_pago or not id_item:
        cursor.connection.close()
        return {
            "error": "Faltan datos requeridos para crear el pago."
        }, 400
    
    # Crear el pago en la base de datos con estado "pending"
    pago = insertar_pago(monto, usuario_id, cursor)

    if pago['status'] == 'error':
        cursor.connection.close()
        return {
            "error": "Error al crear el pago.",
            "message": pago['message']
        }, 500
    
    if pago['status'] == 'success' and not pago['data']:
        cursor.connection.close()
        return {
            "error": "No se pudo crear el pago."
        }, 400
    
    id_pago = pago['data']
    
    respuesta_json = crear_orden_qr_mp(id_pago, monto, descripcion, tipo_pago, id_item)
    
    if respuesta_json.get('status') == 'error':
        cursor.connection.close()
        return {
            "error": "Error al crear la orden de pago en MercadoPago.",
            "message": respuesta_json.get('message')
        }, 500
        
    return {
        "message": "Orden de pago creada exitosamente.",
        "status_mp": respuesta_json.get("status")
    }, 200    
    
def actualizar_estado_pago_service(id_pago, estado):
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
    
    # actuaizar estado del pago
    res_actualizar = actualizar_estado_pago(id_pago, estado, cursor)
    
    if res_actualizar['status'] == 'error':
        cursor.connection.close()
        return {
            "error": "Error al actualizar el estado del pago.",
            "message": res_actualizar['message']
        }, 500
    
    cursor.connection.close()
    
    return {
        "message": f"Estado del pago con id {id_pago} actualizado a {estado}."
    }, 200