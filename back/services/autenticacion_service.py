import jwt
from datetime import datetime, timedelta
from db.operaciones.consultar_db import buscar_empleado_por_correo, consultar_usuario_por_correo

# Clave secreta para firmar JWT (en producción, usar variable de entorno)
JWT_SECRET_KEY = "tu-clave-secreta-super-segura-aqui"
JWT_EXPIRATION_HOURS = 24

def login_service(correo: str, contraseña: str):
    """El tipo se refiere a si es cliente, recepcionista 
        o administrador. El rol es necesario para después
        checkear los permisos de ciertos endpoints."""
    usuario = consultar_usuario_por_correo(correo)

    if usuario:
        if usuario["contraseña"] != contraseña:
            return {"error": "Contraseña incorrecta"}, 400

        # Generar JWT
        token = _generate_jwt({
            "id": usuario["id"],
            "nombre": usuario["nombre"],
            "tipo": "CLIENTE",
            "rol": ""
        })

        return {
            "mensaje": "Inicio de sesión exitoso",
            "token": token,
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

    # Generar JWT
    token = _generate_jwt({
        "id": empleado["id"],
        "nombre": empleado["nombre"],
        "tipo": empleado["tipo"],
        "rol": empleado["rol"]
    })

    return {
        "mensaje": "Inicio de sesión exitoso",
        "token": token,
        "usuario": {
            "id": empleado["id"],
            "nombre": empleado["nombre"],
            "tipo": empleado["tipo"],
            "rol": empleado["rol"]
        }
    }, 200

def _generate_jwt(user_data):
    """Genera un JWT token con los datos del usuario."""
    payload = {
        **user_data,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return token

def verify_jwt(token):
    """Verifica y decodifica un JWT token."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
