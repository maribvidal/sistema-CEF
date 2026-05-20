from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_descuento(nombre: str):
    """Permite insertar una fila para la tabla Descuento"""
    query = f"""INSERT INTO Descuento (nombre)
                VALUES ('{nombre}');"""
    cursor = conectarse_db()
    cursor.execute(query)
    commitear(cursor)
