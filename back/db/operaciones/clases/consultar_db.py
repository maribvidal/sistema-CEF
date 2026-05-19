from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def listar_clases() -> list:
    """Hace una consulta para listar todas las clases, y devuelve una lista de tuplas"""
    return ejecutar_fetchall("SELECT * FROM Clase")