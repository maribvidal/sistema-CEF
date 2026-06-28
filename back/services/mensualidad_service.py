from db.operaciones.mensualidades.borrar_db import borrar_mensualidad
from db.operaciones.mensualidades.consultar_db import obtener_mensualidad_activa
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_dni, verificar_usuario_tiene_mensualidad
from db.operaciones.usuarios import consultar_usuario_por_dni
from db.operaciones.mensualidades import configurar_fin_mensualidad
from db.operaciones.clase_tener_mensualidad import borrar_clase_tener_mensualidad

from services import _controlar_errores_query,_controlar_errores_query_sin_none, _msj_exito_helper, _msj_error_helper

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
    
    # validar si el usuario tiene una mensualidad activa
    tiene_mensualidad = verificar_usuario_tiene_mensualidad(usuario["data"]["id"], id_mensualidad, cursor)
    if not tiene_mensualidad:
        cursor.connection.close()
        return {
            "error": "El usuario no tiene una mensualidad activa."
        }, 400
    
    # obtener si la mensualidad esta activa y en caso afirmativo devuelve la fecha de fin
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
    
    respuesta = borrar_clase_tener_mensualidad(id_mensualidad, cursor)
    control = _controlar_errores_query_sin_none(respuesta, 500, "Error al borrar la relación de la mensualidad con las clases.", 400, cursor)
    if control is not None:
        return control
    
    respuesta = borrar_mensualidad(id_mensualidad, cursor)
    control = _controlar_errores_query_sin_none(respuesta, 500, "Error al borrar la mensualidad.", 400, cursor)
    if control is not None:
        return control

    return _msj_exito_helper("Mensualidad cancelada exitosamente.", cursor)