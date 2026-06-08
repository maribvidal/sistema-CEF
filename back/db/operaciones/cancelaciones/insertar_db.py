from db.operaciones.exception_handler import ejecutar_insertar

def insertar_cancelacion(reserva_id, cursor):
    """Operación que permite insertar una cancelación."""
    fecha = '2026-08-06'
    query = f"""INSERT INTO Cancelacion (fecha, reserva_id)
                                VALUES ('{fecha}', {reserva_id});"""
    return ejecutar_insertar(query, cursor)
