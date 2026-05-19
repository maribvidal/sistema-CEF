from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_actividad(nombre: str, precio_mensual: float):
    """Permite insertar una fila para la tabla Actividad"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Actividad (nombre, precio_mensual)
                                VALUES ('{nombre}', {precio_mensual});""")
    commitear(cursor)
