from db.operaciones.exception_handler import ejecutar_query

def modificar_clase(clase_id: int, estado: str, actividad_id: int, profesor_id: int, cupo_maximo: int, cursor):
    """Permite modificar una fila para la tabla Clase.
        Se modifican todas las variables, excepto su id."""
    query = f"""UPDATE Clase
                SET estado = '{estado}', actividad_id = {actividad_id}, profesor_id = {profesor_id}, cupo_maximo = {cupo_maximo}
                WHERE id = {clase_id};"""
    return ejecutar_query(query, cursor)

def modificar_clase_estado(clase_id: int, estado: str, cursor):
    """Permite modificar el estado de una clase a 'Borrada'."""
    query = f"""UPDATE Clase
                SET estado = '{estado}'
                WHERE id = {clase_id};"""
    return ejecutar_query(query, cursor)