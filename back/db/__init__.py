from db.checkeos.restricciones_objeto import restriccion

NOM_DB = "database.db"

LONG_NOM = 20
LONG_APE = 30
LONG_CORREO = 30
LONG_CONTRA = 12
LONG_TEL = 15

restricciones = {
    restriccion("nombre", LONG_NOM),
    restriccion("apellido", LONG_APE),
    restriccion("correo", LONG_CORREO),
    restriccion("contraseña", LONG_CONTRA),
    restriccion("telefono", LONG_TEL)
}