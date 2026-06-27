from db.operaciones.exception_handler import ejecutar_insertar

def insertar_instancia_clase(clase_id: int, fecha, monto: float, cursor):
    """ Permite insertar una instancia de una clase. """
    query = f"""
        INSERT INTO Instancia_Clase (fecha, clase_id, monto)
        VALUES                      ('{fecha}', {clase_id}, {monto});
    """
    return ejecutar_insertar(query, cursor)
