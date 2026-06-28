from db.operaciones.exception_handler import ejecutar_insertar
from db import Dias

def insertar_clase(estado: str, actividad_id: int, profesor_id: int, sala_id: int, dia: str, hora: str, cupo_maximo: int, monto: float, cursor):
    """Permite insertar una fila para la tabla Clase"""
    query = f"""INSERT INTO Clase (estado, actividad_id, profesor_id, sala_id, dia, hora, cupo_maximo, monto)
                VALUES ('{estado}', {actividad_id}, {profesor_id}, {sala_id}, '{dia}', '{hora}', {cupo_maximo}, {monto});"""
    return ejecutar_insertar(query, cursor)