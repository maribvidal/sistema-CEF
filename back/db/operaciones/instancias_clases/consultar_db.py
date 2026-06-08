from db.operaciones.exception_handler import ejecutar_fetchone, ejecutar_fetchall

def consultar_instancia_clase_por_id(ins_id, cursor) -> dict:
    """Hace una consulta para obtener una instancia de clase por su ID, y devuelve una tupla."""
    return ejecutar_fetchone(f"SELECT * FROM Instancia_Clase WHERE id = {ins_id}", cursor)
