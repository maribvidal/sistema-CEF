from flask import Blueprint, request, jsonify
from services.empleados_service import modificar_empleado_service
from services.empleados_service import listar_empleados_service
from services.empleados_service import borrar_empleado_service
from services.empleados_service import desactivar_empleado_service
from services.empleados_service import listar_empleados_desactivados_service

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
    
    print("Hora de procesar request")
    print(request.content_type)
    print(request.data)
    data = request.get_json()

    print("Request procesado")

    nombre = data.get("nombre")
    apellido = data.get("apellido")
    correo = data.get("correo")
    contraseña = data.get("contraseña")
    fecha_nac = data.get("fecha_nac")
    telefono = data.get("telefono")
    genero = data.get("genero")
    rol_id = data.get("rol_id")
    print(" nombre: ", nombre, " apellido: ", apellido, " correo: ", correo, " contraseña: ", contraseña, " fecha_nac: ", fecha_nac, " telefono: ", telefono, " genero: ", genero, " rol_id: ", rol_id)
    print("empleado_dni: ", empleado_dni)

    respuesta, status = modificar_empleado_service(
        empleado_dni,
        nombre,
        apellido,
        correo,
        contraseña,
        fecha_nac,
        telefono,
        genero,
        rol_id,
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


@empleados_bp.route('/empleados/desactivados', methods=['GET'])
def listar_empleados_desactivados():
    """Endpoint para obtener la lista de empleados desactivados."""
    respuesta, status = listar_empleados_desactivados_service()
    
    return jsonify(respuesta), status