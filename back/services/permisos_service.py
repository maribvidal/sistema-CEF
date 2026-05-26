from db.operaciones.conectar_db import conectarse_db
from db.operaciones.permisos.modificar_db import cambiar_permiso

def cambiar_permiso_service(dni, permiso):
    """Función para cambiar el permiso de un usuario. 
        Recibe el DNI del usuario y el nuevo permiso."""
    
    cursor = conectarse_db()
    print("DNI recibido en el servicio: ", dni, " Permiso recibido en el servicio: ", permiso)
    respuesta = cambiar_permiso(dni, permiso, cursor)
    print("RESPUESTA DEL SERVICIO: ", respuesta)
    cursor.connection.close()

    if respuesta['status'] == 'error':
        return {
            "error": "Error al intentar modificar permiso",
            "message": respuesta['message']
        }, 500

    return respuesta['data'], 200


