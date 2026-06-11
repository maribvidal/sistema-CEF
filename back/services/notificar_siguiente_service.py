

from back.db.operaciones.clases.consultar_db import consultar_clase_por_id, obtener_detalles_clase
from back.db.operaciones.conectar_db import conectarse_db
from back.db.operaciones.listas_espera.consultar_db import obtener_siguiente_usuario_abonado, obtener_siguiente_usuario_individual


def notificar_siguiente_service(id_clase: int)-> tuple:
    """Service que permite notificar al siguiente usuario en la lista de espera de una clase."""
    cursor = conectarse_db()

    # verificar existencia de clase
    res_clase = obtener_detalles_clase(id_clase, cursor)

    if res_clase["status"] == 'error':
        cursor.connection.close()
        return {
            "error": res_clase['message']
        }, 500
        
    if res_clase["status"] == 'success' and res_clase["data"] is None:
        cursor.connection.close()
        return {
            "error": "No se encontró la clase."
        }, 404
        
    # obtenemos al siguiente usuario en la lista de espera de abonados
    usuario = obtener_siguiente_usuario_abonado(id_clase, cursor)

    if usuario["status"] == 'error':
        cursor.connection.close()
        return {
            "error": res_clase['message']
        }, 500
        
    if usuario["status"] == 'success' and usuario["data"] is None:
        
        usuario = obtener_siguiente_usuario_individual(id_clase, cursor)
        
        if usuario["status"] == 'error':
            cursor.connection.close()
            return {
                "error": usuario['message']
            }, 500

    if usuario["data"] is not None:
        
        # notificar usuario por correo electrónico
        correo_usuario = usuario["data"]["correo"]
        mensaje = f"""
            Se ha liberado un cupo para la clase de '{res_clase['data']['nombre']}' el día {res_clase['data']['fecha']} a las {res_clase['data']['hora']}. 
            
            Para confirmar su reserva haga click aquí: http://localhost:5173/ConfirmarReserva?correo={correo_usuario}&clase_id={id_clase}
        """

    return {
        "message": "Notificacion enviada."
    }, 200