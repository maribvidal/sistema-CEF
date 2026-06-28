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

# HABRIA QUE MODIFICAR ESTO, ES 1 MES. NO SE TENDRIAN QUE PODER PASAR CUALQUIER FECHA DE INICIO Y FIN
def insertar_mensualidad(usuario_id: int, cursor, fecha_ini = None):
    """Permite insertar una fila para la tabla Mensualidad"""
    query = f"""INSERT INTO Mensualidad (fecha_ini, fecha_fin, usuario_id)"""
    
    if fecha_ini is None:
        valores = f""" 
            VALUES (DATE('now'), DATE('now', '+1 month'), {usuario_id})
        """
    else:
        fecha = formattear_fecha(fecha_ini)
        valores = f"""VALUES ('{fecha}', DATE('{fecha}', '+1 month'), {usuario_id});"""
    
    query += valores
    return ejecutar_insertar(query, cursor)
