from db.operaciones.commitear_db import commitear

def insertar_administrador(cursor, dni: int):
    """Permite insertar una fila para la tabla Administrador"""
    query = f"""INSERT INTO Administrador (dni)
                VALUES ({dni});"""
    cursor.execute(query)
    commitear(cursor)
    return cursor.lastrowid
