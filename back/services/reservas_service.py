from db.operaciones.conectar_db import conectarse_db
from db.operaciones.reservas.consultar_db import consultar_reserva_por_id
from db.operaciones.cancelaciones.insertar_db import insertar_cancelacion

def _msj_error_helper(razon: str, cursor):
    cursor.connection.close()
    return {
        "status": "error",
        "message": razon
    }

def _msj_exito_helper(razon: str, cursor, res=None):
    cursor.connection.close()
    if res is None:
        return {
            "status": "success",
            "message": razon
        }, 200
    else:
        return {
            "status": "success",
            "message": razon,
            "data": res
        }, 200

def cancelar_reserva_service(reserva_id):
    """Service que permite cancelar la reserva de un usuario."""

    cursor = conectarse_db()

    # Validar si la reserva existe
    res_reserva = consultar_reserva_por_id(reserva_id, cursor)
    if res_reserva['status'] == 'error':
        return _msj_error_helper(res_reserva['message']), 400

    # Cancelar reserva (insertar una cancelación)
    res_ins_cancelacion = insertar_cancelacion(reserva_id, cursor)
    if res_ins_cancelacion['status'] == 'error':
        return _msj_error_helper(res_ins_cancelacion['message']), 401
    
    cursor.connection.commit()
    
    return _msj_exito_helper(f"Cancelación para la reserva con id {reserva_id} creada exitosamente.", cursor)
