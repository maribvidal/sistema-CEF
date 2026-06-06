from db.operaciones.exception_handler import ejecutar_query

def modificar_clase_estado(clase_id: int, estado: str, cursor):
    """Permite modificar el estado de una clase."""
    query = f"""UPDATE Clase
                SET estado = '{estado}'
                WHERE id = {clase_id};"""
    return ejecutar_query(query, cursor)
