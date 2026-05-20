from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

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

def insertar_clase_ocurrir_sala(clase_id: int, sala_id: int, fecha):
    """Permite insertar una fila para la tabla Clase_Ocurrir_Sala"""
    query = f"""INSERT INTO Clase_Ocurrir_Sala (clase_id, sala_id, fecha)
                VALUES ({clase_id}, {sala_id}, '{formattear_fecha(fecha)}');"""
    cursor = conectarse_db()
    cursor.execute(query)
    commitear(cursor)
    return cursor.lastrowid