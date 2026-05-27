from db.operaciones.exception_handler import ejecutar_insertar

def insertar_clase(estado: str, actividad_id: int, profesor_id: int, cupo_maximo: int, cursor):
    """Permite insertar una fila para la tabla Clase"""
    query = f"""INSERT INTO Clase (estado, actividad_id, profesor_id, cupo_maximo)
                VALUES ('{estado}', {actividad_id}, {profesor_id}, {cupo_maximo});"""
    return ejecutar_insertar(query, cursor)
