from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_sala(nombre: str):
    """Permite insertar una fila para la tabla Sala"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Sala (nombre)
                                VALUES ('{nombre}');""")
    commitear(cursor)
