from db.operaciones.commitear_db import commitear

def insertar_clase(cursor, estado: str, actividad_id: int, profesor_id: int) -> int:
    """Permite insertar una fila para la tabla Clase
        y retorna el ID de la fila insertada"""
    query = f"""INSERT INTO Clase (estado, actividad_id, profesor_id)
                VALUES ('{estado}', {actividad_id}, {profesor_id});"""
    cursor.execute(query)
    commitear(cursor)
    return cursor.lastrowid
