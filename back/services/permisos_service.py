from db.operaciones.conectar_db import conectarse_db
from db.operaciones.permisos.modificar_db import cambiar_permiso
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_id

def cambiar_permiso_service(id, permiso):
    """Función para cambiar el permiso de un usuario. 
        Recibe el id del usuario y el nuevo permiso."""
    
    cursor = conectarse_db()

    usuario = consultar_usuario_por_id(id, cursor)

    if usuario['status'] == 'error':
        cursor.connection.close()
        return {
            "error": usuario['message']
        }, 400

    if usuario['status'] == 'success' and not usuario['data']:
        cursor.connection.close()
        return {
            "error": "Usuario no encontrado."
        }, 401

    # Si el rol_id del usuario es el mismo que se le intenta poner ahora...
    if usuario['data']['rol_id'] == permiso:
        cursor.connection.close()
        return {
            "error": "El usuario ya contaba con ese permiso."
        }, 402

    respuesta = cambiar_permiso(id, permiso, cursor)
    cursor.connection.close()

    if respuesta['status'] == 'error':
        return {
            "error": "Error al intentar modificar permiso",
            "message": respuesta['message']
        }, 500

    return respuesta['data'], 200
