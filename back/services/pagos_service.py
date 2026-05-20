from db.operaciones import listar_pagos

def obtener_pagos_service():
    pagos = listar_pagos()

    print(pagos)

    if pagos['status'] == 'error':
        return {
            "error": "Error al obtener pagos",
            "message": pagos['message']
        }, 500
        
    if pagos['status'] == 'success' and not pagos['data']:
        return {
            "error": "No se encontraron pagos"
        }, 404

    return {
        "pagos": pagos['data']
    }, 200