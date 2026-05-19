from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_permiso(nombre: str):
    """Permite insertar una fila para la tabla Permiso"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Permiso (nombre)
                                VALUES ('{nombre}');""")
    commitear(cursor)
