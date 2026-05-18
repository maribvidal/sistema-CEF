def checkear_inputs(objetos):
    """Función que busca que los objetos recibidos
        cumplan las restricciones especificadas en
        el módulo restricciones.

        En los parametros vienen el nombre y el valor
        a checkear.
        ej: [{"name": "nombre", "value": "Maximiliano"}"""
    from db import restricciones

    for restriccion in restricciones:
        for objeto in objetos:
            if restriccion.es_nombre(objeto["name"]):
                result = restriccion.checkear_restriccion(objeto["value"])
                if len(result) > 0:
                    return result

    return {}
