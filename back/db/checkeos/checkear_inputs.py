# en los parametros vienen el nombre y el valor a checkear
# ej [{"name": "nombre", "value": "Maximiliano"},....]
def checkear_inputs(objetos):
    from db import restricciones

    for restriccion in restricciones:
        for objeto in objetos:
            if restriccion.es_nombre(objeto["name"]):
                result = restriccion.checkearRestriccion(objeto["value"])
                if len(result) > 0:
                    return result

    return {}