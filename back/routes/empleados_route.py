from flask import Blueprint, request, jsonify

from services.empleados_service import cambiar_rol_empleado, obtener_empleados_service

empleados_bp = Blueprint("empleados", __name__)


@empleados_bp.route("/empleados", methods=["GET"])
def listar_empleados():
    respuesta, status = obtener_empleados_service()

    return jsonify(respuesta), status

## preguntar si lo queremos hacer con dni, con id o con correo
@empleados_bp.route("/empleados/<int:dni>/rol", methods=["PUT"])
def modificar_rol(dni):

    data = request.get_json()

    nuevo_rol_id = data.get("rol_id")

    if nuevo_rol_id is None:
        return jsonify({
            "error": "rol_id es obligatorio"
        }), 400

    respuesta, status = cambiar_rol_empleado(
        dni,
        nuevo_rol_id
    )

    return jsonify(respuesta), status
