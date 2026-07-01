from pprint import pprint
import time

from db.operaciones.reservas.borrar_db import borrar_reserva
from db.operaciones.mensualidades.insertar_db import agregar_nuevas_reservas_mensualidad
from services.pagos_service import crear_pago_service_mensualidad
from utils.envio_mails import enviar_mail, enviar_mail_vencimiento_mensualidad
from db.operaciones.mensualidades.borrar_db import borrar_mensualidad
from db.operaciones.mensualidades.consultar_db import obtener_mensualidad_activa, obtener_mensualidad_activa_por_usuario, obtener_mensualidades_activa, obtener_todas_las_mensualidades_usuario
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_dni, obtener_mensualidad_usuario, verificar_usuario_tiene_mensualidad
from db.operaciones.usuarios import consultar_usuario_por_dni
from db.operaciones.mensualidades import configurar_fin_mensualidad, cancelar_mensualidad, configurar_datos_mensualidad, cambiar_estado_mensualidad
from db.operaciones.clase_tener_mensualidad import borrar_clase_tener_mensualidad

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
        
    # Cambiar el estado de la mensualidad
    respuesta = cambiar_estado_mensualidad(datos_mensualidad['id'], cursor)
    control = _controlar_errores_query_sin_none(respuesta, 500, "Error al cambiar el estado de la mensualidad.", 413, cursor)
    if control is not None:
        return control

    cursor.connection.commit()
    cursor.connection.close()
    
    return _msj_exito_helper("Mensualidad renovada exitosamente.", cursor)  

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
    usuario = consultar_usuario_por_dni(dni_cliente, cursor)

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