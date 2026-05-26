from db.operaciones.conectar_db import conectarse_db
from db.operaciones.permisos.modificar_db import cambiar_permiso

def cambiar_permiso_service(id, permiso):
    """Función para cambiar el permiso de un usuario. 
        Recibe el id del usuario y el nuevo permiso."""
    
    cursor = conectarse_db()
    respuesta = cambiar_permiso(id, permiso, cursor)
    cursor.connection.close()

    if respuesta['status'] == 'error':
        return {
            "error": "Error al intentar modificar permiso",
            "message": respuesta['message']
        }, 500

    return respuesta['data'], 200
