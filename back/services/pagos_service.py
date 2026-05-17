from db.operaciones import listar_pagos

def obtener_pagos_service():
    pagos = listar_pagos()

    if not pagos:
        return {
            "error": "No se encontraron pagos"
        }, 404

    return {
        "pagos": pagos
    }, 200