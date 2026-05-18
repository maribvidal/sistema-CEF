import functools, inspect

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

# WRAPPERS

def validar_inputs_db(func):
    @functools.wraps(func) # Esto mantiene el nombre original y el docstring de la función
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        objetos_a_checkear = [
            {"name": param_name, "value": param_value}
            for param_name, param_value in bound_args.arguments.items()
        ]
        
        errores = checkear_inputs(objetos_a_checkear)
        if errores:
            raise ValueError(f"Error de validación: {errores}")
        return func(*args, **kwargs)
        
    return wrapper

# TODO: Hacer un wrapper que escupa los errores que tira el motor de la BD