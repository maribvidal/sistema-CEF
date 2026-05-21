from db.operaciones.exception_handler import ejecutar_insertar

import datetime
from datetime import date
from dateutil.parser import parse

def formattear_fecha(fecha):
    """Función interna que formattea la fecha al
        formato pedido, suponiendo que se recibe
        un objeto tipo date, datetime, o un str
        pero que tiene una fecha dentro suyo."""
    if isinstance(fecha, date) and not isinstance(fecha, datetime.datetime):
        return fecha.strftime("%Y-%m-%d")
    if isinstance(fecha, datetime.datetime):
        return fecha.date().strftime("%Y-%m-%d")
    if isinstance(fecha, str):
        fecha = parse(fecha, dayfirst=False)
        return fecha.date().strftime("%Y-%m-%d")

def insertar_clase_ocurrir_sala(clase_id: int, sala_id: int, fecha, hora: int, cursor):
    """Permite insertar una fila para la tabla Clase_Ocurrir_Sala"""
    query = f"""INSERT INTO Clase_Ocurrir_Sala (clase_id, sala_id, fecha, hora)
                VALUES ({clase_id}, {sala_id}, '{formattear_fecha(fecha)}', {hora});"""
    return ejecutar_insertar(query, cursor)
