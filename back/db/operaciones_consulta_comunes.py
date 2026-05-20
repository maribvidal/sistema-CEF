import sqlite3 as sqlite

from db.operaciones.clases.consultar_db import obtener_clase_por_id
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_dni as cons_usu_por_dni
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_correo as cons_usu_por_correo

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

def consultar_usuario_por_dni(cursor: sqlite.Cursor, dni: int) -> tuple:
    """Función que se encarga de consultar un usuario por su DNI 
        y controlar algunas cuestiones mas."""
    try:
        return cons_usu_por_dni(cursor, dni)
    except Exception as e:
        print(f"Error al consultar el usuario por DNI: {e}")
        return None

def consultar_usuario_por_correo(cursor: sqlite.Cursor, correo: str) -> list:
    """Función que se encarga de consultar un usuario por su correo 
        y controlar algunas cuestiones mas."""
    try:
        return cons_usu_por_correo(cursor, correo)
    except Exception as e:
        print(f"Error al consultar el usuario por correo: {e}")
        return None
