from db.operaciones.exception_handler import ejecutar_insertar

def insertar_instancia_clase(fecha, clase_id: int, cursor):
    """ Permite insertar una instancia de una clase. """
    query = f"""
        INSERT INTO Instancia_Clase (fecha, clase_id)
        VALUES                      ('{fecha}', {clase_id});
    """
    return ejecutar_insertar(query, cursor)
