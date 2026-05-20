from db.operaciones.commitear_db import commitear

def borrar_clase(cursor, clase_id):
    """Elimina una clase de la base de datos por su ID."""
    cursor.execute("DELETE FROM Clase WHERE id = ?", (clase_id,))
    commitear(cursor)
