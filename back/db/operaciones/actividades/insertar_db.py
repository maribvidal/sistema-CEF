from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_actividad(nombre: str, precio_mensual: float) -> int:
    """Permite insertar una fila para la tabla Actividad 
        y retorna el ID de la fila insertada"""
    query = f"""INSERT INTO Actividad (nombre, precio_mensual)
                VALUES ('{nombre}', {precio_mensual});"""
    cursor = conectarse_db()
    cursor.execute(query)
    commitear(cursor)
    return cursor.lastrowid
