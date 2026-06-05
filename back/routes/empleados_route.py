from flask import Blueprint, request, jsonify
from services.empleados_service import (
    modificar_empleado_service,
    listar_empleados_service,
    borrar_empleado_service,
    desactivar_empleado_service,
    crear_recepcionista_service
)
from services.empleados_service import (
    modificar_empleado_service,
    listar_empleados_service,
    borrar_empleado_service,
    desactivar_empleado_service,
    crear_recepcionista_service
)

empleados_bp = Blueprint('empleados', __name__)

@empleados_bp.route('/empleados', methods=['GET'])
def listar_empleados():
    """Endpoint para obtener la lista de empleados."""
    respuesta, status = listar_empleados_service()
    
    return jsonify(respuesta), status

@empleados_bp.route("/empleados/<int:empleado_dni>", methods=["PUT"])
def modificar_empleado(empleado_dni):
    """Endpoint para modificar un empleado específico. 
        Recibe el ID del empleado a modificar y los nuevos datos en formato JSON."""
    
    data = request.get_json()

    dni_nuevo = data.get("nuevo_dni")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    correo = data.get("correo")
    genero = data.get("genero")
    rol_id = data.get("rol_id")

    respuesta, status = modificar_empleado_service(
        empleado_dni,
        dni_nuevo,
        nombre,
        apellido,
        correo,
        genero,
        rol_id
    )

    return jsonify(respuesta), status

@empleados_bp.route("/empleados/<int:empleado_dni>", methods=["DELETE"])
def borrar_empleado(empleado_dni):

    respuesta, status = borrar_empleado_service(empleado_dni)

    return jsonify(respuesta), status

@empleados_bp.route("/empleados/<int:empleado_dni>/desactivar", methods=["PATCH"])
def desactivar_empleado(empleado_dni):
    respuesta, status = desactivar_empleado_service(empleado_dni)
    return jsonify(respuesta), status

@empleados_bp.route('/empleados/recepcionistas', methods=['POST'])
def crear_recepcionista():
    """Endpoint para crear un recepcionista."""

    data = request.get_json()

    dni = data.get("dni")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    correo = data.get("correo")
    contraseña = data.get("contraseña")
    genero = data.get("genero")

    respuesta, status = crear_recepcionista_service(dni, nombre, apellido, correo, contraseña, genero)

    return jsonify(respuesta), status
