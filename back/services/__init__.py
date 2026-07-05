
def _controlar_errores_query(consulta, codigo_error, razon_error2, codigo_error2, cursor):
    """Esta función permite controlar los dos casos de una consulta de error que tenemos:
        el caso donde la query se hizo mal, o hay algún otro tipo de error no contemplado,
        y el caso donde la query se hizo bien, pero no ha retornado nada, u ocurrió un
        error de restricción de parte de la BD."""

    if consulta["status"] == 'error':
        return _msj_error_helper(consulta["message"], cursor), codigo_error
    elif consulta["status"] == 'success' and consulta["data"] is None:
        return _msj_error_helper(razon_error2, cursor), codigo_error2

    return None

def _controlar_errores_query_sin_none(consulta, codigo_error, razon_error2, codigo_error2, cursor):
    """Hace lo mismo que la función de arriba, pero controla que NO haya un none."""

    if consulta["status"] == 'error':
        return _msj_error_helper(consulta["message"], cursor), codigo_error
    elif consulta["status"] == 'success' and consulta["data"] is not None:
        return _msj_error_helper(razon_error2, cursor), codigo_error2

    return None

def _msj_error_helper(razon: str, cursor):
    cursor.connection.close()
    return {
        "status": "error",
        "message": razon
    }

def _msj_exito_helper(razon: str, cursor, res=None):
    cursor.connection.close()
    if res is None:
        return {
            "status": "success",
            "message": razon
        }, 200
    else:
        return {
            "status": "success",
            "message": razon,
            "data": res
        }, 200
