from flask import Blueprint, request, jsonify
from services.clases_service import (
    listar_clases_service, publicar_clase_service, 
    modificar_clase_service, eliminar_clase_service,
    cancelar_clase_service
)

clases_bp = Blueprint('clases', __name__)
 
@clases_bp.route('/clases', methods=['GET'])
def listar_clases():
    """Este endpoint permite listar todas las clases disponibles 
        en el sistema."""
    respuesta, status = listar_clases_service()
    
    return jsonify(respuesta), status

@clases_bp.route('/clases', methods=['POST'])
def publicar_clase():
    """Este endpoint permite subir una nueva clase al
        sistema. Los datos son recibidos en formato JSON."""

    data = request.get_json()

    estado = data.get("estado")
    id_actividad = data.get("id_actividad")
    id_profesor = data.get("id_profesor")
    fecha = data.get("fecha")
    hora = data.get("hora")
    sala = data.get("sala")

    respuesta, status = publicar_clase_service(
        estado,
        id_actividad,
        id_profesor,
        fecha,
        hora,
        sala
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
    fecha = data.get("fecha")
    hora = data.get("hora")
    sala = data.get("sala")

    respuesta, status = modificar_clase_service(
        id_clase,
        estado,
        id_actividad,
        id_profesor,
        fecha,
        hora,
        sala
    )

    return jsonify(respuesta), status

## Habría que ver si a una clase cancelada hay que hacerle otra
## cosa que no sea cambiarle el estado.

@clases_bp.route("/clases/<int:id_clase>", methods=["PATCH"])
def cancelar_clase(id_clase):
    """Este endpoint permite cancelar una clase específica. 
        Recibe el ID de la clase a cancelar en formato JSON."""

    respuesta, status = cancelar_clase_service(id_clase)

    return jsonify(respuesta), status

## No estoy seguro de como implementar esto. Mañana lo voy
## a ver mejor, porque también podríamos implementar un
## endpoint que reciba simplemente la id del 
## clase_ocurrir_sala en vez de esto.

@clases_bp.route("/clases/<int:id_clase>/reservar", methods)
def reservar_clase(id_clase):
    """Este endpoint permite inscribir a un usuario a
        una clase específica. Esto se hace pidiendo el
        id del usuario, la fecha, y la hora de la clase."""

    # Por implementar

    pass
