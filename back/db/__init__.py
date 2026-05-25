from db.checkeos.restricciones_objeto import Restriccion

NOM_DB = "database.db"

LONG_NOM = 20
LONG_APE = 30
LONG_CORREO = 30
LONG_CONTRA = 12
LONG_TEL = 15

import datetime

def _validar_fecha(fecha: datetime.date):
        try:
            if isinstance(fecha, datetime.date):
                return {}
            datetime.datetime.strptime(fecha, "%Y-%m-%d")
            return {}
        except:
            return {"error": f"La fecha {fecha} no es válida"}

def validar_contraseña(contraseña: str):
    """Función que valida que la contraseña cumpla con los requisitos de seguridad."""
    if len(contraseña) < 8:
        return {"error": "La contraseña debe tener al menos 8 caracteres"}
    if not contraseña.isalnum():
        return {"error": "La contraseña debe ser alfanumérica"}
    return {}


## Habria que modificar lo de la restriccion porque se manda el Long con la longitud maxima pero no la minima en el caso de la contraseña
## esta se valida en la funcion aparte

restricciones = {
    Restriccion("nombre", LONG_NOM),
    Restriccion("apellido", LONG_APE),
    Restriccion("correo", LONG_CORREO),
    Restriccion("contraseña", LONG_CONTRA, funcion_checkeo = validar_contraseña),
    Restriccion("telefono", LONG_TEL),
    Restriccion("fecha_ini", funcion_checkeo = _validar_fecha),
    Restriccion("fecha_fin", funcion_checkeo = _validar_fecha),
    Restriccion("fecha_nac", funcion_checkeo = _validar_fecha),
    Restriccion("fecha", funcion_checkeo = _validar_fecha)
}
