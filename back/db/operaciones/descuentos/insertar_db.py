from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_descuento(nombre: str):
    """Permite insertar una fila para la tabla Descuento"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Descuento (nombre)
                                VALUES ('{nombre}');""")
    commitear(cursor)
