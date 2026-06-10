from db.operaciones import obtener_clases_mas_canceladas
from db.operaciones.conectar_db import conectarse_db

def listar_clases_mas_canceladas_service(limite, actividad, fecha_inicio, fecha_fin):
    cursor = conectarse_db()
    clases_mas_canceladas = obtener_clases_mas_canceladas(cursor, limite, actividad, fecha_inicio, fecha_fin)
    print("clases_mas_canceladas: ", clases_mas_canceladas)

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