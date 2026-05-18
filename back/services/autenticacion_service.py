from db.operaciones import buscar_empleado_por_correo, consultar_usuario_por_correo

def login_service(correo: str, contraseña: str):
    """El tipo se refiere a si es cliente, recepcionista 
        o administrador. El rol es necesario para después
        checkear los permisos de ciertos endpoints."""
    usuario = consultar_usuario_por_correo(correo)

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
