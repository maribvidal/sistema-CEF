from db.operaciones.exception_handler import ejecutar_fetchone, ejecutar_fetchall

def consultar_cancelacion_por_id(cancelacion_id: int, cursor):
    """Operación que consulta por una cancelacion según su id y devuelve una tupla."""
    query = f"SELECT * FROM Cancelacion WHERE id = {cancelacion_id}"
    return ejecutar_fetchone(query, cursor)

def consultar_cancelacion_por_reserva_id(reserva_id: int, cursor):
    """Operación que consulta por una cancelacion según el id de la reserva y devuelve una tupla."""
    query = f"SELECT * FROM Cancelacion WHERE reserva_id = {reserva_id}"
    return ejecutar_fetchone(query, cursor)

def obtener_cancelaciones_por_usuario_inst_clase(id_ins_clase: int, id_usuario: int, cursor):
    """Operación que consulta por una cancelación según el id de la instancia de la clase
        de la reserva vinculada con la cancelación, y del usuario de la reserva."""
    query = f"""SELECT c.fecha, c.reserva_id
                FROM Reserva r INNER JOIN Cancelacion c ON (r.id = c.reserva_id)
                WHERE inst_clase_id = {id_ins_clase} AND usuario_id = {id_usuario};"""
    return ejecutar_fetchall(query, cursor)
