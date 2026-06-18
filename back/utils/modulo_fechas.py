from datetime import datetime, date, timedelta
from enums.dias import Dias

import dateparser

FORMATO_FECHA = '%Y-%m-%d'
FORMATO_FECHA_2 = '%Y-%m-%d %H:%M:%S'

def generar_fecha_actual(dia: str = None) -> str:
    """Genera la fecha del día de hoy con el formato FORMATO_FECHA."""
    if (dia is not None):
        return obtener_fecha_dia_semana(dia)
    return datetime.today().strftime(FORMATO_FECHA)

def generar_fecha_hora_actual(dia: str = None) -> str:
    """Genera la fecha del día de hoy con el formato FORMATO_FECHA_2."""
    if (dia is not None):
        return obtener_fecha_dia_semana(dia)
    return datetime.today().strftime(FORMATO_FECHA)

def obtener_fecha_dia_semana(dia: str) -> str:
    hoy = date.today()
    dias_a_sumar = (Dias[dia].value - hoy.weekday()) % 6 + 1
    return (hoy + timedelta(days=dias_a_sumar)).strftime(FORMATO_FECHA)

def comprobar_dia_pertenece_fecha(dia: str, fecha: str):
    fecha_normalizada = convertir_fecha(fecha)
    if fecha_normalizada:
        return fecha_normalizada.weekday() == Dias[dia].value
    return False

def convertir_fecha(fecha: str):
    try:
        return dateparser.parse(fecha, FORMATO_FECHA)
    except:
        print(f" >> convertir_fecha: La fecha {fecha} no es válida.")
        return False

def validar_fecha(fecha: str) -> bool:
    """Función auxiliar para validar el formato de la fecha."""
    try:
        fecha_normalizada = datetime.strptime(fecha, FORMATO_FECHA)
    except ValueError:
        return False

    # Esto para validar que la fecha no sea anterior a la actual. Sino pues no tendria sentido
    return fecha_normalizada.date() >= date.today()

def validar_dia_fecha(fecha: str, dia: str):
    """Valida si una fecha corresponde al día de la semana indicado."""
    fecha_normalizada = convertir_fecha(fecha)
    if fecha_normalizada:
        return fecha_normalizada.weekday() == Dias[dia].value
    return False

def comprobar_fecha_anterior(fecha1: str, fecha2: str) -> bool:
    """Valida si la fecha1 es anterior a la fecha2 o no."""
    fecha1_normalizada = convertir_fecha(fecha1)
    fecha2_normalizada = convertir_fecha(fecha2)

    return fecha1_normalizada < fecha2_normalizada
