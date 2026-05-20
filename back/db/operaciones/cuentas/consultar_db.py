def consultar_cuenta_por_id(cursor, id: int) -> tuple:
    """Función que consulta una cuenta por su id, y devuelve la tupla."""
    query = f"SELECT * FROM Cuenta WHERE id_cuenta = {id};"
    res = cursor.execute(query)
    res = res.fetchone()
    return res
