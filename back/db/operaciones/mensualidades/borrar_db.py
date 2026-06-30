from db.operaciones.exception_handler import ejecutar_query 

def borrar_mensualidad(mensualidad_id: int, cursor):
    """Permite borrar una fila de la tabla Mensualidad"""
    query = f"""DELETE FROM Mensualidad WHERE id = {mensualidad_id};"""
    return ejecutar_query(query, cursor)

def borrar_reservas_mensualidad(mensualidad_id: int, cursor):
    """Permite borrar las reservas de una mensualidad"""
    query = f"""
        DELETE FROM Reserva
        WHERE usuario_id IN (
            SELECT usuario_id
            FROM Mensualidad
            WHERE id = {mensualidad_id}
        )
        AND inst_clase_id IN (
            SELECT ic.id
            FROM Instancia_Clase ic
            INNER JOIN Clase c ON ic.clase_id = c.id
            INNER JOIN Clase_Tener_Mensualidad ctm ON c.id = ctm.clase_id
            WHERE ctm.mensualidad_id = {mensualidad_id}
        );
    """
    return ejecutar_query(query, cursor)