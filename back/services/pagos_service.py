from db.operaciones import listar_pagos
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def obtener_pagos_service():
    cursor = conectarse_db()
    pagos = listar_pagos(cursor)
    print("pagos: ", pagos)

    commitear(cursor)
    if pagos['status'] == 'error':
        return {
            "error": "Error al obtener pagos",
            "message": pagos['message']
        }, 500
        
    if pagos['status'] == 'success' and not pagos['data']:
        return {
            "error": "No se encontraron pagos"
        }, 404

    return pagos['data'], 200