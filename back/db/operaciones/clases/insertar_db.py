from db.operaciones.exception_handler import ejecutar_insertar
from db import Dias

def insertar_clase(estado: str, actividad_id: int, profesor_id: int, sala_id: int, dia: Dias, hora: str, cupo_maximo: int, cursor):
    """Permite insertar una fila para la tabla Clase"""
    query = f"""INSERT INTO Clase (estado, actividad_id, profesor_id, sala_id, dia, hora, cupo_maximo)
                VALUES ('{estado}', {actividad_id}, {profesor_id}, {sala_id}, '{dia}', '{hora}', {cupo_maximo});"""
    return ejecutar_insertar(query, cursor)
