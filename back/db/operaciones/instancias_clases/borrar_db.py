from db.operaciones.exception_handler import ejecutar_query

def borrar_instancias_clases_por_clase(id_clase: int, cursor):
    """ Permite borrar las filas de la tabla Instancia_Clase
        que pertenezcan a una clase."""
    query = f"""
        DELETE FROM Instancia_Clase
        WHERE clase_id = {id_clase};
    """
    return ejecutar_query(query, cursor)
