from db.operaciones import insertar_usuario, consultar_usuario_por_correo, consultar_usuario_por_dni
from db.checkeos.checkear_inputs import checkear_inputs

def registrar_usuario_service(
    dni: int,
    nombre: str,
    apellido: str,
    contraseña: str,
    correo: str,
    telefono: str,
    genero: str,
    edad: int 
):
    errores = checkear_inputs(
        [
            {"name": "dni", "value": dni},
            {"name": "nombre", "value": nombre},
            {"name": "apellido", "value": apellido},
            {"name": "correo", "value": correo},
            {"name": "contraseña", "value": contraseña},
            {"name": "telefono", "value": telefono},
            {"name": "genero", "value": genero},
            {"name": "edad", "value": edad}
        ]
    )
    
    if len(errores) > 0:
        return errores, 400

    if consultar_usuario_por_dni(dni):
        return {
            "error": "El DNI ya se encuentra registrado"
        }, 400
    
    if consultar_usuario_por_correo(correo):
        return {
            "error": "El correo electrónico ya se encuentra registrado"
        }, 400
    
    if edad < 14:
        return {
            "error": "El usuario debe ser mayor de 14 años"
        }, 400
      
    insertar_usuario(
        dni,
        nombre,
        apellido,
        contraseña,
        correo,
        telefono,
        genero,
        edad
    )

    return {
        "mensaje": "Usuario registrado exitosamente"
    }, 201