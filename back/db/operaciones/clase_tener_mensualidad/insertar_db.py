from db.operaciones.exception_handler import ejecutar_insertar

def insertar_clase_tener_mensualidad(mensualidad_id: int, clase_id: int, cursor):
    """Permite insertar una fila para la tabla Clase_Tener_Mensualidad"""
    query = f"""INSERT INTO Clase_Tener_Mensualidad (mensualidad_id, clase_id)
                VALUES ({mensualidad_id}, {clase_id});"""
    return ejecutar_insertar(query, cursor)
