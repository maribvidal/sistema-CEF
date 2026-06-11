from flask import Blueprint, request, jsonify
from services.clases_service import (
    anotarse_lista_espera_service, listar_clases_service, publicar_clase_service,
    reservar_clase_service, registrar_asistencia_clase_service, rechazar_asistencia_clase_service
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
    id_sala = data.get("id_sala")
    dia = data.get("dia")
    hora = data.get("hora")
    cupo_maximo = data.get("cupo_maximo")

    return publicar_clase_service(estado, id_actividad, id_profesor, id_sala, dia, hora, cupo_maximo)

@clases_bp.route("/clases/<int:id_clase>", methods=["DELETE"])
def eliminar_clase(id_clase):
    """Este endpoint permite eliminar una clase específica. 
        Recibe el ID de la clase a eliminar en formato JSON."""

    ## TODO: Repensar implementación del endpoint

    return {
        "status": "success",
        "message": "En remodelación."
    }, 200

@clases_bp.route("/clases/<int:id_clase>", methods=["PUT"])
def modificar_clase(id_clase):
    """Este endpoint permite modificar los detalles de una 
        clase específica. Recibe el ID de la clase a modificar 
        y los nuevos datos en formato JSON."""

    ## TODO: Repensar implementación del endpoint

    return {
        "status": "success",
        "message": "En remodelación."
    }, 200

## Habría que ver si a una clase cancelada hay que hacerle otra
## cosa que no sea cambiarle el estado.

@clases_bp.route("/clases/<int:id_clase>", methods=["PATCH"])
def cancelar_clase(id_clase):
    """Este endpoint permite cancelar una clase específica. 
        Recibe el ID de la clase a cancelar en formato JSON."""

    ## TODO: Repensar implementación del endpoint

    return {
        "status": "success",
        "message": "En remodelación."
    }, 200

@clases_bp.route("/clases/<int:id_ins_clase>/reservar", methods=["PUT"])
def reservar_clase(id_ins_clase):
    """Este endpoint permite inscribir a un usuario a
        una clase específica. Esto se hace pidiendo el
        id del usuario y el id de la instancia de la clase."""

    data = request.get_json()

    id_usuario = data.get("id_usuario")

    return reservar_clase_service(id_ins_clase, id_usuario)

@clases_bp.route("/clases/<int:id_clase>", methods=["GET"])
def verificar_inscripcion_usuario_clase(id_clase):
    """Este endpoint permite verificar si un usuario
        tiene una inscripción a una clase específica,
        en un día y hora dado."""

    ## TODO: Repensar implementación del endpoint

    return {
        "status": "success",
        "message": "En remodelación."
    }, 200

@clases_bp.route("/clases/<int:id_clase>/inscripciones", methods=["POST"])
def anotarse_lista_espera(id_clase):
    """Este endpoint permite verificar si un usuario
        tiene una inscripción a una clase específica,
        en un día y hora dado."""
        
    data = request.get_json()

    id_usuario = data.get("id_usuario")

    respuesta, status = anotarse_lista_espera_service(id_clase, id_usuario)
    
    return jsonify(respuesta), status

# la logica seria que cuando se cancela una reserva entonces se notifica via mail a alguno de la lista de abonado o de individual para confirmar asistencia
# si hago 2 endpoints para cada uno de las tipo de usuario va a ser identico
# pienso que el front seria el que agarra directamente el id_usuario cuando el mail lo redirija a la pagina de confirmacion y que pregunte luego si es abonado o no
@clases_bp.route("/clases/<int:id_clase>/confirmar_asistencia", methods=["POST"])
def registrar_asistencia_clase(id_clase):
    """Este endpoint permite registrar la asistencia de un usuario
        a una clase específica. Recibe el ID del usuario y el ID
        de la clase en formato JSON."""
        
    data = request.get_json()

    id_usuario = data.get("id_usuario")
    
    respuesta, status = registrar_asistencia_clase_service(id_clase, id_usuario)
    
    return jsonify(respuesta), status

# pienso que las hu de usuario se diferencian en este caso desde el front
# en el caso de la confirmacion y la cancelacion se llaman a distintos endpoints en el back. no funcionan de la misma forma que lo veniamos haciendo con los otros endpoints que era
# un endpoint por hu

@clases_bp.route("/clases/<int:id_clase>/rechazar_asistencia", methods=["POST"])
def rechazar_asistencia_clase(id_clase):
    """Este endpoint permite rechazar la asistencia de un usuario
        a una clase específica. Recibe el ID del usuario y el ID
        de la clase en formato JSON."""
        
    data = request.get_json()

    id_usuario = data.get("id_usuario")
    
    respuesta, status = rechazar_asistencia_clase_service(id_clase, id_usuario)
    
    return jsonify(respuesta), status