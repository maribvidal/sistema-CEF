from db.operaciones.exception_handler import ejecutar_fetchone, ejecutar_fetchall

def consultar_cancelacion_por_id(cancelacion_id: int, cursor):
    """Operación que consulta por una cancelacion según su id y devuelve una tupla."""
    query = f"SELECT * FROM Cancelacion WHERE id = {cancelacion_id}"
    return ejecutar_fetchone(query, cursor)

def consultar_cancelacion_por_reserva_id(reserva_id: int, cursor):
    """Operación que consulta por una cancelacion según el id de la reserva y devuelve una tupla."""
    query = f"SELECT * FROM Cancelacion WHERE reserva_id = {reserva_id}"
    return ejecutar_fetchone(query, cursor)
