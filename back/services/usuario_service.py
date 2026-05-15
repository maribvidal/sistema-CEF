from db.insertar_db import insertar_usuario
from db.usuario_requerido import checkeo_dni_registrado, checkeo_correo_registrado

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
    
    if checkeo_dni_registrado(dni):
        return {
            "error": "El DNI ya se encuentra registrado"
        }, 400
    
    if checkeo_correo_registrado(correo):
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