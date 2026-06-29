from db.operaciones.exception_handler import ejecutar_query

def modificar_clase_estado(clase_id: int, estado: str, cursor):
    """Permite modificar el estado de una clase."""
    query = f"""UPDATE Clase
                SET estado = '{estado}'
                WHERE id = {clase_id};"""
    return ejecutar_query(query, cursor)

def modificar_clase(clase_id: int, estado: str, id_profesor: int, sala_id: int, cursor, monto = None):
    """Permite modificar los detalles de una clase."""
    query = f"""UPDATE Clase
                SET estado = '{estado}',
                    profesor_id = {id_profesor},"""
    if monto:
        query += f"monto = {monto},"
    query += f"""sala_id = {sala_id}
                WHERE id = {clase_id};"""
    return ejecutar_query(query, cursor)
