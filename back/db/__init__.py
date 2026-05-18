from db.checkeos.restricciones_objeto import Restriccion

NOM_DB = "database.db"

LONG_NOM = 20
LONG_APE = 30
LONG_CORREO = 30
LONG_CONTRA = 12
LONG_TEL = 15

restricciones = {
    Restriccion("nombre", LONG_NOM),
    Restriccion("apellido", LONG_APE),
    Restriccion("correo", LONG_CORREO),
    Restriccion("contraseña", LONG_CONTRA),
    Restriccion("telefono", LONG_TEL)
}
