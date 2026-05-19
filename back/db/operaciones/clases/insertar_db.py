from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_clase(estado: str, actividad_id: int, profesor_id: int):
    """Permite insertar una fila para la tabla Clase"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Clase (estado, actividad_id, profesor_id)
                                VALUES ('{estado}', {actividad_id}, {profesor_id});""")
    commitear(cursor)
