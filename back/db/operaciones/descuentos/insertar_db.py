from db.operaciones.commitear_db import commitear

def insertar_descuento(cursor, nombre: str):
    """Permite insertar una fila para la tabla Descuento"""
    query = f"""INSERT INTO Descuento (nombre)
                VALUES ('{nombre}');"""
    cursor.execute(query)
    commitear(cursor)
    return cursor.lastrowid
