from db.operaciones.conectar_db import conectarse_db
from db.operaciones.clases.consultar_db import listar_clases, consultar_clase_por_id, consultar_clase_por_sala_dia_hora
from db.operaciones.clases.insertar_db import insertar_clase
from db.operaciones.clases.modificar_db import modificar_clase_estado
from db.operaciones.actividades.consultar_db import consultar_actividad_por_id
from db.operaciones.profesores.consultar_db import consultar_profesor_por_id
from db.operaciones.salas.consultar_db import consultar_sala_por_id
from db.operaciones.reservas.insertar_db import insertar_reserva
from enums.dias import Dias
from pprint import pprint

def _msj_error_helper(razon: str, cursor):
    cursor.connection.close()
    return {
        "status": "error",
        "message": razon
    }

def listar_clases_service():
    """Service que lista las clases"""

    cursor = conectarse_db()

    respuesta = listar_clases(cursor)

    if respuesta['status'] == 'error':
        cursor.connection.close()
        return respuesta, 400

    if respuesta['status'] == 'success' and not respuesta['data']:
        return _msj_error_helper("No se encontraron clases.", cursor), 401

    cursor.connection.close()
    return respuesta, 200

def publicar_clase_service(
    estado: str,
    id_actividad: int,
    id_profesor: int,
    id_sala: int,
    dia: Dias,
    hora: str,
    cupo_maximo: int
):
    """Service que publica una clase"""

    cursor = conectarse_db()

    # Comprobar que la actividad existe

    resp_act = consultar_actividad_por_id(id_actividad, cursor)
    if resp_act['status'] == 'error':
        cursor.connection.close()
        return resp_act, 400

    # Comprobar que el profesor existe

    resp_prof = consultar_profesor_por_id(id_profesor, cursor)
    if resp_prof['status'] == 'error':
        cursor.connection.close()
        return resp_prof, 401

    # Comprobar que la sala existe

    resp_sala = consultar_sala_por_id(id_sala, cursor)
    if resp_sala['status'] == 'error':
        cursor.connection.close()
        return resp_sala, 402

    # Comprobar que la sala no esté ocupada en ese día y hora

    resp_clas = consultar_clase_por_sala_dia_hora(id_sala, dia, hora, cursor)
    if resp_clas['status'] == 'success':
        return _msj_error_helper("La sala ya se encuentra ocupada en ese día y hora.", cursor), 403

    # Comprobar que la sala escogida tenga la capacidad suficiente

    capacidad_sala = resp_sala["data"]["capacidad"]

    if (capacidad_sala < cupo_maximo):
        return _msj_error_helper("El cupo máximo ingresado supera la capacidad de la sala.", cursor), 404

    # Intentar insertar la clase

    resp_inser_clas = insertar_clase(estado, id_actividad, id_profesor, id_sala, dia, hora, cupo_maximo, cursor)

    if resp_inser_clas['status'] == 'error':
        cursor.connection.close()
        return resp_inser_clas['message'], 405

    cursor.connection.commit()
    cursor.connection.close()

    return {
        "status": "success",
        "message": "Clase publicada exitosamente."
    }, 200

def modificar_clase_service(
    clase_id: int,
    estado: str,
    id_actividad: int,
    id_profesor: int,
    fecha,
    hora: str,
    sala: int,
    cupo_maximo: int
):
    """Service que modifica una clase"""

    cursor = conectarse_db()

    respuesta_consulta = consultar_clase_por_id(clase_id, cursor)

    if respuesta_consulta['status'] == 'error':
        cursor.connection.close()
        return respuesta_consulta, 400

    if respuesta_consulta['status'] == 'success' and not respuesta_consulta['data']:
        cursor.connection.close()
        return {
            "error": "Clase no encontrada."
        }, 401

    # respuesta = modificar_clase(clase_id, estado, id_actividad, id_profesor, cupo_maximo, cursor)

    if respuesta['status'] == 'error':
        cursor.connection.close()
        return respuesta, 402

    respuesta2 = modificar_clase_ocurrir_sala(clase_id, sala, fecha, hora, cursor)

    if respuesta2['status'] == 'error':
        cursor.connection.close()
        return respuesta2, 403
    
    cursor.connection.commit()
    cursor.connection.close()

    return {
        "message": "Clase modificada exitosamente."
    }, 200

def eliminar_clase_service(clase_id: int):
    """Service que elimina una clase"""

    ## Recibir id del usuario. Buscar rol del usuario.
    ## Si no tiene el permiso necesario, tirar un error.

    cursor = conectarse_db()

    respuesta_consulta = consultar_clase_por_id(clase_id, cursor)

    if respuesta_consulta['status'] == 'error':
        cursor.connection.close()
        return respuesta_consulta, 400

    if respuesta_consulta['status'] == 'success' and not respuesta_consulta['data']:
        cursor.connection.close()
        return {
            "error": "Clase no encontrada."
        }, 401
    

    respuesta = modificar_clase_estado(clase_id, 'Borrado', cursor)

    if respuesta['status'] == 'error':
        cursor.connection.close()
        return respuesta, 402

    cursor.connection.commit()
    cursor.connection.close()
    return {
        "message": "Clase eliminada exitosamente."
    }, 200

def cancelar_clase_service(clase_id: int):
    """Service que cancela una clase"""

    cursor = conectarse_db()

    respuesta_consulta = consultar_clase_por_id(clase_id, cursor)

    if respuesta_consulta['status'] == 'error':
        cursor.connection.close()
        return respuesta_consulta, 400

    if respuesta_consulta['status'] == 'success' and not respuesta_consulta['data']:
        cursor.connection.close()
        return {
            "error": "Clase no encontrada."
        }, 401

    respuesta = modificar_clase_estado(clase_id, 'Cancelada', cursor)

    if respuesta['status'] == 'error':
        cursor.connection.close()
        return respuesta, 402

    cursor.connection.commit()
    cursor.connection.close()
    return {
        "message": "Clase cancelada exitosamente."
    }, 200

def reservar_clase_service(id_ins_clase: int, id_usuario: int):
    """Service que, dado un usuario, lo intenta inscribir
        en una clase con una fecha y hora dada."""

    cursor = conectarse_db()

    # Insertar reserva de clase 
    res_reserva = insertar_reserva(id_usuario, id_ins_clase, cursor)
    if res_reserva["status"] == 'error':
        cursor.connection.close()
        return res_reserva, 400

    cursor.connection.commit()
    cursor.connection.close()

    return res_reserva, 200

def verificar_inscripcion_usuario_clase_service(id_clase, id_usuario, dia: Dias, hora):
    """Service que devuelve si un usuario se encuentra
        inscripto o no en una clase a una fecha y hora dada."""

    cursor = conectarse_db()

    # Comprobar si clase existe

    respuesta_consulta = consultar_clase_por_id(id_clase, cursor)

    if respuesta_consulta['status'] == 'error':
        cursor.connection.close()
        return respuesta_consulta, 400

    if respuesta_consulta['status'] == 'success' and not respuesta_consulta['data']:
        cursor.connection.close()
        return {
            "error": "Clase no encontrada."
        }, 401

    # Comprobar si el usuario está inscripto

    # res_usuario_clase = obtener_clase_usuario_dia_hora(id_usuario, dia, hora, cursor)

    if res_usuario_clase['status'] == 'error':
        cursor.connection.close()
        return res_usuario_clase['message'], 402

    if str(res_usuario_clase['data']) == "[]":
        cursor.connection.close()
        return {
            "error": "El usuario no se encuentra inscripto en la clase."
        }, 403

    cursor.connection.close()
    return {
        "message": "El usuario se encuentra inscripto."
    }, 200
