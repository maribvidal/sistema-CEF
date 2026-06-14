from db.operaciones.exception_handler import ejecutar_query 

def configurar_fin_mensualidad(id_mensualidad: int, fecha_fin: str, cursor):
    """Permite configurar la fecha de fin de una mensualidad."""
    query = f"""
        UPDATE Mensualidades
        SET fecha_fin = '{fecha_fin}'
        WHERE id = {id_mensualidad};
    """
    return ejecutar_query(query, cursor)