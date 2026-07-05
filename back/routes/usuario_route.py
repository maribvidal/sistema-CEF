from flask import Blueprint, request, jsonify

from db.operaciones.usuarios.modificar_db import modificar_perfil_usuario
from db.operaciones.conectar_db import conectarse_db

from services.usuario_service import (
    listar_usuarios_service,
    listar_pagos_usuario_service,
    obtener_perfil_usuario_service,
    editar_perfil_usuario_service,
    modificar_contraseña_service,
    restablecer_contraseña_service,
    confirmar_nueva_contrasena_service,
    subir_avatar_usuario_service,
    obtener_avatar_usuario_service,
    verificar_correo_usuario_service,
    obtener_clases_usuario_service,
    desactivar_usuario_service,
    obtener_reserva_usuario_instancia_service,
    reactivar_usuario_service,
    eliminar_cliente_service
)

from services.reservas_service import (
    obtener_reserva_usuario_inst_clase_service
)

usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route("/usuarios/<int:usuario_id>/pagos", methods=["GET"])
def listar_pagos_usuario(usuario_id):
    """Este endpoint permite listar los pagos realizados 
        por un usuario específico."""
    respuesta, status = listar_pagos_usuario_service(usuario_id)

    return jsonify(respuesta), status

@usuario_bp.route("/usuarios/<int:usuario_id>/<int:inst_clase_id>/reserva", methods=["GET"])
def obtener_reserva_usuario_instancia(usuario_id, inst_clase_id):
    """Este endpoint permite obtener la reserva de un usuario para una instancia de clase específica."""

    respuesta, status = obtener_reserva_usuario_instancia_service(usuario_id, inst_clase_id)
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

@usuario_bp.route("/usuarios/RestablecerContrasena", methods=["POST"])
def restablecer_contrasena():
    """Este endpoint permite que un usuario pueda restablecer su contraseña.
        Recibe el correo electrónico del usuario en formato JSON, y luego 
        se envía un correo con instrucciones para restablecer la contraseña."""
    
    data = request.get_json()

    correo = data.get("correo")

    respuesta, status = restablecer_contraseña_service(correo)

    return jsonify(respuesta), status


@usuario_bp.route("/usuarios/ConfirmarNuevaContrasena", methods=["PUT"])
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

@usuario_bp.route("/usuarios/<int:usuario_id>/clases", methods=["GET"])
def obtener_clases_usuario(usuario_id):
    """Este endpoint permite obtener una lista de las clases a las que un usuario está inscrito.
        Se conecta a la base de datos, consulta la tabla de clases y devuelve la lista de clases en formato JSON."""

    respuesta, status = obtener_clases_usuario_service(usuario_id)

    return jsonify(respuesta), status

@usuario_bp.route("/usuarios/<int:usuario_id>/avatar", methods=["POST"])
def subir_avatar_usuario(usuario_id):
    """Este endpoint permite subirle un avatar a un usuario dado.
        Recibe el ID del usuario a través de la URL, y el archivo de imagen
        por medio de parámetro en el JSON. Luego, inserta la imágen en la
        base de datos, y al final asocia el ID de la imagen al usuario."""

    # Recibimos la imagen como un string codificado en base64
    # por medio de un parámetro en el JSON
    data = request.get_json()
    avatar = data.get("avatar")

    respuesta, status = subir_avatar_usuario_service(usuario_id, avatar)

    return jsonify(respuesta), status

@usuario_bp.route("/usuarios/<int:usuario_id>/avatar", methods=["GET"])
def obtener_avatar_usuario(usuario_id):
    """Este endpoint permite obtener el avatar de un usuario dado.
        Recibe el ID del usuario a través de la URL, y devuelve el avatar
        asociado a ese usuario como fue codificado cuando se recibió."""

    respuesta, status = obtener_avatar_usuario_service(usuario_id)

    return jsonify(respuesta), status


@usuario_bp.route("/usuarios/<int:usuario_id>/verificar_correo", methods=["GET"])
def verificar_correo_usuario(usuario_id):
    """Este endpoint permite verificar el correo de un usuario dado.
        Recibe el ID del usuario a través de la URL, y devuelve una respuesta
        indicando si el correo está verificado."""

    respuesta, status = verificar_correo_usuario_service(usuario_id)

    return jsonify(respuesta), status

@usuario_bp.route("/usuarios/<int:usuario_id>/desactivar", methods=["PUT"])
def desactivar_usuario(usuario_id):
    """Este endpoint permite desactivar un usuario.
        Recibe el ID del usuario a través de la URL, y devuelve
        una respuesta de confirmación si todo salió bien."""
    
    respuesta, status = desactivar_usuario_service(usuario_id)

    return jsonify(respuesta), status

@usuario_bp.route("/usuarios/<int:usuario_id>/<int:inst_clase_id>/reserva")
def obtener_reserva_usuario_inst_clase(usuario_id, inst_clase_id):
    """Este endpoint permite obtener la reserva de
        un usuario en una instancia de clase dada."""
    
    respuesta, status = obtener_reserva_usuario_inst_clase_service(usuario_id, inst_clase_id)

    return jsonify(respuesta), status

@usuario_bp.route("/usuarios/confirmar_cambio_correo/<int:usuario_id>/<nuevo_correo>", methods=["GET"])
def confirmar_cambio_correo(usuario_id, nuevo_correo):
    """Endpoint simplificado. Recibe los datos del link y actualiza."""
    
    cursor = conectarse_db()
    
    # Hacemos el cambio real del correo en la base de datos
    res = modificar_perfil_usuario(
        cursor,
        usuario_id,
        None, None, None, None,  # No tocamos los otros datos
        nuevo_correo,            # Guardamos el nuevo correo definitivamente
        None
    )

    if res['status'] == 'error':
        cursor.connection.close()
        return jsonify({"message": "Error al procesar el cambio de correo."}), 500

    cursor.connection.commit()
    cursor.connection.close()

    return jsonify({
        "message": "Tu correo electrónico ha sido actualizado con éxito."
    }), 200


@usuario_bp.route("/usuarios/<int:usuario_id>/reactivar", methods=["PUT"])
def reactivar_usuario(usuario_id):
    """Endpoint para reactivar un usuario desactivado."""
    respuesta, status = reactivar_usuario_service(usuario_id)
    return jsonify(respuesta), status

#   const response = await apiClient.put(`/usuarios/${userId}/eliminar`);
@usuario_bp.route("/usuarios/<int:usuario_id>/eliminar", methods=["PUT"])
def eliminar_cliente(usuario_id):
    """Endpoint para eliminar un cliente (cambiar su rol a +20)."""
    print("HOLAAAAAAAAAAAAAAAAAAAAAAA")
    respuesta, status = eliminar_cliente_service(usuario_id)
    return jsonify(respuesta), status