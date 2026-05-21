from db.operaciones.exception_handler import ejecutar_insertar

def insertar_clase(estado: str, actividad_id: int, profesor_id: int, cursor):
    """Permite insertar una fila para la tabla Clase"""
    query = f"""INSERT INTO Clase (estado, actividad_id, profesor_id)
                VALUES ('{estado}', {actividad_id}, {profesor_id});"""
    return ejecutar_insertar(query, cursor)
