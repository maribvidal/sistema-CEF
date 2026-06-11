from datetime import datetime, date, timedelta
from enums.dias import Dias

import dateparser

FORMATO_FECHA = '%Y-%m-%d'

def generar_fecha_actual(dia: Dias = None) -> str:
    """Genera la fecha del día de hoy con el formato FORMATO_FECHA."""
    if (dias is not None):
        return obtener_fecha_dia_semana(dia)
    return datetime.today().strftime(FORMATO_FECHA)

def obtener_fecha_dia_semana(dia: Dias) -> str:
    hoy = date.today()
    dias_a_sumar = (dia.value - hoy.weekday()) % 6
    return (hoy + timedelta(days=dias_a_sumar)).strftime(FORMATO_FECHA)

def comprobar_dia_pertenece_fecha(dia: Dias, fecha: str):
    fecha_normalizada = convertir_fecha(fecha)
    if fecha_normalizada:
        return fecha_normalizada.weekday() == dia.value
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

def validar_dia_fecha(fecha: str, dia):
    """Valida si una fecha corresponde al día de la semana indicado."""
    fecha_normalizada = convertir_fecha(fecha)
    if fecha_normalizada:
        return fecha_normalizada.weekday() == dia.value
    return False
