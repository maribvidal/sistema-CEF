from pprint import pprint
import time

from db.operaciones.pago_pagar_mensualidad.consultar_db import consultar_mensualidad_por_pago_id
from db.operaciones.mensualidades.modificar_db import extender_mensualidad_un_mes
from db.operaciones.clases.consultar_db import consultar_clase_por_id
from db.operaciones.instancias_clases.consultar_db import revisar_validez_cupos
from utils.modulo_manejo_listas import revisar_cupos_disponible_abonado, revisar_si_hay_cupos
from db.operaciones.info_mensualidad.consultar_db import comprobar_existe_info_mensualidad, consultar_info_mensualidad
from db.operaciones.pagos.consultar_db import consultar_pago_por_id
from db.operaciones.pagos.modificar_db import aprobar_pago
from db.operaciones.clase_tener_mensualidad.insertar_db import insertar_clase_tener_mensualidad
from db.operaciones.reservas.borrar_db import borrar_reserva
from db.operaciones.mensualidades.insertar_db import agregar_nuevas_reservas_mensualidad, insertar_reservas_mensualidad
from services.pagos_service import crear_pago_service_mensualidad
from utils.envio_mails import enviar_mail, enviar_mail_vencimiento_mensualidad
from db.operaciones.mensualidades.borrar_db import borrar_mensualidad
from db.operaciones.mensualidades.consultar_db import obtener_mensualidad_activa, obtener_mensualidad_activa_por_usuario, obtener_mensualidad_por_id, obtener_mensualidades_activa, obtener_todas_las_mensualidades_usuario
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_dni, obtener_mensualidad_usuario, verificar_usuario_tiene_mensualidad
from db.operaciones.usuarios import consultar_usuario_por_dni
from db.operaciones.mensualidades import configurar_fin_mensualidad, cancelar_mensualidad, configurar_datos_mensualidad, cambiar_estado_mensualidad
from db.operaciones.clase_tener_mensualidad import borrar_clase_tener_mensualidad
from db.operaciones.usuarios.consultar_db import consultar_cliente_por_dni

from services import _controlar_errores_query,_controlar_errores_query_sin_none, _msj_exito_helper, _msj_error_helper

def obtener_mensualidad_service():
    cursor = conectarse_db()
    
    mensualidades_activas = obtener_mensualidades_activa(cursor)
    control = _controlar_errores_query(mensualidades_activas, 500, "Error al obtener mensualidades activas.", 400, cursor)
    if control is not None:
        return control

    return _msj_exito_helper(mensualidades_activas['data'], cursor)

def obtener_mensualidad_usuario_service(dni_cliente):
    cursor = conectarse_db()
    
    # validar si el usuario existe
    usuario = consultar_usuario_por_dni(dni_cliente, cursor)
    control = _controlar_errores_query(usuario, 500, "No se encontró el usuario.", 400, cursor)
    if control is not None:
        return control
    
    mensualidades_activas = obtener_mensualidad_activa_por_usuario(usuario["data"]["id"], cursor)
    control = _controlar_errores_query(mensualidades_activas, 500, "No se encontraron mensualidades activas para este usuario.", 401, cursor)
    if control is not None:
        return control

    return _msj_exito_helper(mensualidades_activas['data'], cursor)

def configurar_fin_mensualidad_service(dni_cliente, id_mensualidad, fecha_fin = None):
    cursor = conectarse_db()
    
    # validar si el usuario existe
    usuario = consultar_usuario_por_dni(dni_cliente, cursor)
    control = _controlar_errores_query(usuario, 500, "No se encontró el usuario.", 400, cursor)
    if control is not None:
        return control
        
    # obtener la mensualidad del usuario
    mensualidad = obtener_mensualidad_usuario(usuario["data"]["id"], id_mensualidad, cursor)
    control = _controlar_errores_query(mensualidad, 500, "No se encontró la mensualidad del usuario.", 401, cursor)
    if control is not None:
        return control
    
    datos_mensualidad = mensualidad['data']
    
    respuesta = configurar_fin_mensualidad(id_mensualidad, cursor, fecha_fin = fecha_fin)
    control = _controlar_errores_query_sin_none(respuesta, 500, "Error al configurar fin de mensualidad.", 402, cursor)
    if control is not None:
        return control
    
    reservas_agregadas = agregar_nuevas_reservas_mensualidad(id_mensualidad, usuario['data']['id'], cursor)
    print("reservas_agregadas", reservas_agregadas)
    if reservas_agregadas['status'] != "success":
        
        roll_back = configurar_datos_mensualidad(datos_mensualidad, cursor)

        control2 = _controlar_errores_query_sin_none(roll_back, 500, "Error al restaurar la mensualidad.", 403, cursor)
        if control2 is not None:
            return control2
        
        # en este caso no sabria como manejarlo, preguntarle a los chicos porq lo fuerza la recepcionista a que sea hasta un fin de mensualidad especifico, por ahi
        # simplemente agregarlo a la lista de espera directamente sin retornar nada
        if reservas_agregadas['status'] == "no_cupos":
            return {
                "status": "no_cupos",
                "message": "No se pudieron agregar nuevas reservas por falta de cupos."
            }, 201
        
        return {
            "error": "Error al agregar nuevas reservas de la mensualidad."
        }, 404

    cursor.connection.close()
    return _msj_exito_helper("Fin de mensualidad configurado exitosamente.", cursor)

def renovar_mensualidad_service(dni_cliente, id_mensualidad, descripcion):
    cursor = conectarse_db()
    
    # validar si el usuario existe
    usuario = consultar_usuario_por_dni(dni_cliente, cursor)
    control = _controlar_errores_query(usuario, 500, "No se encontró el usuario.", 405, cursor)
    if control is not None:
        return control
        
    # obtener la mensualidad del usuario
    mensualidad = obtener_mensualidad_usuario(usuario["data"]["id"], id_mensualidad, cursor)
    control = _controlar_errores_query(mensualidad, 500, "No se encontró la mensualidad del usuario.", 406, cursor)
    if control is not None:
        return control
        
    datos_mensualidad = mensualidad['data']
    
    respuesta = configurar_fin_mensualidad(id_mensualidad, cursor)
    control = _controlar_errores_query_sin_none(respuesta, 500, "Error al renovar la mensualidad.", 408, cursor)
    if control is not None:
        return control
    
    reservas_agregadas = agregar_nuevas_reservas_mensualidad(id_mensualidad, usuario['data']['id'], cursor)
    print("reservas_agregadas", reservas_agregadas)
    if reservas_agregadas['status'] != "success":
        roll_back = configurar_datos_mensualidad(datos_mensualidad, cursor)
        control2 = _controlar_errores_query_sin_none(roll_back, 500, "Error al restaurar la mensualidad.", 409, cursor)
        if control2 is not None:
            return control2
        
        # aca en front simplemente preguntan si es que quiere entrar a la lista de espera de abonados (voy a crear un route confirmarListaEsperaAbonados)
        # luego se maneja con la funcion que hizo marian
        if reservas_agregadas['status'] == "no_cupos":
            return {
                "status": "no_cupos",
                "message": "No se pudieron agregar nuevas reservas por falta de cupos."
            }, 501
        
        return {
            "error": "Error al agregar nuevas reservas de la mensualidad."
        }, 410
    
    respuesta, status = crear_pago_service_mensualidad(usuario['data']['id'], descripcion, id_mensualidad)
    # time.sleep(10)
    # status = 200
    if status != 200:
        roll_back = configurar_datos_mensualidad(datos_mensualidad, cursor)
        control = _controlar_errores_query_sin_none(roll_back, 500, "Error al hacer rollback.", 411, cursor)
        if control is not None:
            return control
        
        for reserva in reservas_agregadas['data']:
            roll_back = borrar_reserva(reserva, cursor)
            control = _controlar_errores_query_sin_none(roll_back, 500, "Error al borrar reservas de la mensualidad.", 412, cursor)
            if control is not None:
                return control
        
        return respuesta, status
    
    print(" > Esto es en renovar_mensualidad_service al crear el pago de mensualidad")
    print(respuesta)

    # EXTRAEMOS EL PREFERENCE ID DE LA ESTRUCTURA CORRECTA
    preference_id = respuesta["data"]
        
    # Cambiar el estado de la mensualidad
    respuesta_estado = cambiar_estado_mensualidad(datos_mensualidad['id'], cursor)
    control = _controlar_errores_query_sin_none(respuesta_estado, 500, "Error al cambiar el estado de la mensualidad.", 413, cursor)
    if control is not None:
        return control

    cursor.connection.commit()
    cursor.connection.close()
    
    return {
        "status": "success",
        "message": "Mensualidad renovada exitosamente.",
        "preference_id": preference_id
    }, 200

def ver_estado_mensualidad_service(dni_cliente, id_mensualidad):
    cursor = conectarse_db()
    
    # validar si el usuario existe
    usuario = consultar_usuario_por_dni(dni_cliente, cursor)
    control = _controlar_errores_query(usuario, 500, "No se encontró el usuario.", 400, cursor)
    if control is not None:
        return control
    
    # validar si el usuario tiene una mensualidad con fechas dentro de la vigencia de la misma
    tiene_mensualidad = verificar_usuario_tiene_mensualidad(usuario["data"]["id"], id_mensualidad, cursor)
    if not tiene_mensualidad:
        cursor.connection.close()
        return {
            "error": "El usuario no tiene una mensualidad con vigencia."
        }, 401
    
    # obtener si la mensualidad esta vigente
    mensualidad_activa = obtener_mensualidad_activa(usuario["data"]["id"], id_mensualidad, cursor)
    control = _controlar_errores_query(mensualidad_activa, 500, "Error al obtener estado de mensualidad.", 402, cursor)
    if control is not None:
        return control
    
    cursor.connection.close()

    return _msj_exito_helper("Mensualidad activa encontrada.", cursor, mensualidad_activa['data']['fecha_fin'])
    
def cancelar_mensualidad_service(dni_cliente, id_mensualidad):
    cursor = conectarse_db()
    
    # validar si el usuario existe
    usuario = consultar_usuario_por_dni(dni_cliente, cursor)
    control = _controlar_errores_query(usuario, 500, "No se encontró el usuario.", 400, cursor)
    if control is not None:
        return control
        
    # validar si el usuario tiene esa mensualidad
    tiene_mensualidad = verificar_usuario_tiene_mensualidad(usuario["data"]["id"], id_mensualidad, cursor)
    if not tiene_mensualidad:
        return _msj_error_helper("El usuario no tiene esa mensualidad.", cursor), 400
    
    # respuesta = borrar_clase_tener_mensualidad(id_mensualidad, cursor)
    # control = _controlar_errores_query_sin_none(respuesta, 500, "Error al borrar la relación de la mensualidad con las clases.", 400, cursor)
    # if control is not None:
    #     return control
    
    # respuesta = borrar_mensualidad(id_mensualidad, cursor)
    # control = _controlar_errores_query_sin_none(respuesta, 500, "Error al borrar la mensualidad.", 400, cursor)
    # if control is not None:
    #     return control
    
    respuesta = cancelar_mensualidad(id_mensualidad, cursor)
    control = _controlar_errores_query_sin_none(respuesta, 500, "Error al cancelar la mensualidad.", 400, cursor)
    if control is not None:
        return control

    return _msj_exito_helper("Mensualidad cancelada exitosamente.", cursor)

# habria que hacer un boton o algo en el front que llame directamente a esta funcion asi lo mostramos en la demo, sino va a ser imposible
def verificar_mensualidades_por_vencer(cursor_externo=None):
    cursor = conectarse_db()

    query = cursor.execute("""
        SELECT m.id, m.usuario_id, m.fecha_fin
        FROM Mensualidad m
        LEFT JOIN Notificaciones_Enviadas ne ON m.id = ne.mensualidad_id
        WHERE DATE(fecha_fin) BETWEEN DATETIME('now', '-1 day') AND DATETIME('now', '+10 days')
        AND ne.mensualidad_id IS NULL
    """)

    mensualidades = cursor.fetchall()

    for mensualidad in mensualidades:
        usuario_id = mensualidad["usuario_id"]

        cursor.execute(f"""
            SELECT id, correo
            FROM Usuario
            WHERE id = {usuario_id}
        """)

        usuario = cursor.fetchone()

        link = f"http://localhost:5173/RenovarMensualidad/{mensualidad['id']}/{usuario_id}"

        if usuario:
            enviar_mail_vencimiento_mensualidad(usuario_id, usuario["correo"], link)

            # Enviar una notificación para que no se le envíen mas en el futuro
            cursor.execute(f"""
                INSERT INTO Notificaciones_Enviadas (mensualidad_id, fecha_envio)
                VALUES ({mensualidad["id"]}, DATETIME('now'))
            """)

    cursor.connection.commit()
    cursor.connection.close()
    
def verificar_notificaciones_viejas():
    cursor = conectarse_db()

    # elimina todas las notificaciones enviadas pasadas el mes asi no se sobrecarga la db
    cursor.execute("""
        DELETE FROM Notificaciones_Enviadas
        WHERE fecha_envio < DATETIME('now', '-1 month')
    """)

    cursor.connection.commit()
    cursor.connection.close()

def obtener_todas_las_mensualidades_usuario_service(dni_cliente):
    cursor = conectarse_db()
    # consulto usuario por dni. Sin embargo esta query tambien termina buscando para aquellos con rol_id != 3, por lo tanto busca para también administradores
    # usuario = consultar_usuario_por_dni(dni_cliente, cursor)
    usuario = consultar_cliente_por_dni(dni_cliente, cursor)

    # Validar si el usuario existe
    usuario = consultar_usuario_por_dni(dni_cliente, cursor)
    control = _controlar_errores_query(usuario, 500, "No se encontró el usuario.", 400, cursor)
    if control is not None:
        return control
    
    usuario_id = usuario['data']['id']

    mensualidades = obtener_todas_las_mensualidades_usuario(usuario_id, cursor)
    if mensualidades['status'] == "error":
        return _msj_error_helper("Error al obtener las mensualidades del usuario.", cursor), 500
    elif mensualidades['data'] is None:
        return _msj_error_helper("No se encontraron mensualidades para este usuario.", cursor), 404


    cursor.connection.commit()
    cursor.connection.close()

    return _msj_exito_helper(mensualidades['data'], cursor)

def una_vez_que_se_aprobo_el_pago_service(pago_id: int):
    # En este service se revisa si la mensualidad se paga por primera vez, o si se renueva

    cursor = conectarse_db()

    aprobar_pago(pago_id, cursor)
    info_pago_mens = consultar_mensualidad_por_pago_id(pago_id, cursor)
    id_mensualidad = info_pago_mens["data"]["mensualidad_id"]

    # Cambiar el estado de la mensualidad
    cambiar_estado_mensualidad(id_mensualidad, cursor)
    
    # Con la mensualidad, obtener la información relacionada a la mensualidad
    info_inf_mens = comprobar_existe_info_mensualidad(id_mensualidad, cursor)
    print(info_inf_mens)
    info_inf = consultar_info_mensualidad(info_inf_mens["data"]["id"], cursor)
    inf_renovada = info_inf["data"]["renovada"]

    print(inf_renovada)
    if inf_renovada == 0:
        # Si la mensualidad no había sido renovada...
        info_mens = obtener_mensualidad_por_id(id_mensualidad, cursor)
        print(info_inf["data"])
        print(info_inf["data"]["clase_id"])
        clase_id = info_inf["data"]["clase_id"]
        usuario_id = info_mens["data"]["usuario_id"]
        resp = crear_reservas_y_clase_tener_mensualidad_service(id_mensualidad, clase_id, usuario_id, pago_id, cursor)
        return resp
    else:
        # Si no, renovarla nada mas
        resp = extender_mensualidad_un_mes(id_mensualidad, cursor)
        return resp

def extender_mensualidad_service(id_mensualidad: int, cursor):
    # Si la mensualidad ya había sido creada, y el usuario la pagó a tiempo, renovarla...
    extender_mensualidad_un_mes(id_mensualidad, cursor)

    cursor.connection.commit()
    cursor.connection.close()

    return _msj_exito_helper("Se renovó la mensualidad con éxito.", cursor)

def crear_reservas_y_clase_tener_mensualidad_service(id_mensualidad: int, clase_id: int, usuario_id: int, pago_id: int, cursor):
    # OBTENER LOS CUPOS
    clase = consultar_clase_por_id(clase_id, cursor)
    control = _controlar_errores_query(clase, 500, "No se encontro la clase asociada a la mensualidad.", 404, cursor)
    if control is not None:
        return control

    dict_cupos = revisar_si_hay_cupos(clase['data']['id'], cursor) # me devuelve { inst_clase_id: numero_cupos }
    # revisar que las instancias de clase que me manda este dentro del rango de la mensualidad que se va a crear
    
    dict_cupos = revisar_validez_cupos(dict_cupos, cursor)
    hay_cupos = revisar_cupos_disponible_abonado(dict_cupos)

    print(dict_cupos)

    # CREAR LAS RESERVAS
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
    
    print(respuesta)
    
    cursor.connection.commit()
    cursor.connection.close()

    return _msj_exito_helper("Se crearon las reservas y la información de la Mensualidad con éxito", cursor)
