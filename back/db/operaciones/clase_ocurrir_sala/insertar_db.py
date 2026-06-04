from db.operaciones.exception_handler import ejecutar_insertar

import datetime
from datetime import date
from dateutil.parser import parse

def insertar_clase_ocurrir_sala(clase_id: int, sala_id: int, dia, hora: str, cursor):
    """Permite insertar una fila para la tabla Clase_Ocurrir_Sala"""
    query = f"""INSERT INTO Clase_Ocurrir_Sala (clase_id, sala_id, dia, hora)
                VALUES ({clase_id}, {sala_id}, '{dia}', '{hora}');"""
    return ejecutar_insertar(query, cursor)
