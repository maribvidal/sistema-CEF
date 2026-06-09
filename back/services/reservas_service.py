from db.operaciones.conectar_db import conectarse_db
from db.operaciones.reservas.consultar_db import consultar_reserva_por_id
from db.operaciones.cancelaciones.insertar_db import insertar_cancelacion
from db.operaciones.reservas.borrar_db import borrar_reserva

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
        return _msj_error_helper(res_reserva['message'], cursor), 400
    if res_reserva['status'] == 'success' and res_reserva['data'] is None:
        return _msj_error_helper(f"La reserva con el id {reserva_id} no existe.", cursor), 401

    # Cancelar reserva (insertar una cancelación)
    res_elim_reserva = borrar_reserva(reserva_id, cursor)
    id_usuario = res_reserva["data"]["usuario_id"]
    id_ins_clase = res_reserva["data"]["inst_clase_id"]
    res_ins_cancelacion = insertar_cancelacion(id_usuario, id_ins_clase, cursor)
    if res_ins_cancelacion['status'] == 'error':
        return _msj_error_helper(res_ins_cancelacion['message']), 402
    
    cursor.connection.commit()
    
    return _msj_exito_helper(f"Cancelación para la reserva con id {reserva_id} creada exitosamente.", cursor)
