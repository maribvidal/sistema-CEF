from db.operaciones.exception_handler import ejecutar_fetchone, ejecutar_fetchall

def consultar_reserva_por_id(reserva_id: int, cursor):
    """Operación que consulta por una reserva según su id y devuelve una tupla."""
    query = f"SELECT * FROM Reserva WHERE id = {reserva_id}"
    return ejecutar_fetchone(query, cursor)
