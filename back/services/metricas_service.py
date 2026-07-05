from db.operaciones.pagos.consultar_db import listar_pagos, listar_pagos_fechas
from services import _controlar_errores_query
from db.operaciones import obtener_clases_mas_canceladas
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.asistencias import obtener_clases_con_mensualidad_mas_concurridas

def listar_clases_mas_canceladas_service(actividad= None, fecha_inicio = None, fecha_fin = None):
    cursor = conectarse_db()
    print(actividad, fecha_inicio, fecha_fin)
    clases_mas_canceladas = obtener_clases_mas_canceladas(cursor, actividad = actividad, fecha_inicio = fecha_inicio, fecha_fin = fecha_fin)
    control = _controlar_errores_query(clases_mas_canceladas, 400, "No se encontraron clases canceladas.", 401, cursor)
    
    if control is not None:
        return control

    cursor.connection.close()

    return clases_mas_canceladas['data'], 200

def listar_clases_con_mensualidad_mas_concurridas_service(fecha_inicio = None, fecha_fin = None):
    cursor = conectarse_db()
    clases_con_mensualidad_mas_concurridas = obtener_clases_con_mensualidad_mas_concurridas(fecha_inicio = fecha_inicio, fecha_fin = fecha_fin, cursor = cursor)

    control = _controlar_errores_query(clases_con_mensualidad_mas_concurridas, 400, "No se encontraron clases concurridas con mensualidad.", 401, cursor)
    if control is not None:
        return control

    cursor.connection.close()

    return clases_con_mensualidad_mas_concurridas['data'], 200

def listar_plata_recaudada_service():
    cursor = conectarse_db()
    plata_recaudada = listar_pagos(cursor)

    control = _controlar_errores_query(plata_recaudada, 400, "No hay informacion para esta categoria.", 401, cursor)
    if control is not None:
        return control

    cursor.connection.close()
    return plata_recaudada['data'], 200

def listar_plata_recaudada_service_fechas(fecha_inicio, fecha_fin):
    cursor = conectarse_db()
    plata_recaudada = listar_pagos_fechas(cursor, fecha_inicio, fecha_fin)

    control = _controlar_errores_query(plata_recaudada, 400, "No hay informacion para esta categoria.", 401, cursor)
    if control is not None:
        return control

    cursor.connection.close()
    return plata_recaudada['data'], 200