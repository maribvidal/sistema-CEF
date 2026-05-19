from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_administrador(dni: int):
    """Permite insertar una fila para la tabla Administrador"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Administrador (dni)
                                VALUES ({dni});""")
    commitear(cursor)
