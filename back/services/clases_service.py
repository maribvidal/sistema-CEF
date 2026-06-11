from back.db.operaciones.asistencias import verificar_asistencia_usuario_clase, registrar_asistencia
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.clases.consultar_db import listar_clases, consultar_clase_por_id, consultar_clase_por_sala_dia_hora
from db.operaciones.clases.insertar_db import insertar_clase
from db.operaciones.clases.modificar_db import modificar_clase_estado
from db.operaciones.actividades.consultar_db import consultar_actividad_por_id
from db.operaciones.profesores.consultar_db import consultar_profesor_por_id
from db.operaciones.salas.consultar_db import consultar_sala_por_id
from db.operaciones.reservas.insertar_db import insertar_reserva
from db.operaciones.reservas.consultar_db import obtener_reservas_usuario_dia_hora, obtener_reservas_usuario_inst_clase
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_id, obtener_clase_usuario_dia_hora, verificar_usuario_abonado
from db.operaciones.instancias_clases.consultar_db import consultar_instancia_clase_por_id, obtener_reservas_instancia_clase
from db.operaciones.instancias_clases.insertar_db import insertar_instancia_clase
from db.modulo_fechas import generar_fecha_actual
from enums.dias import Dias
from db.operaciones.listas_espera import anotarse_lista_abonados, anotarse_lista_publico_general
from db.operaciones.reservas import consultar_reserva_por_usuario_clase

def _msj_error_helper(razon: str, cursor):
    cursor.connection.close()
    return {
        "status": "error",
        "message": razon
    }

def _msj_exito_helper(razon: str, cursor, res=None):
    cursor.connection.close()
    if res is None:
        return {
            "status": "success",
            "message": razon
        }, 200
    else:
        return {
            "status": "success",
            "message": razon,
            "data": res
        }, 200

def listar_clases_service():
    """Service que lista las clases"""

    cursor = conectarse_db()

    respuesta = listar_clases(cursor)

    if respuesta['status'] == 'error':
        cursor.connection.close()
        return respuesta, 400
    if respuesta['status'] == 'success' and respuesta['data'] is None:
        return _msj_error_helper("No se encontró ninguna clase en el sistema.", cursor), 401

    return _msj_exito_helper("Se devolvió una lista de clases con éxito.", cursor, respuesta["data"])

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
        return _msj_error_helper(resp_act['message'], cursor), 400
    if resp_act['status'] == 'success' and resp_act['data'] is None:
        return _msj_error_helper("Se intentó devolver una actividad pero no se encontró nada.", cursor), 401

    # Comprobar que el profesor existe

    resp_prof = consultar_profesor_por_id(id_profesor, cursor)
    if resp_prof['status'] == 'error':
        return _msj_error_helper(resp_prof['message'], cursor), 402
    if resp_prof['status'] == 'success' and resp_prof['data'] is None:
        return _msj_error_helper("Se intentó devolver un profesor pero no se encontró nada.", cursor), 403

    # Comprobar que la sala existe

    resp_sala = consultar_sala_por_id(id_sala, cursor)
    if resp_sala['status'] == 'error':
        return _msj_error_helper(resp_sala['message'], cursor), 404
    if resp_sala['status'] == 'success' and resp_sala['data'] is None:
        return _msj_error_helper("Se intentó devolver una sala pero no se encontró nada.", cursor), 405

    # Comprobar que la sala no esté ocupada en ese día y hora

    resp_clas = consultar_clase_por_sala_dia_hora(id_sala, dia, hora, cursor)
    if resp_clas['status'] == 'error':
        return _msj_error_helper(resp_clas['message'], cursor), 406
    if resp_clas['status'] == 'success' and resp_clas['data'] is not None:
        return _msj_error_helper("La sala ya se encuentra ocupada en ese día y hora.", cursor), 407

    # Comprobar que la sala escogida tenga la capacidad suficiente

    capacidad_sala = resp_sala["data"]["capacidad"]

    if (capacidad_sala < cupo_maximo):
        return _msj_error_helper("El cupo máximo ingresado supera la capacidad de la sala.", cursor), 408

    # Intentar insertar la clase

    resp_inser_clas = insertar_clase(estado, id_actividad, id_profesor, id_sala, dia, hora, cupo_maximo, cursor)

    if resp_inser_clas['status'] == 'error':
        return _msj_error_helper(resp_inser_clas['message'], cursor), 410
    if resp_inser_clas['status'] == 'success' and resp_inser_clas['data'] is None:
        return _msj_error_helper("Esa clase ya se encontraba insertada en el sistema.", cursor), 411

    # Intentar insertar una instancia para la clase
    ## TODO: Asegurarse de que la fecha utilizada para la instancia sea válida

    clase_id = resp_inser_clas["data"]
    resp_inser_inst_clase = insertar_instancia_clase(clase_id, generar_fecha_actual(), cursor)

    if resp_inser_inst_clase['status'] == 'error':
        return _msj_error_helper(resp_inser_inst_clase['message'], cursor), 412
    if resp_inser_inst_clase['status'] == 'success' and resp_inser_inst_clase['data'] is None:
        return _msj_error_helper("Esa instancia de clase ya se encontraba insertada en el sistema.", cursor), 413

    cursor.connection.commit()
    return _msj_exito_helper("Clase publicada exitosamente.", cursor, resp_inser_clas['data'])

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
    return _msj_exito_helper("Clase modificada exitosamente.", cursor)

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

    # Comprobar que exista la instancia de la clase
    res_ins = consultar_instancia_clase_por_id(id_ins_clase, cursor)
    if res_ins["status"] == 'error':
        return _msj_error_helper(res_ins['message'], cursor), 400
    if res_ins['status'] == 'success' and res_ins['data'] is None:
        return _msj_error_helper("Se intentó devolver la instancia de la clase pero no se encontró nada.", cursor), 401

    id_clase = res_ins["data"]["clase_id"]
    res_clase = consultar_clase_por_id(id_clase, cursor)
    dia = res_clase["data"]["dia"]
    hora = res_clase["data"]["hora"]

    # Comprobar si el usuario ya tenía reservas hechas de la misma instancia de clase
    res_reservas_inst_clase = obtener_reservas_usuario_inst_clase(id_ins_clase, id_usuario, cursor)
    if res_reservas_inst_clase["status"] == 'error':
        return _msj_error_helper(res_reservas_inst_clase['message'], cursor), 402
    if res_reservas_inst_clase["status"] == 'success' and res_reservas_inst_clase["data"] is not None:
        return _msj_error_helper("El usuario ya tenía una reserva hecha para esa misma clase en el mismo horario.", cursor), 403

    # Comprobar si el usuario ya tenía reservas hechas de otra clase para ese día a esa hora
    res_reservas_usu_dia_hora = obtener_reservas_usuario_dia_hora(id_usuario, dia, hora, cursor)
    if res_reservas_usu_dia_hora["status"] == 'error':
        return _msj_error_helper(res_reservas_usu_dia_hora['message'], cursor), 404
    if res_reservas_usu_dia_hora["status"] == 'success' and res_reservas_usu_dia_hora["data"] is not None:
        return _msj_error_helper("El usuario ya tenía una reserva hecha para otra clase en ese mismo día y hora.", cursor), 405

    # Comprobar que la instancia de la clase no tenga el cupo lleno
    cons_clase = consultar_clase_por_id(id_clase, cursor)
    cupo_clase = cons_clase["data"]["cupo_maximo"]
    tuplas_reservas_ic = obtener_reservas_instancia_clase(id_ins_clase, cursor)
    
    if (tuplas_reservas_ic["data"] is not None):
        cant_reservas = len(tuplas_reservas_ic["data"])
        if (cant_reservas >= cupo_clase):
            return _msj_error_helper("La clase ya se encuentra llena.", cursor), 406

    # Insertar reserva de clase 
    res_reserva = insertar_reserva(id_usuario, id_ins_clase, cursor)
    if res_reserva["status"] == 'error':
        return _msj_error_helper(res_reserva['message'], cursor), 407
    if res_reserva["status"] == 'success' and res_reserva["data"] is None:
        return _msj_error_helper("Ya se había creado una reserva para esa instancia de clase y ese usuario.", cursor), 408

    cursor.connection.commit()
    return _msj_exito_helper(f"Se reservó una clase para el usuario {id_usuario} con éxito.", cursor, res_reserva["data"])

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


def anotarse_lista_espera_service(id_clase, id_usuario):
    """Service que permite anotarse a la lista de espera de una clase"""
    
    cursor = conectarse_db()
    
    # verificar existencia de usuario
    res_usuario = consultar_usuario_por_id(id_usuario, cursor)
    
    if res_usuario["status"] == 'error':
        cursor.connection.close()
        return {
            "error": res_usuario['message']
        }, 500
    
    if res_usuario["status"] == 'success' and res_usuario["data"] is None:
        cursor.connection.close()
        return {
            "error": "No se encontró el usuario."
        }, 404
    
    esAbonado = verificar_usuario_abonado(cursor, id_usuario)
    
    if esAbonado:
        
        res = anotarse_lista_abonados(id_usuario, id_clase, cursor)
        
        if res["status"] == 'error':
            cursor.connection.close()
            return {
                "error": res['message']
            }, 500
            
        if res["status"] == 'success' and res["data"] is None:
            cursor.connection.close()
            return {
                "error": "No se pudo anotar a la lista de espera."
            }, 400
            
        tipo = "de abonados"
            
    else:
        
        res = anotarse_lista_publico_general(id_usuario, id_clase, cursor)
        
        if res["status"] == 'error':
            cursor.connection.close()
            return {
                "error": res['message']
            }, 500
            
        if res["status"] == 'success' and res["data"] is None:
            cursor.connection.close()
            return {
                "error": "No se pudo anotar a la lista de espera."
            }, 400
        
        tipo = "individual"
            
    cursor.connection.commit()
    cursor.connection.close()
    return {
        "message": f"Se anotó a la lista de espera {tipo} con éxito."
    }, 200
    
def registrar_asistencia_clase_service(id_clase, id_usuario):
    """Service que permite registrar la asistencia de un usuario a una clase"""
    cursor = conectarse_db()
    
    # verificar existencia de usuario
    res_usuario = consultar_usuario_por_id(id_usuario, cursor)
    
    if res_usuario["status"] == 'error':
        cursor.connection.close()
        return {
            "error": res_usuario['message']
        }, 500
        
    if res_usuario["status"] == 'success' and res_usuario["data"] is None:
        cursor.connection.close()
        return {
            "error": "No se encontró el usuario."
        }, 404
        
    # verificar existencia de clase
    res_clase = consultar_clase_por_id(id_clase, cursor)

    if res_clase["status"] == 'error':
        cursor.connection.close()
        return {
            "error": res_clase['message']
        }, 500
        
    if res_clase["status"] == 'success' and res_clase["data"] is None:
        cursor.connection.close()
        return {
            "error": "No se encontró la clase."
        }, 404
        
    # verificar que el usuario tenga una reserva a la clase
    res_reserva = consultar_reserva_por_usuario_clase(id_usuario, id_clase, cursor)

    if res_reserva["status"] == 'error':
        cursor.connection.close()
        return {
            "error": res_reserva['message']
        }, 500

    if res_reserva["status"] == 'success' and res_reserva["data"] is None:
        cursor.connection.close()
        return {
            "error": "El usuario no tiene una reserva para esta clase."
        }, 404
        
    # verificar que el usuario no tenga ya registrada la asistencia a la clase
    # peude que le den 2 veces para confirmar la asistencia
    res_asistencia = verificar_asistencia_usuario_clase(id_usuario, id_clase, cursor)
    
    if res_asistencia["status"] == 'error':
        cursor.connection.close()
        return {
            "error": res_asistencia['message']
        }, 500
    
    if res_asistencia["status"] == 'success' and res_asistencia["data"] is not None:
        cursor.connection.close()
        return {
            "error": "El usuario ya tiene registrada la asistencia a esta clase."
        }, 400    

    # Registrar asistencia
    res_asistencia = registrar_asistencia(id_usuario, id_clase, cursor)

    if res_asistencia["status"] == 'error':
        cursor.connection.close()
        return {
            "error": res_asistencia['message']
        }, 500

    cursor.connection.commit()
    cursor.connection.close()
    return {
        "message": "Asistencia registrada con éxito."
    }, 200