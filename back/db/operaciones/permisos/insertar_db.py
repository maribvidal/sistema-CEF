from db.operaciones.commitear_db import commitear

def insertar_permiso(cursor, nombre: str):
    """Permite insertar una fila para la tabla Permiso"""
    query = f"""INSERT INTO Permiso (nombre)
                VALUES ('{nombre}');"""
    cursor.execute(query)
    commitear(cursor)
    return cursor.lastrowid
