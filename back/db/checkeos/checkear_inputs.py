from db import restricciones

def checkear_inputs(objetos):
    """Función que busca que los objetos recibidos
        cumplan las restricciones especificadas en
        el módulo restricciones.

        En los parametros vienen el nombre y el valor
        a checkear.
        ej: [{"name": "nombre", "value": "Maximiliano"}"""

    for restriccion in restricciones:
        for objeto in objetos:
            tipo_obj = objeto["name"]
            
            if restriccion.es_nombre(tipo_obj):
                result = restriccion.checkear(objeto["value"])
                if len(result) > 0:
                    return result

    return {}
