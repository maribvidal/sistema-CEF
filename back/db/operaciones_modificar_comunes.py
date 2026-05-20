import sqlite3 as sqlite

from db.operaciones.clases.modificar_db import modificar_clase as modif_clas

# Estas operaciones devuelven True si las filas fueron modificadas
# con éxito, o False si hubo un error.

def modificar_clase(cursor: sqlite.Cursor, clase_id: int, estado: str, actividad_id: int, profesor_id: int) -> bool:
    """Función que se encarga de modificar una clase por su ID y controlar
        algunas cuestiones mas."""
    try:
        modif_clas(cursor, clase_id, estado, actividad_id, profesor_id)
        return True
    except Exception as e:
        print(f" > Error al modificar clase: {e}")
        return False
