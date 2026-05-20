from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def consultar_cuenta_por_id(id: int) -> tuple:
    """Función que consulta una cuenta por su id, y devuelve la tupla."""
    query = f"SELECT * FROM Cuenta WHERE id_cuenta = {id};"
    return ejecutar_fetchone(query)
