from db.operaciones.exception_handler import ejecutar_insertar
from utils.modulo_fechas import convertir_fecha_a_obj, convertir_fecha_a_formato, generar_fecha_actual
from datetime import timedelta

def insertar_instancia_clase(clase_id: int, fecha, monto: float, cursor):
    """ Permite insertar una instancia de una clase. """
    query = f"""
        INSERT INTO Instancia_Clase (fecha, clase_id, monto)
        VALUES                      ('{fecha}', {clase_id}, {monto});
    """
    return ejecutar_insertar(query, cursor)

def crear_instancias_clase_por_un_año(clase_id: int, monto: float, cursor, dia = None) -> list:
    """ Permite crear un montón de instancias de una clase, a partir de una fecha
        dada pasada como argumento."""
    
    # Si no se especificó un día, se generará la fecha del día actual
    fecha = generar_fecha_actual(dia)
    
    fecha_obj = convertir_fecha_a_obj(fecha)
    print(fecha)
    ids_ins_clases = []

    # En un año por lo menos hay 52 días de un día de la semana

    respuesta = None
    for i in range(1, 52):
        fecha_str = convertir_fecha_a_formato(fecha_obj)
        respuesta = insertar_instancia_clase(clase_id, fecha_str, monto, cursor)
        ids_ins_clases.append(respuesta["data"])
        fecha_obj = fecha_obj + timedelta(days=7)

    return ids_ins_clases
