from db.operaciones.exception_handler import ejecutar_query

def borrar_reserva(reserva_id, cursor):
    """Operación que elimina una reserva."""
    query = f"DELETE FROM Reserva WHERE id = {reserva_id};"
    ejecutar_query(query, cursor)
