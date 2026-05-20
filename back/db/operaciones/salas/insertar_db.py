from db.operaciones.commitear_db import commitear

def insertar_sala(cursor, nombre: str):
    """Permite insertar una fila para la tabla Sala"""
    query = f"""INSERT INTO Sala (nombre)
                VALUES ('{nombre}');"""
    cursor.execute(query)
    commitear(cursor)
    return cursor.lastrowid
