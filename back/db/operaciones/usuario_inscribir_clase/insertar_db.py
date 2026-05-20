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

def insertar_usuario_inscribir_clase(cursor, usuario_id: int, clase_id: int, fecha):
    """Permite insertar una fila para la tabla Usuario_Inscribir_Clase"""
    query = f"""INSERT INTO Usuario_Inscribir_Clase (usuario_id, clase_id, fecha)
                VALUES ({usuario_id}, {clase_id}, '{formattear_fecha(fecha)}');"""
    cursor.execute(query)
    commitear(cursor)
    return cursor.lastrowid
