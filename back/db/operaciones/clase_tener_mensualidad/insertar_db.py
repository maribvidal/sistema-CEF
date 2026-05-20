from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_clase_tener_mensualidad(mensualidad_id: int, clase_id: int):
    """Permite insertar una fila para la tabla Clase_Tener_Mensualidad"""
    query = f"""INSERT INTO Clase_Tener_Mensualidad (mensualidad_id, clase_id)
                VALUES ({mensualidad_id}, {clase_id});"""
    cursor = conectarse_db()
    cursor.execute(query)
    commitear(cursor)
