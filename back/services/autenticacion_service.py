from db.usuario_requerido import buscar_empleado_por_correo, buscar_usuario_por_correo

# el tipo se refiere a si es cliente, recepcionista o administrador
# el rol es necesario para despues checkear los permisos de ciertos endpoints
def login_service(correo: str, contraseña: str):
    usuario = buscar_usuario_por_correo(correo)

    if usuario:
        if usuario["contraseña"] != contraseña:
            return {"error": "Contraseña incorrecta"}, 400

        return {
            "mensaje": "Inicio de sesión exitoso",
            "usuario": {
                "id": usuario["id"],
                "nombre": usuario["nombre"],
                "tipo": "CLIENTE",
                "rol": ""
            }
        }, 200

    empleado = buscar_empleado_por_correo(correo)

    if not empleado:
        return {"error": "Usuario no registrado"}, 404

    if empleado["contraseña"] != contraseña:
        return {"error": "Contraseña incorrecta"}, 400

    return {
        "mensaje": "Inicio de sesión exitoso",
        "usuario": {
            "id": empleado["id"],
            "nombre": empleado["nombre"],
            "tipo": empleado["tipo"],
            "rol": empleado["rol"]
        }
    }, 200