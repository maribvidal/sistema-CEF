import sqlite3 as sqlite

from db.operaciones.clases.borrar_db import borrar_clase

# Estas operaciones devuelven True si las filas fueron eliminadas
# con éxito, o False si hubo un error.

def eliminar_clase_por_id(cursor: sqlite.Cursor, clase_id: int) -> bool:
    """Función que se encarga de eliminar una clase por su ID y controlar
        algunas cuestiones mas."""
    try:
        borrar_clase(cursor, clase_id)
        return True
    except Exception as e:
        print(f" > Error al eliminar clase: {e}")
        return False
