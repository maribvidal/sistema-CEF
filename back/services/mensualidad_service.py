from utils.envio_mails import enviar_mail
from db.operaciones.mensualidades.borrar_db import borrar_mensualidad
from db.operaciones.mensualidades.consultar_db import obtener_mensualidad_activa, obtener_mensualidad_activa_por_usuario, obtener_mensualidades_activa
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_dni, verificar_usuario_tiene_mensualidad
from db.operaciones.usuarios import consultar_usuario_por_dni
from db.operaciones.mensualidades import configurar_fin_mensualidad, cancelar_mensualidad
from db.operaciones.clase_tener_mensualidad import borrar_clase_tener_mensualidad

from services import _controlar_errores_query,_controlar_errores_query_sin_none, _msj_exito_helper, _msj_error_helper

def obtener_mensualidad_service():
    cursor = conectarse_db()
    
    mensualidades_activas = obtener_mensualidades_activa(cursor)
    print(mensualidades_activas)
    control = _controlar_errores_query(mensualidades_activas, 500, "Error al obtener mensualidades activas.", 400, cursor)
    print(control)
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
    control = _controlar_errores_query(mensualidades_activas, 500, "No se encontraron mensualidades activas para este usuario.", 400, cursor)
    if control is not None:
        return control

    return _msj_exito_helper(mensualidades_activas['data'], cursor)

def configurar_fin_mensualidad_service(dni_cliente, id_mensualidad, fecha_fin = None):
    cursor = conectarse_db()
    
    # validar si el usuario existe
    usuario = consultar_usuario_por_dni(dni_cliente, cursor)
    if usuario["status"] == 'error':
        cursor.connection.close()
        return {
            "error": usuario['message']
        }, 500
        
    if usuario["status"] == 'success' and usuario["data"] is None:
        cursor.connection.close()
        return {
            "error": "No se encontró el usuario."
        }, 404
        
    # validar si el usuario tiene esa mensualidad
    tiene_mensualidad = verificar_usuario_tiene_mensualidad(usuario["data"]["id"], id_mensualidad, cursor)
    if not tiene_mensualidad:
        cursor.connection.close()
        return {
            "error": "El usuario no tiene esa mensualidad."
        }, 400
    
    respuesta = configurar_fin_mensualidad(id_mensualidad, cursor, fecha_fin = fecha_fin)

    cursor.connection.close()
    if respuesta['status'] == 'error':
        return {
            "error": "Error al configurar fin de mensualidad.",
            "message": respuesta['message']
        }, 500

    return respuesta['data'], 200

def ver_estado_mensualidad_service(dni_cliente, id_mensualidad):
    cursor = conectarse_db()
    
    # validar si el usuario existe
    usuario = consultar_usuario_por_dni(dni_cliente, cursor)
    if usuario["status"] == 'error':
        cursor.connection.close()
        return {
            "error": usuario['message']
        }, 500
        
    if usuario["status"] == 'success' and usuario["data"] is None:
        cursor.connection.close()
        return {
            "error": "No se encontró el usuario."
        }, 404
    
    # validar si el usuario tiene una mensualidad con fechas dentro de la vigencia de la misma
    tiene_mensualidad = verificar_usuario_tiene_mensualidad(usuario["data"]["id"], id_mensualidad, cursor)
    if not tiene_mensualidad:
        cursor.connection.close()
        return {
            "error": "El usuario no tiene una mensualidad con vigencia."
        }, 400
    
    # obtener si la mensualidad esta vigente
    mensualidad_activa = obtener_mensualidad_activa(usuario["data"]["id"], id_mensualidad, cursor)
    
    cursor.connection.close()
    if mensualidad_activa['status'] == 'error':
        return {
            "error": "Error al obtener estado de mensualidad.",
            "message": mensualidad_activa['message']
        }, 500
        
    if mensualidad_activa['data'] is None:
        return {
            "error": "No se encontró una mensualidad activa para el usuario."
        }, 404

    return {
        "message": "Mensualidad activa encontrada.",
        "fecha_fin": mensualidad_activa['data']['fecha_fin']        
    }, 200
    
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
def verificar_mensualidades_por_vencer():
    cursor = conectarse_db()

    cursor.execute("""
        SELECT m.id, m.usuario_id, m.fecha_fin
        FROM Mensualidad m
        LEFT JOIN Notificaciones_Enviadas ne ON m.id = ne.mensualidad_id
        WHERE m.fecha_fin BETWEEN DATETIME('now') AND DATETIME('now', '+7 days')
        AND ne.mensualidad_id IS NULL
    """)

    mensualidades = cursor.fetchall()

    for mensualidad in mensualidades:
        usuario_id = mensualidad["usuario_id"]

        cursor.execute(f"""
            SELECT correo
            FROM Usuario
            WHERE id = {usuario_id}
        """)

        usuario = cursor.fetchone()

        link = f"http://localhost:5173/Renovar_mensualidad/{mensualidad['id']}/{usuario_id}"

        if usuario:
            enviar_mail(
                usuario["correo"],
                "Aviso de mensualidad por vencer",
                f"Tu mensualidad está por vencer /n Por favor, renueva tu mensualidad para seguir disfrutando de nuestros servicios. /n {link}"
            )

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