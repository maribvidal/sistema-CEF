from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_permiso(nombre: str):
    """Permite insertar una fila para la tabla Permiso"""
    query = f"""INSERT INTO Permiso (nombre)
                VALUES ('{nombre}');"""
    cursor = conectarse_db()
    cursor.execute(query)
    commitear(cursor)
