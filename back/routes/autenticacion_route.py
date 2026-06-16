from flask import Blueprint, request, jsonify
from flask import send_file

from db import modulo_qr
from services.autenticacion_service import login_service
from services.autenticacion_service import register_service
from services.usuario_service import registrar_usuario_service
from services.autenticacion_service import validar_reserva_service

autenticacion_bp = Blueprint("autenticacion", __name__)

@autenticacion_bp.route("/login", methods=["POST"])
def login():
    print("Recibiendo solicitud de login...")
    data = request.get_json()

    correo = data.get("correo")
    contraseña = data.get("contraseña")

    print("Datos recibidos - Correo: ", correo, " Contraseña: ", contraseña)
    respuesta, status = login_service(
        correo, contraseña
    )

    print("Respuesta: ", respuesta)
    return jsonify(respuesta), status

@autenticacion_bp.route("/registro", methods=["POST"])
def registro():
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
    rol_id = data.get("rol")
    
    respuesta, status = registrar_usuario_service(
        dni,
        nombre,
        apellido,
        contraseña,
        fecha_nac,
        correo,
        telefono,
        genero,
        rol_id 
    )

    return jsonify(respuesta), status


# Implementar validar QR no es necesario, ya que existe en clases_route una verificación de validar.
# Hay que ver si se implementa o no el visualizar qr, creo que es mucho mejor el simplemente generarlo por demanda así no ocupa espacio
@autenticacion_bp.route("/clientes/<int:id_cliente>/qr", methods=["GET"])
def generar_qr(id_cliente: int):
    qr = modulo_qr.generar_qr(id_cliente)

    return send_file(
        qr,
        mimetype='image/png'
    )


# Implementar validar QR, se debe recibir el id de la clase + id_cliente, y se debe validar que el client tenga una reserva para esa clase, y que la clase esté activa, y que la fecha y hora sean correctas. Si todo es correcto, se debe devolver un mensaje de éxito, sino se debe devolver un mensaje de error.
@autenticacion_bp.route("/clientes/<int:inst_clase_id>/validar_qr", methods=["POST"])
def validar_qr(inst_clase_id: int):
    # Aquí se debe implementar la lógica para validar el QR, utilizando el id_cliente y el inst_clase_id para verificar si el client tiene una reserva para esa clase, y si la clase está activa, y si la fecha y hora son correctas.
    # Si todo es correcto, se debe devolver un mensaje de éxito, sino se debe devolver un mensaje de error.
    data = request.get_json()
    id_usuario = data.get("id_usuario")

    respuesta, status = validar_reserva_service(inst_clase_id, id_usuario)

    return jsonify(respuesta), status