from datetime import datetime
from enums.dias import Dias

import dateparser

FORMATO_FECHA = '%Y-%m-%d'

def generar_fecha_actual() -> str:
    """Genera la fecha del día de hoy con el formato FORMATO_FECHA."""
    return datetime.today().strftime(FORMATO_FECHA)

def comprobar_dia_pertenece_fecha(dia: Dias, fecha: str):
    fecha_normalizada = convertir_fecha(fecha)
    if fecha_normalizada:
        return fecha_normalizada.weekday() == dia.value
    return False

def convertir_fecha(fecha: str):
    try:
        return dateparser.parse(fecha, "%Y-%m-%d")
    except:
        print(f" >> convertir_fecha: La fecha {fecha} no es válida.")
        return False
