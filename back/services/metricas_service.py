from db.operaciones import obtener_clases_mas_canceladas
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.asistencias import obtener_clases_con_mensualidad_mas_concurridas

def listar_clases_mas_canceladas_service(limite, actividad, fecha_inicio, fecha_fin):
    cursor = conectarse_db()
    clases_mas_canceladas = obtener_clases_mas_canceladas(cursor, limite, actividad, fecha_inicio, fecha_fin)

    cursor.connection.close()
    if clases_mas_canceladas['status'] == 'error':
        return {
            "error": "Error al obtener clases más canceladas.",
            "message": clases_mas_canceladas['message']
        }, 500

    if clases_mas_canceladas['status'] == 'success' and not clases_mas_canceladas['data']:
        return {
            "error": "No se encontraron clases canceladas."
        }, 400

    return clases_mas_canceladas['data'], 200

def listar_clases_con_mensualidad_mas_concurridas_service(limite, fecha_inicio, fecha_fin):
    cursor = conectarse_db()
    clases_con_mensualidad_mas_concurridas = obtener_clases_con_mensualidad_mas_concurridas(limite, fecha_inicio, fecha_fin, cursor)

    cursor.connection.close()
    if clases_con_mensualidad_mas_concurridas['status'] == 'error':
        return {
            "error": "Error al obtener clases con mensualidad más concurridas.",
            "message": clases_con_mensualidad_mas_concurridas['message']
        }, 500

    if clases_con_mensualidad_mas_concurridas['status'] == 'success' and not clases_con_mensualidad_mas_concurridas['data']:
        return {
            "error": "No se encontraron clases concurridas con mensualidad."
        }, 400

    return clases_con_mensualidad_mas_concurridas['data'], 200