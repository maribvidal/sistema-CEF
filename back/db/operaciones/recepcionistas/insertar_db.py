from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_recepcionista(dni: int):
    """Permite insertar una fila para la tabla Recepcionista"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Recepcionista (dni)
                                VALUES ({dni});""")
    commitear(cursor)
