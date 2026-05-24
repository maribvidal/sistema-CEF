from flask import Blueprint, request, jsonify

from services.usuario_service import (
    listar_usuarios_service,
    registrar_usuario_service,
    listar_pagos_usuario_service,
    obtener_perfil_usuario_service,
    editar_perfil_usuario_service,
    modificar_contraseña_service,
    restablecer_contraseña_service,
    confirmar_nueva_contrasena_service
)

usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route("/usuarios", methods=["POST"])
def registrar_usuario():
    """Este endpoint registra un nuevo usuario en el sistema. 
        Recibe los datos del usuario en formato JSON, incluyendo 
        su DNI, nombre, apellido, contraseña, fecha de nacimiento, 
        correo electrónico, teléfono y género. Luego, llama al 
        servicio correspondiente para procesar el registro y devuelve 
        una respuesta con el resultado de la operación."""
    data = request.get_json()

    dni = data.get("dni")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    contraseña = data.get("contraseña")
    fecha_nac = data.get("fecha_nac")
    correo = data.get("correo")
    telefono = data.get("telefono")
    genero = data.get("genero")
    rol = data.get("rol")

    respuesta, status = registrar_usuario_service(
        dni,
        nombre,
        apellido,
        contraseña,
        fecha_nac,
        correo,
        telefono,
        genero,
        rol
    )

    return jsonify(respuesta), status

@usuario_bp.route("/usuarios/<int:usuario_id>/pagos", methods=["GET"])
def listar_pagos_usuario(usuario_id):
    """Este endpoint permite listar los pagos realizados 
        por un usuario específico."""
    respuesta, status = listar_pagos_usuario_service(usuario_id)

    return jsonify(respuesta), status

@usuario_bp.route("/usuarios/<int:usuario_id>/perfil", methods=["GET"])
def obtener_perfil_usuario(usuario_id):
    """Este endpoint permite obtener el perfil de un usuario 
        específico."""
    respuesta, status = obtener_perfil_usuario_service(usuario_id)

    return jsonify(respuesta), status

@usuario_bp.route("/usuarios/<int:usuario_id>/perfil", methods=["PUT"])
def editar_perfil_usuario(usuario_id):
    """Este endpoint permite editar el perfil de un usuario específico.
        Recibe los datos actualizados del usuario en formato JSON, 
        incluyendo su correo electrónico y teléfono. Luego, llama al 
        servicio correspondiente para procesar la actualización y devuelve 
        una respuesta con el resultado de la operación."""
    data = request.get_json()

    dni = data.get("dni")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    fecha_nac = data.get("fecha_nac")
    correo = data.get("correo")
    telefono = data.get("telefono")

    respuesta, status = editar_perfil_usuario_service(
        usuario_id,
        dni,
        nombre,
        apellido,
        fecha_nac,
        correo,
        telefono
    )

    return jsonify(respuesta), status

# HUs de las contraseñas

@usuario_bp.route("/usuarios/<int:usuario_id>/contraseña", methods=["PUT"])
def modificar_contraseña(usuario_id):
    """Este endpoint permite que un usuario pueda modificar su contraseña.
        Recibe el ID del usuario a través de la URL, la contraseña actual 
        del usuario y la nueva contraseña  en formato JSON."""
    
    data = request.get_json()

    contraseña_actual = data.get("contraseña_actual")
    contraseña_nueva = data.get("contraseña_nueva")

    # Por ahora, se devuelve una respuesta de ejemplo
    respuesta, status = modificar_contraseña_service(
        usuario_id, contraseña_actual, contraseña_nueva
    )

    return jsonify(respuesta), status

@usuario_bp.route("/usuarios/RestablecerContrasena", methods=["GET"])
def restablecer_contrasena():
    """Este endpoint permite que un usuario pueda restablecer su contraseña.
        Recibe el correo electrónico del usuario en formato JSON, y luego 
        se envía un correo con instrucciones para restablecer la contraseña."""
    
    data = request.get_json()

    correo = data.get("correo")

    respuesta, status = restablecer_contraseña_service(correo)

    return jsonify(respuesta), status


@usuario_bp.route("/usuarios/ConfirmarNuevaContrasena", methods=["GET"])
def confirmar_nueva_contrasena():
    """Este endpoint permite que un usuario confirme su nueva contraseña después de haber solicitado el restablecimiento.
        Recibe la nueva contraseña en formato JSON, y luego actualiza la contraseña del usuario en la base de datos."""
    
    data = request.get_json()

    nueva_contraseña = data.get("nueva_contraseña")
    correo = data.get("correo")

    respuesta, status = confirmar_nueva_contrasena_service(nueva_contraseña, correo)

    return jsonify(respuesta), status


@usuario_bp.route("/usuarios/ObtenerListaUsuarios", methods=["GET"])
def obtener_usuarios():
    """Este endpoint permite obtener una lista de todos los usuarios registrados en el sistema. 
        Se conecta a la base de datos, consulta la tabla de usuarios y devuelve la lista de usuarios en formato JSON."""

    respuesta , status = listar_usuarios_service()
        
    return jsonify(respuesta), status

# falta un delete