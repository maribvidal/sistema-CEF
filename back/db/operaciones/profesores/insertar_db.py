from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_profesor(nombre: str, apellido: str, genero: str, dni: int):
    """Permite insertar una fila para la tabla Profesor"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Profesor (nombre, apellido, genero, dni)
                                VALUES('{nombre}', '{apellido}', '{genero}', '{dni}');""")
    commitear(cursor)
