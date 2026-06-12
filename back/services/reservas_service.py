from db.operaciones.reservas.insertar_db import confirmar_reserva_individual, confirmar_reserva_abonado
from db.operaciones.instancias_clases.consultar_db import consultar_instancia_clase_por_id
from db.operaciones.listas_espera.consultar_db import consultar_lista_espera_abonado, consultar_lista_espera_individual
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_id, verificar_usuario_abonado
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.reservas.consultar_db import consultar_reserva_por_id
from db.operaciones.cancelaciones.insertar_db import insertar_cancelacion
from db.operaciones.reservas import borrar_reserva

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
        return _msj_error_helper(res_ins_cancelacion['message'], cursor), 402
    
    cursor.connection.commit()
    
    return _msj_exito_helper(f"Cancelación para la reserva con id {reserva_id} creada exitosamente.", cursor)

def confirmar_reserva_service(id_clase, id_usuario):
    """Service que permite confirmar la reserva de un usuario."""
    cursor = conectarse_db()
    
    # validar si el usuario existe
    usuario = consultar_usuario_por_id(id_usuario, cursor)
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
        
    # validar si existe la instancia de clase
    res_clase = consultar_instancia_clase_por_id(id_clase, cursor)
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
    
    # validar si el usuario es abonado o individual
    es_abonado = verificar_usuario_abonado(cursor, id_usuario, id_clase) # <- repensar porque puede que tenga una mensualidad distinta a la que requiere la clase o que no este vigente

    # validar que el usuario este en una lista de espera correspondiente
    if es_abonado:
        validacion_lista_espera = consultar_lista_espera_abonado(id_usuario, id_clase, cursor)
    else:
        validacion_lista_espera = consultar_lista_espera_individual(id_usuario, id_clase, cursor)
    
    if validacion_lista_espera["status"] == 'error':
        cursor.connection.close()
        return {
            "error": validacion_lista_espera['message']
        }, 500
        
    if validacion_lista_espera["status"] == 'success' and validacion_lista_espera["data"] is None:
        cursor.connection.close()
        return {
            "error": "El usuario no se encuentra en una lista de espera para esta clase."
        }, 404
        
    if es_abonado:
        # confirmar reserva (pasa de estar en la lista de espera a estar en las reservas de la instancia de clase)
        confirmacion = confirmar_reserva_abonado(id_usuario, id_clase, cursor)
    else:
        # confirmar reserva (pasa de estar en la lista de espera a estar en las reservas de la instancia de clase)
        confirmacion = confirmar_reserva_individual(id_usuario, id_clase, cursor)
    
    if confirmacion["status"] == 'error':
        cursor.connection.close()
        return {
            "error": confirmacion['message']
        }, 500
        
    cursor.connection.commit()
    return confirmacion["data"], 200