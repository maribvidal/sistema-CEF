from db.operaciones.conectar_db import conectarse_db
from db.operaciones.permisos.modificar_db import cambiar_permiso
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_dni, listar_dnis_usuarios
from db.operaciones.empleados.consultar_db import listar_dnis_empleados

def cambiar_permiso_service(dni, permiso):
    """Función para cambiar el permiso de un empleado. 
        Recibe el dni del empleado y el nuevo permiso."""
    
    cursor = conectarse_db()

    empleado = consultar_usuario_por_dni(dni, cursor)

    if empleado['status'] == 'error':
        cursor.connection.close()
        return {
            "error": empleado['message']
        }, 400

    if empleado['status'] == 'success' and not empleado['data']:
        cursor.connection.close()
        return {
            "error": "Empleado no encontrado."
        }, 401

    # Si el rol_id del empleado es el mismo que se le intenta poner ahora...

    rol_viejo = empleado['data']['rol_id']
    if rol_viejo == permiso:
        cursor.connection.close()
        return {
            "error": "El Empleado ya contaba con ese permiso."
        }, 402

    # Intentar cambiar el permiso

    respuesta = cambiar_permiso(dni, permiso, cursor)
    cursor.connection.close()

    if respuesta['status'] == 'error':
        return {
            "error": "Error al intentar modificar permiso",
            "message": respuesta['message']
        }, 500

    return respuesta, 200
