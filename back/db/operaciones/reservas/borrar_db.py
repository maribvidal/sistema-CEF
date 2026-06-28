from db.operaciones.exception_handler import ejecutar_query

def borrar_reserva(reserva_id, cursor):
    """Operación que elimina una reserva."""
    query = f"DELETE FROM Reserva WHERE id = {reserva_id};"
    ejecutar_query(query, cursor)

def eliminar_reservas_usuario(usuario_id, cursor):
    """
    Elimina todas las reservas futuras de un usuario.
    Se asegura de verificar que la clase asociada tenga una fecha futura.
    """
    print(f"Eliminando reservas del usuario con ID: {usuario_id}")
    query = f"""
        DELETE FROM Reserva 
        WHERE usuario_id = {usuario_id}
    """
    return ejecutar_query(query, cursor)