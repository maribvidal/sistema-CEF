from db.operaciones.commitear_db import commitear

def insertar_recepcionista(cursor, dni: int):
    """Permite insertar una fila para la tabla Recepcionista"""
    query = f"""INSERT INTO Recepcionista (dni)
                VALUES ({dni});"""
    cursor.execute(query)
    commitear(cursor)
    return cursor.lastrowid
