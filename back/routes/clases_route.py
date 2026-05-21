from flask import Blueprint, request, jsonify
from services.clases_service import (
    listar_clases_service, publicar_clase_service, 
    modificar_clase_service, eliminar_clase_service,
    listar_actividades_service, listar_profesores_service
)

clases_bp = Blueprint('clases', __name__)
 
@clases_bp.route('/clases', methods=['GET'])
def listar_clases():
    """Este endpoint permite listar todas las clases disponibles 
        en el sistema."""
    respuesta, status = listar_clases_service()
    
    return jsonify(respuesta), status

@clases_bp.route('/actividades', methods=['GET'])
def listar_actividades():
    """Endpoint para obtener la lista de actividades."""
    respuesta, status = listar_actividades_service()
    
    return jsonify(respuesta), status

@clases_bp.route('/empleados', methods=['GET'])
def listar_profesores():
    """Endpoint para obtener la lista de profesores (empleados)."""
    respuesta, status = listar_profesores_service()
    
    return jsonify(respuesta), status

@clases_bp.route('/clases', methods=['POST'])
def publicar_clase():
    """Este endpoint permite subir una nueva clase al
        sistema. Los datos son recibidos en formato JSON."""

    data = request.get_json()

    estado = data.get("estado")
    id_actividad = data.get("id_actividad")
    id_profesor = data.get("id_profesor")

    respuesta, status = publicar_clase_service(
        estado,
        id_actividad,
        id_profesor
    )

    return jsonify(respuesta), status

@clases_bp.route("/clases/<int:id_clase>", methods=["DELETE"])
def eliminar_clase(id_clase):
    """Este endpoint permite eliminar una clase específica. 
        Recibe el ID de la clase a eliminar en formato JSON."""

    respuesta, status = eliminar_clase_service(id_clase)

    return jsonify(respuesta), status

@clases_bp.route("/clases/<int:id_clase>", methods=["PUT"])
def modificar_clase(id_clase):
    """Este endpoint permite modificar los detalles de una 
        clase específica. Recibe el ID de la clase a modificar 
        y los nuevos datos en formato JSON."""
    data = request.get_json()

    estado = data.get("estado")
    id_actividad = data.get("id_actividad")
    id_profesor = data.get("id_profesor")

    respuesta, status = modificar_clase_service(
        id_clase,
        estado,
        id_actividad,
        id_profesor
    )

    return jsonify(respuesta), status

"""
def cancelar_clase():
    Este endpoint permite cancelar una clase específica. 
        Recibe el ID de la clase a cancelar en formato JSON.
    data = request.get_json()

    # Tengo que ver como se cancelaba una clase
"""