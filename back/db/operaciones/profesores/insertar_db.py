from db.operaciones.commitear_db import commitear

def insertar_profesor(cursor, nombre: str, apellido: str, genero: str, dni: int) -> int:
    """Permite insertar una fila para la tabla Profesor
        y retorna el ID de la fila insertada"""
    query = f"""INSERT INTO Profesor (nombre, apellido, genero, dni)
                VALUES('{nombre}', '{apellido}', '{genero}', '{dni}');"""
    cursor.execute(query)
    commitear(cursor)
    return cursor.lastrowid
