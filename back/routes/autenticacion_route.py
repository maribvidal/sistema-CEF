from flask import Blueprint, request, jsonify

from services.autenticacion_service import login_service
from services.autenticacion_service import register_service
from services.usuario_service import registrar_usuario_service

autenticacion_bp = Blueprint("autenticacion", __name__)

@autenticacion_bp.route("/login", methods=["POST"])
def login():
    print("Recibiendo solicitud de login...")
    data = request.get_json()

    correo = data.get("correo")
    contraseña = data.get("contraseña")

    print("Datos recibidos - Correo: ", correo, " Contraseña: ", contraseña)
    respuesta, status = login_service(
        correo,
        contraseña
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
    rol_id = data.get("rol_id")
    
    print("Datos recibidos para registro - DNI: ", dni, " Nombre: ", nombre, " Apellido: ", apellido, " Contraseña: ", contraseña, " Fecha de Nacimiento: ", fecha_nac, " Correo: ", correo, " Teléfono: ", telefono, " Género: ", genero, " Rol ID: ", rol_id)

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