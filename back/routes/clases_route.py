from flask import Blueprint, request, jsonify
from services.clases_service import (
    cancelar_clase_service, listar_clases_service, modificar_clase_service, publicar_clase_service,
    reservar_clase_service, verificar_inscripcion_usuario_clase_service,
    eliminar_clase_service, anotarse_lista_espera_service
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

    # ESTA IMPLEMENTACIÓN PUEDE SERVIR PARA PRÓXIMAS IMPLEMENTACIÓNES, CON ESTO NOS ASEGURAMOS QUE EL REQUEST ESTÉ BIEN Y NO HAYA NINGUN "NONE" O ALGO ASÍ
    body = request.get_json()

    campos = [
        "estado",
        "id_actividad",
        "id_profesor",
        "id_sala",
        "dia",
        "hora",
        "cupo_maximo"
    ]

    for campo in campos:
        if campo not in body:
            return {"error": f"Falta el campo {campo}"}, 400

    estado = body.get("estado")
    id_actividad = body.get("id_actividad")
    id_profesor = body.get("id_profesor")
    id_sala = body.get("id_sala")
    dia = body.get("dia")
    hora = body.get("hora")
    cupo_maximo = body.get("cupo_maximo")

    return publicar_clase_service(estado, id_actividad, id_profesor, id_sala, dia, hora, cupo_maximo)

@clases_bp.route("/clases/<int:id_clase>", methods=["DELETE"])
def eliminar_clase(id_clase):
    """Este endpoint permite eliminar una clase específica. 
        Recibe el ID de la clase a eliminar en formato JSON."""

    # Lozi: La explicación de mi implementación se encuentra dentro de la función eliminar_clase...
    return eliminar_clase_service(id_clase)


@clases_bp.route("/clases/<int:id_clase>", methods=["PUT"])
def modificar_clase(id_clase):
    """Este endpoint permite modificar los detalles de una 
        clase específica. Recibe el ID de la clase a modificar 
        y los nuevos datos en formato JSON."""

    ## TODO: Repensar implementación del endpoint

    # ESTA IMPLEMENTACIÓN PUEDE SERVIR PARA PRÓXIMAS IMPLEMENTACIÓNES, CON ESTO NOS ASEGURAMOS QUE EL REQUEST ESTÉ BIEN Y NO HAYA NINGUN "NONE" O ALGO ASÍ
    body = request.get_json()
    print("JSON RECIBIDOOOOOOOOO:")
    print(body)

    campos = [
        "estado",
        "id_actividad",
        "id_profesor",
        "id_sala",
        "dia",
        "hora",
        "cupo_maximo"
    ]

    for campo in campos:
        if campo not in body:
            return {"error": f"Falta el campo {campo}"}, 400


    return modificar_clase_service(id_clase, **body)
    

## Habría que ver si a una clase cancelada hay que hacerle otra
## cosa que no sea cambiarle el estado.

@clases_bp.route("/clases/<int:id_clase>", methods=["PATCH"])
def cancelar_clase(id_clase):
    """Este endpoint permite cancelar una clase específica. 
        Recibe el ID de la clase a cancelar en formato JSON."""

    # Lozi: Propuesta de implementación se encuentra en cancelar_clase_service..
    return cancelar_clase_service(id_clase)



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
    # Para poder verificar su inscripción, nosotros tenemos el id de la clase pero necesitamos un distintivo para saber de que usuario se trata
    data = request.get_json()
    id_usuario = data.get("id_usuario")
    fecha = data.get("fecha")

    return verificar_inscripcion_usuario_clase_service(id_clase, id_usuario, fecha)

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

    # respuesta, status = anotarse_lista_espera_service(id_clase, id_usuario)
    
    return {
        "status": "success",
        "message": "En remodelación."
    }, 200
