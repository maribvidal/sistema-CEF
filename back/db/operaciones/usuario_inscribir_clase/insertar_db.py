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

def insertar_usuario_inscribir_clase_por_id(usuario_id: int, clase_id: int, clase_ocurrir_sala_id: int, cursor):
    """Permite insertar una fila para la tabla Usuario_Inscribir_Clase
        pero sabiendo el id de la Clase_Ocurrir_Sala buscada."""
    query = f"""INSERT INTO Usuario_Inscribir_Clase (usuario_id, clase_id, clase_ocurrir_sala_id)
                VALUES ({usuario_id}, {clase_id}, {clase_ocurrir_sala_id});"""
    return ejecutar_insertar(query, cursor)
