from db.operaciones.commitear_db import commitear

def insertar_rol(cursor, nombre: str):
    """Permite insertar una fila para la tabla Rol"""
    query = f"""INSERT INTO Rol (nombre) 
                VALUES ('{nombre}');"""
    cursor.execute(query)
    commitear(cursor)
    return cursor.lastrowid
