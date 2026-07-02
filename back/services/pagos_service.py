import time

from db.operaciones.mensualidades.borrar_db import borrar_reservas_mensualidad
from db.operaciones.clase_tener_mensualidad.borrar_db import borrar_clase_tener_mensualidad
from db.operaciones.mensualidades.consultar_db import verificar_usuario_tenga_mensualidad_clase, verificar_disponibilidad_usuario
from db.operaciones.clase_tener_mensualidad.insertar_db import insertar_clase_tener_mensualidad
from db.operaciones.pago_pagar_clase.borrar_db import borrar_pago_pagar_clase
from db.operaciones.clases.consultar_db import consultar_clase_por_id_instancia
from db.operaciones.mensualidades.insertar_db import insertar_mensualidad, insertar_reservas_mensualidad
from utils.modulo_manejo_listas import revisar_cupos_disponible_abonado, revisar_si_hay_cupos
from db.operaciones.clase_tener_mensualidad.consultar_db import consultar_montos_mensualidad
from db.operaciones.instancias_clases.consultar_db import consultar_instancia_clase_por_id, revisar_validez_cupos
from db.operaciones.pago_pagar_clase.insertar_db import insertar_pago_pagar_clase
from db.operaciones.pago_pagar_mensualidad.insertar_db import insertar_pago_pagar_mensualidad
from db.operaciones.pagos.borrar_db import borrar_pago
from db.operaciones.pagos import verificar_existencia_pago_por_id, actualizar_estado_pago, verificar_estado_pago_por_id, insertar_pago
from utils.operaciones_mp import crear_preferencia_checkout_pro
from db.operaciones import listar_pagos, consultar_clase_por_id, verificar_usuario_tenga_mensualidad, borrar_mensualidad, borrar_pago_pagar_mensualidad
from db.operaciones.pagos.consultar_db import consultar_pagos_de_usuario
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.info_mensualidad.consultar_db import comprobar_existe_info_mensualidad
from db.operaciones.info_mensualidad.modificar_db import cambiar_estado_info_mensualidad
from db.operaciones.info_mensualidad.insertar_db import insertar_info_mensualidad
import time

from utils.operaciones_mp import crear_preferencia_checkout_pro
from services import _controlar_errores_query,_controlar_errores_query_sin_none, _msj_error_helper, _msj_exito_helper

# esto lo podria replantear como que las inserciones se hagan luego del pago asi no tengo que andar haciendo rollbacks
def verificar_poder_pagar_mensualidad_service(usuario_id, clase_id):
    cursor = conectarse_db()
    
    if not usuario_id or not clase_id:
        cursor.connection.close()
        return {
            "error": "Faltan datos requeridos para verificar el pago de la mensualidad."
        }, 400
    
    # verificar que el usuario tenga esa mensualidad
    verificacion = verificar_usuario_tenga_mensualidad_clase(usuario_id, clase_id, cursor)
    control = _controlar_errores_query_sin_none(verificacion, 500, "El usuario ya se encuentra registrado en esa clase a ese mismo horario.", 401, cursor)
    if control is not None:
        return control
    
    verificacion = verificar_disponibilidad_usuario(usuario_id, clase_id, cursor)
    print("verificacion", verificacion)
    control = _controlar_errores_query_sin_none(verificacion, 500, "El usuario no tiene disponibilidad para inscribirse en esa clase.", 401, cursor)
    if control is not None:
        return control

    clase = consultar_clase_por_id(clase_id, cursor)
    print("clase", clase)
    control = _controlar_errores_query(clase, 500, "No se encontro la clase asociada a la mensualidad.", 404, cursor)
    if control is not None:
        return control

    dict_cupos = revisar_si_hay_cupos(clase['data']['id'], cursor) # me devuelve { inst_clase_id: numero_cupos }
    # revisar que las instancias de clase que me manda este dentro del rango de la mensualidad que se va a crear
    print("dict_cupos", dict_cupos)
    
    dict_cupos = revisar_validez_cupos(dict_cupos, cursor)
    print("dict_cupos despues de revisar validez", dict_cupos)
    # valores de prueba en postman:
    # {
    #     "dni_cliente": 8,
    #     "clase_id": 3
    # }
    
    hay_cupos = revisar_cupos_disponible_abonado(dict_cupos)
    
    if not hay_cupos:
        # aca lo tendria que mandar el front un mensaje diciendo que no hay cupos disponibles que si quiere incribirse a la lista de espera de abonados y de ahi que llame al otro endpoint
        cursor.connection.close()
        return {
            "status": "no_cupos",
            "message": "No se pudieron agregar nuevas reservas por falta de cupos."
        }, 501
    
    # generar mensualidad y mandar el id como retorno
    respuesta = insertar_mensualidad(usuario_id, cursor)
    control = _controlar_errores_query(respuesta, 500, "No se pudo crear la mensualidad.", 400, cursor)
    if control is not None:
        return control
    
    id_mensualidad = int(respuesta['data'])

    # -- Esto lo puedo mover al nuevo endpoint, una vez que se aprobó el pago que se cree todo.
    respuesta = insertar_clase_tener_mensualidad(respuesta['data'], clase_id, cursor)
    control = _controlar_errores_query(respuesta, 500, "No se pudo asociar la mensualidad a la clase.", 400, cursor)
    if control is not None:
        respuesta = borrar_mensualidad(respuesta['data'], cursor)
        
        control2 = _controlar_errores_query_sin_none(respuesta, 500, "Error al borrar la mensualidad.", 400, cursor)
        if control2 is not None:
            return control2
        
        return control
    
    # Revisar si ya existe la mensualidad.
    # - Si ya existe la mensualidad, entonces no tengo que crear reservas ni nada...
    # - Poner el renovar en True, así desde el otro endpoint no se crea nada mas
    # - Un Info_Mensualidad debería corresponder a una sola mensualidad nada mas
    respuesta = comprobar_existe_info_mensualidad(id_mensualidad, cursor)
    print(respuesta)
    if respuesta: # Si es true que existe
        cambiar_estado_info_mensualidad(id_mensualidad, cursor)
    else:
        insertar_info_mensualidad(id_mensualidad, clase_id, cursor)
    
    # -- Esto lo puedo mover al nuevo endpoint, una vez que se aprobó el pago que se cree todo.
    respuesta = insertar_reservas_mensualidad(usuario_id, dict_cupos, cursor)
    control = _controlar_errores_query(respuesta, 500, "No se pudo insertar las reservas de la mensualidad.", 400, cursor)
    if control is not None:
        respuesta = borrar_clase_tener_mensualidad(id_mensualidad, cursor)
        control2 = _controlar_errores_query_sin_none(respuesta, 500, "Error al borrar la clase tener mensualidad.", 400, cursor)
        if control2 is not None:
            return control2
        
        respuesta = borrar_mensualidad(id_mensualidad, cursor)
        control3 = _controlar_errores_query_sin_none(respuesta, 500, "Error al borrar la mensualidad.", 400, cursor)
        if control3 is not None:
            return control3
        
        return control

    cursor.connection.close()
    
    respuesta, status = crear_pago_service_mensualidad(usuario_id, "Pago de mensualidad", id_mensualidad)
    # para pruebas:
    #status = 200
    # time.sleep(10)
    
    if status != 200:
        cursor_cleanup = conectarse_db()
        
        respuesta = borrar_reservas_mensualidad(id_mensualidad, cursor_cleanup)
        control = _controlar_errores_query_sin_none(respuesta, 500, "Error al borrar las reservas de la mensualidad.", 400, cursor_cleanup)
        if control is not None:
            return control
        
        respuesta = borrar_clase_tener_mensualidad(id_mensualidad, cursor_cleanup)
        control = _controlar_errores_query_sin_none(respuesta, 500, "Error al borrar la clase tener mensualidad.", 400, cursor_cleanup)
        if control is not None:
            return control
        
        respuesta = borrar_mensualidad(id_mensualidad, cursor_cleanup)
        
        control = _controlar_errores_query_sin_none(respuesta, 500, "Error al borrar la mensualidad.", 400, cursor_cleanup)
        if control is not None:
            return control
        
        cursor_cleanup.connection.close()

    preference_id = respuesta["data"]
    
    # Devolvemos la estructura que espera Vue
    return {
        "status": "success",
        "message": "Orden de pago creada exitosamente.",
        "preference_id": preference_id
    }, 200

def obtener_pagos_service():
    cursor = conectarse_db()
    pagos = listar_pagos(cursor)
    
    cursor.connection.close()
    
    control = _controlar_errores_query(pagos, 500, "Error al obtener pagos.", 400, cursor)
    if control is not None:
        return control

    return pagos['data'], 200

def crear_preferencia_pagos_seleccionados_service(usuario_id, payment_ids):
    cursor = conectarse_db()

    if not usuario_id or not payment_ids:
        cursor.connection.close()
        return {
            "error": "Faltan datos requeridos para crear la preferencia de pago."
        }, 400

    pagos_usuario = consultar_pagos_de_usuario(usuario_id, cursor)
    control = _controlar_errores_query(pagos_usuario, 500, "No se pudieron obtener los pagos del usuario.", 400, cursor)
    if control is not None:
        return control

    pagos_disponibles = pagos_usuario["data"] or []
    ids_solicitados = []
    for payment_id in payment_ids:
        try:
            ids_solicitados.append(int(payment_id))
        except (TypeError, ValueError):
            cursor.connection.close()
            return {
                "error": "Uno de los pagos seleccionados no es válido."
            }, 400

    pagos_seleccionados = [p for p in pagos_disponibles if int(p.get("id", 0)) in ids_solicitados]

    if len(pagos_seleccionados) != len(set(ids_solicitados)):
        cursor.connection.close()
        return {
            "error": "Uno o más pagos seleccionados no pertenecen al usuario."
        }, 403

    estados_permitidos = {"pending", "created"}
    pagos_no_pagables = [p for p in pagos_seleccionados if str(p.get("estado", "")).lower() not in estados_permitidos]
    if pagos_no_pagables:
        cursor.connection.close()
        return {
            "error": "Sólo se pueden pagar pagos pendientes."
        }, 409

    total = sum(float(p.get("monto", 0) or 0) for p in pagos_seleccionados)
    if total <= 0:
        cursor.connection.close()
        return {
            "error": "El total seleccionado no es válido."
        }, 400

    descripcion = f"Pago de {len(pagos_seleccionados)} comprobantes"
    item = {
        "title": "Pagos seleccionados",
        "quantity": 1,
        "unit_measure": "unit",
        "external_categories": [{"id": "selected-payments"}]
    }
    external_reference = f"PAGOS-{usuario_id}-{int(time.time())}"

    respuesta_json = crear_preferencia_checkout_pro(external_reference, total, descripcion, item)
    control = _controlar_errores_query(respuesta_json, 500, "Error al crear la preferencia de pago en MercadoPago.", 400, cursor)
    if control is not None:
        return control

    cursor.connection.close()

    return {
        "message": "Preferencia de pago creada exitosamente.",
        "preference_id": respuesta_json.get("data", {}).get("id"),
        "total": total,
        "cantidad": len(pagos_seleccionados)
    }, 200

def crear_pago_service_mensualidad(usuario_id, descripcion, id_mensualidad):
    cursor = conectarse_db()
    
    if not usuario_id or not descripcion or not id_mensualidad:
        cursor.connection.close()
        return {
            "error": "Faltan datos requeridos para crear el pago."
        }, 400
    
    # verificar que el usuario tenga esa mensualidad
    verificacion = verificar_usuario_tenga_mensualidad(usuario_id, id_mensualidad, cursor)
    control = _controlar_errores_query(verificacion, 500, "El usuario no tiene esta mensualidad.", 400, cursor)
    if control is not None:
        return control

    # verificar montos de clases de la mensualidad
    montos_mensualidad = consultar_montos_mensualidad(id_mensualidad, cursor)
    control = _controlar_errores_query(montos_mensualidad, 500, "No se pudo consultar los montos de la mensualidad.", 400, cursor)
    if control is not None:
        return control
    
    if montos_mensualidad['data']['total'] is None:
        # pasa cuando por ejemplo existe la clase 3 pero las instancias de clase que existen
        # no tienen la fecha dentro del rango de la mensualidad
        cursor.connection.close()
        return {
            "error": "No existen instancias de clase asignables para esta mensualidad."
        }, 406

    # Crear el pago en la base de datos con estado "pending"
    pago = insertar_pago(montos_mensualidad['data']['total'] * 0.7, usuario_id, cursor)
    
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
    
    resultado = insertar_pago_pagar_mensualidad(id_pago, id_mensualidad, cursor)
    control = _controlar_errores_query(resultado, 500, "No se pudo crear el pago pagar mensualidad.", 400, cursor)
    if control is not None:
        respuesta = borrar_pago(cursor, id_pago)
        control2 = _controlar_errores_query_sin_none(respuesta, 500, "Error al borrar el pago.", 400, cursor)
        if control2 is not None:
            return control2
        return control
    
    item = {
        "title": "Mensualidad",
        "unit_price": str(montos_mensualidad['data']['total'] * 0.7), # se le descuenta el 30% por tener la mensualidad
        "quantity": 1,
        "unit_measure": "unit",
        "external_categories": [
        {"id": "gym-membership"}
        ]
    }
    
    # aca no estoy seguro si es con o sin none
    print(" > Antes de hacer el crear_preferencia_checkout_pro")
    respuesta_json = crear_preferencia_checkout_pro(id_pago, montos_mensualidad['data']['total'] * 0.7, descripcion, item)
    preference_id = respuesta_json["data"]
    #print("respuesta_json", respuesta_json)
    print(" > Después de hacer el crear_preferencia_checkout_pro")
    # control = _controlar_errores_query(respuesta_json, 500, "Error al crear la orden de pago en MercadoPago.", 400, cursor)
    # if control is not None:
    #     return control
    
    cursor.connection.close()
    
    print(preference_id["id"])

    return {
        "message": "Preferencia de pago creada exitosamente.",
        "status_mp": respuesta_json.get("status"),
        "data": preference_id["id"]
    }, 200

# funcion anterior de pago con qr:
# def crear_pago_service_mensualidad(usuario_id, descripcion, id_mensualidad):
#     cursor = conectarse_db()
    
#     if not usuario_id or not descripcion or not id_mensualidad:
#         cursor.connection.close()
#         return {
#             "error": "Faltan datos requeridos para crear el pago."
#         }, 400
    
#     # verificar que el usuario tenga esa mensualidad
#     verificacion = verificar_usuario_tenga_mensualidad(usuario_id, id_mensualidad, cursor)
#     control = _controlar_errores_query(verificacion, 500, "El usuario no tiene esta mensualidad.", 400, cursor)
#     if control is not None:
#         return control

#     # verificar montos de clases de la mensualidad
#     montos_mensualidad = consultar_montos_mensualidad(id_mensualidad, cursor)
#     control = _controlar_errores_query(montos_mensualidad, 500, "No se pudo consultar los montos de la mensualidad.", 400, cursor)
#     if control is not None:
#         return control
    
#     if montos_mensualidad['data']['total'] is None:
#         # pasa cuando por ejemplo existe la clase 3 pero las instancias de clase que existen
#         # no tienen la fecha dentro del rango de la mensualidad
#         cursor.connection.close()
#         return {
#             "error": "No existen instancias de clase asignables para esta mensualidad."
#         }, 406

#     # Crear el pago en la base de datos con estado "pending"
#     pago = insertar_pago(montos_mensualidad['data']['total'] * 0.7, usuario_id, cursor)
    
#     control = _controlar_errores_query(pago, 500, "No se pudo crear el pago.", 400, cursor)
#     if control is not None:
#         return control
    
#     id_pago_raw = pago['data']

#     try:
#         id_pago = int(id_pago_raw)
#     except (TypeError, ValueError):
#         cursor.connection.close()
#         return {
#             "error": "El id del pago creado no es válido."
#         }, 500
    
#     resultado = insertar_pago_pagar_mensualidad(id_pago, id_mensualidad, cursor)
#     control = _controlar_errores_query(resultado, 500, "No se pudo crear el pago pagar mensualidad.", 400, cursor)
#     if control is not None:
#         respuesta = borrar_pago(cursor, id_pago)
#         control2 = _controlar_errores_query_sin_none(respuesta, 500, "Error al borrar el pago.", 400, cursor)
#         if control2 is not None:
#             return control2
#         return control
    
#     item = {
#         "title": "Mensualidad",
#         "unit_price": str(montos_mensualidad['data']['total'] * 0.7), # se le descuenta el 30% por tener la mensualidad
#         "quantity": 1,
#         "unit_measure": "unit",
#         "external_categories": [
#         {"id": "gym-membership"}
#         ]
#     }
    
#     # aca no estoy seguro si es con o sin none
#     respuesta_json = crear_orden_qr_mp(id_pago, montos_mensualidad['data']['total'] * 0.7, descripcion, item)
#     print("respuesta_json", respuesta_json)
#     control = _controlar_errores_query(respuesta_json, 500, "Error al crear la orden de pago en MercadoPago.", 400, cursor)
#     if control is not None:
#         return control
    
#     respuesta = consultar_datos_orden_qr_mp(respuesta_json["data"]["id"])
#     print("respuesta", respuesta)
#     control = _controlar_errores_query(respuesta, 500, "Error al consultar los datos de la orden de pago en MercadoPago.", 400, cursor)
#     if control is not None:
#         return control
    
#     while(respuesta['data']['status'] == "created"):
#         time.sleep(2)
#         respuesta = consultar_datos_orden_qr_mp(respuesta_json["data"]["id"])
#         control = _controlar_errores_query(respuesta, 500, "Error al consultar los datos de la orden de pago en MercadoPago.", 400, cursor)
#         if control is not None:
#             return control
        
#     print("respuesta['data']['status']", respuesta['data']['status'])
#     if respuesta['data']['status'] == "expired" or respuesta['data']['status'] == "refunded":
#         respuesta = borrar_pago_pagar_mensualidad(id_pago, id_mensualidad, cursor)
#         control = _controlar_errores_query_sin_none(respuesta, 500,"Error al borrar el pago pagar mensualidad.", 400, cursor)
#         if control is not None:
#             return control
        
#         respuesta = borrar_pago(cursor, id_pago)
#         control = _controlar_errores_query_sin_none(respuesta, 500, "Error al borrar el pago.", 400, cursor)
#         if control is not None:
#             return control

#         cursor.connection.close()
#         return {
#             "error": f"La orden de pago con id {respuesta_json['data']['id']} ha expirado o fue cancelada."
#         }, 400    
    
#     # actuaizar estado del pago
#     res_actualizar = actualizar_estado_pago(id_pago, respuesta['data']['status'], cursor)
    
#     control = _controlar_errores_query_sin_none(res_actualizar, 500, "Error al actualizar el estado del pago.", 400, cursor)
#     if control is not None:
#         return control
    
#     cursor.connection.close()
        
#     return {
#         "message": "Orden de pago creada exitosamente.",
#         "status_mp": respuesta_json.get("status")
#     }, 200    
    
def crear_pago_service_particular(usuario_id, descripcion, instancia_clase_id):
    cursor = conectarse_db()
    
    if not instancia_clase_id or not usuario_id or not descripcion:
        cursor.connection.close()
        return {
            "error": "Faltan datos requeridos para crear el pago."
        }, 400
    
    instancia_clase = consultar_instancia_clase_por_id(instancia_clase_id, cursor)
    control = _controlar_errores_query(instancia_clase, 500, "No se encontro la instancia de clase.", 400, cursor)
    if control is not None:
        return control
    
    # Crear el pago en la base de datos con estado "pending"
    pago = insertar_pago(instancia_clase['data']['monto'], usuario_id, cursor)
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
    
    clase = consultar_clase_por_id_instancia(instancia_clase_id, cursor)
    control = _controlar_errores_query(clase, 500, "No se encontro la clase asociada a la instancia de clase.", 404, cursor)
    if control is not None:
        respuesta = borrar_pago(cursor, id_pago)
        control2 = _controlar_errores_query_sin_none(respuesta, 500, "Error al borrar el pago.", 400, cursor)
        if control2 is not None:
            return control2
        return control
    
    resultado = insertar_pago_pagar_clase(id_pago, clase['data']['id'], cursor)
    
    control = _controlar_errores_query(resultado, 500, "No se pudo crear el pago pagar clase.", 400, cursor)
    if control is not None:
        respuesta = borrar_pago(cursor, id_pago)
        control2 = _controlar_errores_query_sin_none(respuesta, 500, "Error al borrar el pago.", 400, cursor)
        if control2 is not None:
            return control2
        return control
    
    item = {
        "title": "Clase particular",
        "unit_price": str(instancia_clase['data']['monto']),
        "quantity": 1,
        "unit_measure": "unit",
        "external_categories": [{"id": "personal-training"}]
    }
    
    # 1. Llamamos a nuestra nueva función
    respuesta_json = crear_preferencia_checkout_pro(id_pago, instancia_clase['data']['monto'], descripcion, item)
    
    control = _controlar_errores_query(respuesta_json, 500, "Error al crear la preferencia de pago en MercadoPago.", 400, cursor)
    if control is not None:
        return control
   
    # Imprimimos la respuesta en consola para ver QUÉ se quejó Mercado Pago
    print("\n--- RESPUESTA MERCADO PAGO ---")
    print(respuesta_json)
    print("------------------------------\n")

    # Si Mercado Pago no nos devolvió el ID, detenemos el proceso ordenadamente
    if "data" not in respuesta_json or "id" not in respuesta_json.get("data", {}):
        cursor.connection.close()
        return {
            "status": "error",
            "message": "Mercado Pago rechazó la creación de la preferencia.",
            "detalles_mp": respuesta_json
        }, 500

    preference_id = respuesta_json["data"]
    
    cursor.connection.commit()
    cursor.connection.close()
        
    return {
        "message": "Orden de pago creada exitosamente.",
        "data": preference_id["id"] # <--- ESTE ES EL STRING QUE NECESITA VUE.JS
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