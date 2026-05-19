from db import restricciones
import datetime

def checkear_inputs(objetos):
    """Función que busca que los objetos recibidos
        cumplan las restricciones especificadas en
        el módulo restricciones.

        En los parametros vienen el nombre y el valor
        a checkear.
        ej: [{"name": "nombre", "value": "Maximiliano"}"""
    
    def _validar_fecha(fecha: datetime.date):
        try:
            if isinstance(fecha, datetime.date):
                return {}
            datetime.datetime.strptime(fecha, "%d-%m-%Y")
            return {}
        except:
            return {"error": f"La fecha {fecha} no es válida"}

    for restriccion in restricciones:
        for objeto in objetos:
            tipo_obj = objeto["name"]
            # Si el dato es una fecha
            if (tipo_obj in ['fecha_ini', 'fecha_fin', 'fecha_nac', 'fecha']):
                return _validar_fecha(objeto["value"])
            # En cualquier otro caso
            if restriccion.es_nombre(tipo_obj):
                result = restriccion.checkear_longitud(objeto["value"])
                if len(result) > 0:
                    return result

    return {}
