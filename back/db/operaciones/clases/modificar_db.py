from db.operaciones.commitear_db import commitear

def modificar_clase(cursor, clase_id: int, estado: str, actividad_id: int, profesor_id: int):
    """Permite modificar una fila para la tabla Clase.
        Se modifican todas las variables, excepto su id."""
    query = f"""UPDATE Clase
                SET estado = '{estado}', actividad_id = {actividad_id}, profesor_id = {profesor_id}
                WHERE id = {clase_id};"""
    cursor.execute(query)
    commitear(cursor)
