from db.operaciones.conectar_db import conectarse_db
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_dni, verificar_usuario_tiene_mensualidad
from db.operaciones.usuarios import consultar_usuario_por_dni
from db.operaciones.mensualidades import configurar_fin_mensualidad

def configurar_fin_mensualidad_service(dni_cliente, id_mensualidad, fecha_fin):
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
    
    respuesta = configurar_fin_mensualidad(id_mensualidad, fecha_fin, cursor)

    cursor.connection.close()
    if respuesta['status'] == 'error':
        return {
            "error": "Error al configurar fin de mensualidad.",
            "message": respuesta['message']
        }, 500

    return respuesta['data'], 200