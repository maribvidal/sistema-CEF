from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_rol(nombre: str):
    """Permite insertar una fila para la tabla Rol"""
    query = f"""INSERT INTO Rol (nombre) 
                VALUES ('{nombre}');"""
    cursor = conectarse_db()
    cursor.execute(query)
    commitear(cursor)
