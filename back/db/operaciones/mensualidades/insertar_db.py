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

def insertar_mensualidad(fecha_ini, fecha_fin, usuario_id: int, cursor):
    """Permite insertar una fila para la tabla Mensualidad"""
    query = f"""INSERT INTO Mensualidad (fecha_ini, fecha_fin, usuario_id)
                VALUES ('{formattear_fecha(fecha_ini)}', '{formattear_fecha(fecha_fin)}', {usuario_id});"""
    ejecutar_insertar(query, cursor)
