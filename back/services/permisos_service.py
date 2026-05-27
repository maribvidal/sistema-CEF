from db.operaciones.conectar_db import conectarse_db
from db.operaciones.permisos.modificar_db import cambiar_permiso
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_id, listar_dnis_usuarios
from db.operaciones.empleados.consultar_db import listar_dnis_empleados

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
    rol_viejo = usuario['data']['rol_id']
    if rol_viejo == permiso:
        cursor.connection.close()
        return {
            "error": "El usuario ya contaba con ese permiso."
        }, 402
    
    # Realizar comprobación de DNIs para ver si puede cambiar de rol_id
    # así sin mas o no
    dni_usu = usuario['data']['dni']
    if (rol_viejo != 3 and permiso == 3):
        # El empleado pasará a ser un usuario común
        res_dnis = listar_dnis_usuarios(cursor)

        if res_dnis['status'] == 'error':
            cursor.connection.close()
            return {
                "error": "Error al obtener los DNIs de los usuarios."
            }, 403

        if (dni_usu in str(res_dnis['data'])):
            cursor.connection.close()
            return {
                "error": "El DNI ya se encuentra registrado para un usuario."
            }, 404
    else if (rol_viejo == 3 and permiso != 3):
        # El usuario común pasará a ser un empleado
        res_dnis = listar_dnis_empleados(cursor)

        if res_dnis['status'] == 'error':
            cursor.connection.close()
            return {
                "error": "Error al obtener los DNIs de los empleados."
            }, 405

        if (dni_usu in str(res_dnis['data'])):
            cursor.connection.close()
            return {
                "error": "El DNI ya se encuentra registrado para un empleado."
            }, 406

    # Intentar cambiar el permiso

    respuesta = cambiar_permiso(id, permiso, cursor)
    cursor.connection.close()

    if respuesta['status'] == 'error':
        return {
            "error": "Error al intentar modificar permiso",
            "message": respuesta['message']
        }, 500

    return respuesta['data'], 200
