import sqlite3 as sqlite

from db.operaciones.clases.consultar_db import obtener_clase_por_id

# Estas operaciones devuelven una tupla o varias tuplas si hubo 
# éxito, o None si hubo un error.

def consultar_clase_por_id(cursor: sqlite.Cursor, clase_id: int) -> tuple:
    """Función que se encarga de cnsultar una clase por su ID 
        y controlar algunas cuestiones mas."""
    try:
        return obtener_clase_por_id(cursor, clase_id)
    except Exception as e:
        print(f"Error al consultar la clase: {e}")
        return None
