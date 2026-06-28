from datetime import datetime
from db.operaciones.listas_espera.consultar_db import consultar_lista_espera_individual, consultar_lista_espera_abonado
from db.operaciones.usuarios.consultar_db import obtener_usuario_esta_en_instancia_clase
from db.operaciones.asistencias import verificar_asistencia_usuario_clase, registrar_asistencia
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.clases.consultar_db import listar_clases, consultar_clase_por_id, consultar_clase_por_sala_dia_hora, consultar_instancias_por_clase_id, consultar_reservas_total_por_clase
from db.operaciones.clases.insertar_db import insertar_clase
from db.operaciones.clases import modificar_clase_estado, modificar_clase, borrar_clase
from db.operaciones.actividades.consultar_db import consultar_actividad_por_id
from db.operaciones.profesores.consultar_db import consultar_profesor_por_id, consultar_clases_profesor_dia_hora
from db.operaciones.salas.consultar_db import consultar_sala_profe_por_dia_hora, consultar_sala_por_id
from db.operaciones.reservas.insertar_db import insertar_reserva
from db.operaciones.reservas.consultar_db import obtener_reservas_usuario_dia_hora, obtener_reservas_usuario_inst_clase
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_id, verificar_usuario_abonado
from db.operaciones.instancias_clases.consultar_db import consultar_instancia_clase_por_id, obtener_reservas_instancia_clase, listar_instancias_clases_semana, obtener_instancia_clase_por_clase_id_semana
from db.operaciones.instancias_clases import insertar_instancia_clase
from db.operaciones.reservas import consultar_reserva_por_usuario_clase
from db.operaciones.listas_espera.insertar_db import insertar_lista_espera_abonados, insertar_lista_espera_individual
from utils.modulo_fechas import generar_fecha_actual, validar_fecha, validar_dia_fecha
from enums.dias import Dias
from db.operaciones.profesores.consultar_db import verificar_actividad_profesor

from services import _controlar_errores_query,_controlar_errores_query_sin_none, _msj_error_helper, _msj_exito_helper

def listar_clases_service():
    """Service que lista las clases"""

    cursor = conectarse_db()

    respuesta = listar_clases(cursor)
    control = _controlar_errores_query(respuesta, 400, "No se encontró ninguna clase en el sistema.", 401, cursor)
    if control is not None:
        return control

    return _msj_exito_helper("Se devolvió una lista de clases con éxito.", cursor, respuesta["data"])

def listar_instancias_clases_semana_service():
    """Service que lista las instancias de la clase de la semana"""

    cursor = conectarse_db()

    respuesta = listar_instancias_clases_semana(cursor)
    control = _controlar_errores_query(respuesta, 400, "No se encontró ninguna instancia de clase en el sistema.", 401, cursor)
    if control is not None:
        return control

    return _msj_exito_helper("Se devolvió una lista de instancias de clase con éxito.", cursor, respuesta["data"])

def publicar_clase_service(
    estado: str,
    id_actividad: int,
    id_profesor: int,
    id_sala: int,
    dia: str,
    hora: str,
    cupo_maximo: int,
    monto: float,
    primera_fecha = None
):
    """Service que publica una clase"""

    cursor = conectarse_db()

    # Comprobar que la actividad existe

    respuesta = consultar_actividad_por_id(id_actividad, cursor)
    control = _controlar_errores_query(respuesta, 400, "Se intentó devolver una actividad pero no se encontró nada.", 401, cursor)
    if control is not None:
        return control

    # Comprobar que el profesor existe

    respuesta = consultar_profesor_por_id(id_profesor, cursor)
    control = _controlar_errores_query(respuesta, 402, "Se intentó devolver un profesor pero no se encontró nada.", 403, cursor)
    if control is not None:
        return control

    # Como existe, entonces analicemos qué actividades puede realizar y compararlas con las actividades que puede realizar el profesor, para ver si efectivamente el profesor puede dar la clase de la actividad que se quiere publicar.
    res_habilitado = verificar_actividad_profesor(id_profesor, id_actividad, cursor)
    if res_habilitado['status'] == 'error':
        return _msj_error_helper("Error interno al verificar las actividades del profesor.", cursor), 500
    if not res_habilitado['data']:
        return _msj_error_helper("El profesor no está habilitado para dar esa actividad.", cursor), 400 # 400: Bad Request

    # Comprobar que la sala existe

    respuesta = consultar_sala_por_id(id_sala, cursor)
    control = _controlar_errores_query(respuesta, 404, "Se intentó devolver una sala pero no se encontró nada.", 405, cursor)
    if control is not None:
        return control

    # Comprobar que la sala no esté ocupada en ese día y hora

    respuesta = consultar_clase_por_sala_dia_hora(id_sala, dia, hora, cursor)
    control = _controlar_errores_query_sin_none(respuesta, 406, "La sala ya se encuentra ocupada en ese día y hora.", 407, cursor)
    if control is not None:
        return control

    # Comprobar que la sala escogida tenga la capacidad suficiente

    respuesta = consultar_sala_por_id(id_sala, cursor)
    capacidad_sala = int(respuesta["data"]['capacidad'])

    if (capacidad_sala < cupo_maximo):
        return _msj_error_helper("El cupo máximo ingresado supera la capacidad de la sala.", cursor), 408
    
    # Comprobar que el profesor no se encuentre ocupado en ese día y hora

    respuesta = consultar_clases_profesor_dia_hora(id_profesor, dia, hora, cursor)
    control = _controlar_errores_query_sin_none(respuesta, 410, "El profesor ya se encuentra ocupado en ese día y hora.", 411, cursor)
    if control is not None:
        return control

    # Intentar insertar la clase

    respuesta = insertar_clase(estado, id_actividad, id_profesor, id_sala, dia, hora, cupo_maximo, monto, cursor)
    control = _controlar_errores_query(respuesta, 412, "Esa clase ya se encontraba insertada en el sistema.", 413, cursor)
    if control is not None:
        return control

    # Ver si se recibió una fecha, y si se recibió, ver si es válida

    clase_id = int(respuesta["data"])
    fecha_actual = generar_fecha_actual(dia)

    if (primera_fecha is not None):
        res_validar_fecha = validar_fecha(primera_fecha)
        if (res_validar_fecha):
            res_validar_dia = validar_dia_fecha(primera_fecha, dia)
            if (res_validar_dia):
                fecha_actual = primera_fecha
            else:
                return _msj_error_helper("La fecha que se intentó utilizar no trascurre el día de la semana para la clase.", cursor), 414
        else:
            return _msj_error_helper("La fecha que se recibió no es válida o no cumple con el formato (YYY-mm-dd).", cursor), 415

    # Insertar instancia de clase e listas de esperas

    respuesta = insertar_lista_espera_abonados(clase_id, cursor)
    control = _controlar_errores_query(respuesta, 414, "No se pudo insertar la lista de espera de abonados.", 416, cursor)
    if control is not None:
        return control

    respuesta = insertar_instancia_clase(clase_id, fecha_actual, monto, cursor)
    control = _controlar_errores_query(respuesta, 416, "No se pudo insertar la instancia de la clase.", 417, cursor)
    if control is not None:
        return control
    id_ins_clase = respuesta["data"]

    if not isinstance(id_ins_clase, int):
        cursor.connection.close()
        return _msj_error_helper("No se pudo obtener un id válido para la instancia de la clase.", cursor), 418

    respuesta = insertar_lista_espera_individual(id_ins_clase, cursor)
    control = _controlar_errores_query(respuesta, 419, "No se pudo insertar la lista de espera individual para la instancia de la clase recien creada.", 420, cursor)
    if control is not None:
        return control

    cursor.connection.commit()
    return _msj_exito_helper("Clase publicada exitosamente.", cursor, respuesta['data'])

def modificar_clase_service(
    clase_id: int,
    estado: str,
    id_profesor: int,
    sala: int,
):
    """Service que modifica una clase"""
    cursor = conectarse_db()

    # Primero consultamos si la clase que queremos modificar, efectivamente existe en la base de datos

    respuesta = consultar_clase_por_id(clase_id, cursor)
    control = _controlar_errores_query(respuesta, 400, "Clase no encontrada.", 401, cursor)
    if control is not None:
        return control
    
    # Como la clase existe, extraemos su actividad actual y otros datos
    id_actividad_actual = respuesta['data']['actividad_id']
    dia_clase = respuesta['data']['dia']
    hora_clase = respuesta['data']['hora']
    id_profe_orig = respuesta['data']['profesor_id']
    cupo_maximo = respuesta['data']['cupo_maximo']

    # Ahora realizamos una validación nueva: Verificar si el profesor puede dar la actividad fija de esta clase
    res_habilitado = verificar_actividad_profesor(id_profesor, id_actividad_actual, cursor)
    if res_habilitado['status'] == 'error':
        return _msj_error_helper("Error interno al verificar las actividades del profesor.", cursor), 500
    if not res_habilitado['data']:
        return _msj_error_helper("El profesor no está habilitado para dar esa actividad.", cursor), 412 # 400: Bad Request

    # Comprobar que la sala no está ocupada ya para ese día y hora por ese profe
    respuesta = consultar_sala_profe_por_dia_hora(dia_clase, hora_clase, cursor)
    if respuesta['status'] == 'error':
        cursor.connection.close()
        return _msj_error_helper(respuesta["message"], cursor), 406
    if respuesta['status'] == 'success' and respuesta['data'] is not None:
        salas = [sal for sal in respuesta["data"] if sal["id"] == sala and sal["profesor_id"] != id_profe_orig]
        print(salas)
        if len(salas) > 0:
            cursor.connection.close()
            return _msj_error_helper("La sala ya se encuentra ocupada en ese día y hora.", cursor), 405

    # Comprobar que la sala cuente con capacidad suficiente
    respuesta = consultar_sala_por_id(sala, cursor)
    capacidad_sala = int(respuesta["data"]['capacidad'])
    if (cupo_maximo > capacidad_sala):
        return _msj_error_helper("El cupo máximo ingresado supera la capacidad de la sala.", cursor), 408

    # Comprobar que el profesor no se encuentre ocupado en ese día y hora
    respuesta = consultar_clases_profesor_dia_hora(id_profesor, dia_clase, hora_clase, cursor)
    if respuesta['status'] == 'error':
        cursor.connection.close()
        return _msj_error_helper(respuesta["message"], cursor), 410
    if respuesta['status'] == 'success' and respuesta['data'] is not None:
        clases = [clase for clase in respuesta["data"] if clase["id"] != clase_id]
        if len(clases) > 0:
            cursor.connection.close()
            return _msj_error_helper("El profesor ya se encuentra ocupado en ese día y hora.", cursor), 411

    respuesta = consultar_reservas_total_por_clase(clase_id, cursor)
    if respuesta['status'] == 'error':
        cursor.connection.close()
        return _msj_error_helper(respuesta["message"], cursor), 402
    if respuesta['status'] == 'success' and respuesta['data']['id'] is not None:
        cursor.connection.close()
        return _msj_error_helper("No se puede actualizar la clase porque existen reservas asociadas.", cursor), 403

    # Tercero, intentamos modificar la clase
    respuesta = modificar_clase(clase_id, estado, id_profesor, sala, cursor)

    if respuesta['status'] == 'error':
        return _msj_error_helper(respuesta["message"], cursor), 404
    
    cursor.connection.commit()
    return _msj_exito_helper("Clase modificada exitosamente.", cursor)

def eliminar_clase_service(clase_id: int):
    """Service que elimina una clase"""

    cursor = conectarse_db()

    # vemos si existe ese id_clase en la TABLA Clases
    respuesta = consultar_clase_por_id(clase_id, cursor)
    
    # usamos _controlar_errores_query normal con sus códigos 400/401
    control = _controlar_errores_query(respuesta, 400, "Clase no encontrada.", 401, cursor)
    if control is not None:
        return control

    # nos aseguramos de que no exista ninguna reserva
    respuesta = consultar_reservas_total_por_clase(clase_id, cursor)
    
    # Le agregamos "control =" y mantenemos el _sin_none con 402/403
    if respuesta['status'] == 'error':
        cursor.connection.close()
        return _msj_error_helper(respuesta["message"], cursor), 402
    if respuesta['status'] == 'success' and respuesta['data']['id'] is not None:
        cursor.connection.close()
        return _msj_error_helper("No se pudo eliminar la clase porque existían reservas asociadas.", cursor), 403

    # si todo eso se cumple, entonces eliminamos la clase.
    respuesta = borrar_clase(clase_id, cursor)
    print(respuesta)

    if respuesta['status'] == 'error':
        return _msj_error_helper(respuesta["message"], cursor), 404

    cursor.connection.commit()
    return _msj_exito_helper("Clase eliminada exitosamente.", cursor)

def cancelar_clase_service(clase_id: int):
    """Service que cancela una clase"""

    cursor = conectarse_db()

    # Primero nos fijamos que la clase que queremos cancelar, efectivamente existe en la base de datos.
    
    respuesta = consultar_clase_por_id(clase_id, cursor)
    control = _controlar_errores_query(respuesta, 400, "Clase no encontrada.", 401, cursor)
    if control is not None:
        return control

    # Segundo: Verificamos que no exista ninguna instancia de la misma. Porque si cancelamos la clase y se encuentra instanciada, aunque no hayan reservas, puede haber una condición de carrera o una infima posibilidad de que al último momento alguien reserve
    # PD: si no les gusta esa implementación, entonces implementen una segunda verificacion la cual verifique que no posee ninguna reserva dicha instancia

    respuesta = consultar_instancia_clase_por_id(clase_id, cursor)
    control = _controlar_errores_query(respuesta, 402, "No se puede cancelar la clase porque ya tiene una instancia asociada.", 403, cursor)
    if control is not None:
        return control

    # Tercero: Modificamos el estado de la clase a Cancelada.

    respuesta = modificar_clase_estado(clase_id, 'Cancelada', cursor)

    if respuesta['status'] == 'error':
        return _msj_error_helper(respuesta["message"], cursor), 404

    cursor.connection.commit()
    return _msj_exito_helper("Clase cancelada exitosamente.", cursor)

def reservar_clase_service(id_ins_clase: int, id_usuario: int):
    """Service que, dado un usuario, lo intenta inscribir
        en una clase con una fecha y hora dada."""

    cursor = conectarse_db()

    # Comprobar que exista la instancia de la clase

    respuesta = consultar_instancia_clase_por_id(id_ins_clase, cursor)
    control = _controlar_errores_query(respuesta, 400, "Se intentó devolver la instancia de la clase pero no se encontró nada.", 401, cursor)
    if control is not None:
        return control

    id_clase = respuesta["data"]["clase_id"]
    res_clase = consultar_clase_por_id(id_clase, cursor)
    dia = res_clase["data"]["dia"]
    hora = res_clase["data"]["hora"]

    # Comprobar si el usuario ya tenía reservas hechas de la misma instancia de clase

    respuesta = obtener_reservas_usuario_inst_clase(id_ins_clase, id_usuario, cursor)
    control = _controlar_errores_query_sin_none(respuesta, 402, "El usuario ya tenía una reserva hecha para esa misma clase en el mismo horario.", 403, cursor)
    if control is not None:
        return control

    # Comprobar si el usuario ya tenía reservas hechas de otra clase para ese día a esa hora

    respuesta = obtener_reservas_usuario_dia_hora(id_usuario, dia, hora, cursor)
    control = _controlar_errores_query_sin_none(respuesta, 404, "El usuario ya tenía una reserva hecha para otra clase en ese mismo día y hora.", 405, cursor)
    if control is not None:
        return control

    # Comprobar que la instancia de la clase no tenga el cupo lleno

    cons_clase = consultar_clase_por_id(id_clase, cursor)
    cupo_clase = cons_clase["data"]["cupo_maximo"]
    tuplas_reservas_ic = obtener_reservas_instancia_clase(id_ins_clase, cursor)

    print(cupo_clase, tuplas_reservas_ic)
    
    if (tuplas_reservas_ic["data"] is not None):
        cant_reservas = len(tuplas_reservas_ic["data"])
        if (cant_reservas >= cupo_clase):
            return _msj_error_helper("La clase ya se encuentra llena.", cursor), 406

    # Insertar reserva de clase

    respuesta = insertar_reserva(id_usuario, id_ins_clase, cursor)
    control = _controlar_errores_query(respuesta, 407, "Ya se había creado una reserva para esa instancia de clase y ese usuario.", 408, cursor)
    if control is not None:
        return control

    cursor.connection.commit()
    return _msj_exito_helper(f"Se reservó una clase para el usuario {id_usuario} con éxito.", cursor, respuesta["data"])

def verificar_inscripcion_usuario_clase_service(id_ins_clase, id_usuario):
    """Service que devuelve si un usuario se encuentra
        inscripto o no en una clase a una fecha y hora dada."""

    cursor = conectarse_db()

    # Comprobar si el usuario existe

    respuesta = consultar_usuario_por_id(id_usuario, cursor)
    control = _controlar_errores_query(respuesta, 400, "Usuario no encontrado.", 401, cursor)
    if control is not None:
        return control

    # Comprobar si la instancia de la clase existe

    respuesta = consultar_instancia_clase_por_id(id_ins_clase, cursor)
    control = _controlar_errores_query(respuesta, 402, "Instancia de clase no encontrada.", 403, cursor)
    if control is not None:
        return control

    # Comprobar si el usuario está inscripto en dicha instancia

    respuesta = obtener_usuario_esta_en_instancia_clase(id_ins_clase, id_usuario, cursor)
    control = _controlar_errores_query(respuesta, 404, "El usuario no se encuentra inscripto en la clase.", 405, cursor)
    if control is not None:
        return control

    return _msj_exito_helper("El usuario se encuentra inscripto.", cursor)

def anotarse_lista_espera_service(id_clase, id_usuario):
    """Service que permite anotarse a la lista de espera de una clase"""
    
    cursor = conectarse_db()
    
    # verificar existencia de usuario
    respuesta = consultar_usuario_por_id(id_usuario, cursor)
    control = _controlar_errores_query(respuesta, 400, "No se encontró el usuario.", 401, cursor)
    if control is not None:
        return control
    
    # verificar si el usuario abonó

    # REWORK
            
    cursor.connection.commit()
    return _msj_exito_helper("Se anotó a la lista de espera con éxito.", cursor)
    
def registrar_asistencia_clase_service(id_clase, id_usuario):
    """Service que permite registrar la asistencia de un usuario a una clase"""
    cursor = conectarse_db()
    
    # verificar existencia de usuario
    respuesta = consultar_usuario_por_id(id_usuario, cursor)
    control = _controlar_errores_query(respuesta, 400, "No se encontró el usuario.", 401, cursor)
    if control is not None:
        return control

    # verificar existencia de clase
    respuesta = consultar_clase_por_id(id_clase, cursor)
    control = _controlar_errores_query(respuesta, 402, "No se encontró la clase.", 403, cursor)
    if control is not None:
        return control

    """
    # verificar que el usuario este en una lista de espera a la clase

    # validar que el usuario este en una lista de espera correspondiente
    if es_abonado:
        respuesta = consultar_lista_espera_abonado(id_usuario, id_clase, cursor)
    else:
        respuesta = consultar_lista_espera_individual(id_usuario, id_clase, cursor)
        
    control = _controlar_errores_query(respuesta, 404, "El usuario no tiene una inscripción en la lista de espera para esta clase.", 405, cursor)
    if control is not None:
        return control

    # verificar que el usuario no tenga ya registrada la asistencia a la clase
    # puede que le den 2 veces para confirmar la asistencia

    respuesta = verificar_asistencia_usuario_clase(id_usuario, id_clase, cursor)
    control = _controlar_errores_query_sin_none(respuesta, 406, "El usuario ya tiene registrada la asistencia a esta clase.", 407, cursor)
    if control is not None:
        return control

    # Registrar asistencia

    respuesta = registrar_asistencia(id_usuario, id_clase, cursor)
    if respuesta["status"] == 'error':
        _msj_error_helper(respuesta['message'], cursor), 408
    """

    cursor.connection.commit()
    return _msj_exito_helper("Asistencia registrada con éxito.", cursor)

def rechazar_asistencia_clase_service(id_clase, id_usuario):
    """Service que permite rechazar la asistencia de un usuario a una clase"""
    cursor = conectarse_db()
    
    # verificar existencia de usuario

    respuesta = consultar_usuario_por_id(id_usuario, cursor)
    control = _controlar_errores_query(respuesta, 400, "No se encontró el usuario.", 401, cursor)
    if control is not None:
        return control

    # verificar existencia de clase

    respuesta = consultar_clase_por_id(id_clase, cursor)
    control = _controlar_errores_query(respuesta, 402, "No se encontró la clase.", 403, cursor)
    if control is not None:
        return control

    """
    # verificar que el usuario este en una lista de espera a la clase

    # validar que el usuario este en una lista de espera correspondiente
    if es_abonado:
        respuesta = consultar_lista_espera_abonado(id_usuario, id_clase, cursor)
    else:
        respuesta = consultar_lista_espera_individual(id_usuario, id_clase, cursor)
        
    control = _controlar_errores_query(respuesta, 404, "El usuario no tiene una inscripción en la lista de espera para esta clase.", 405, cursor)
    if control is not None:
        return control

    # Rechazar asistencia
    # esto pensarlo bien, por el momento lo que voy a hacer es borrarlo de la lista de espera.
    respuesta = borrar_lista_espera(id_usuario, id_clase, cursor)
    if respuesta["status"] == 'error':
        cursor.connection.close()
        return {
            "error": respuesta['message']
        }, 500
    """
    
    cursor.connection.commit()
    return _msj_exito_helper("Asistencia rechazada con éxito.", cursor)

def obtener_instancias_clases_service(id_clase):
    """Service que permite obtener las instancias de una clase"""
    cursor = conectarse_db()

    # Controlar que exista la clase

    respuesta = consultar_clase_por_id(id_clase, cursor)
    control = _controlar_errores_query(respuesta, 400, "No se encontró la clase.", 401, cursor)
    if control is not None:
        return control

    # Obtener instancias

    respuesta = consultar_instancias_por_clase_id(id_clase, cursor)
    control = _controlar_errores_query(respuesta, 402, "No se encontraron instancias para dicha clase.", 403, cursor)
    if control is not None:
        return control

    return _msj_exito_helper("Instancias obtenidas exitosamente.", cursor, respuesta["data"])
    
def obtener_instancia_clases_semana_clase_id_service(id_clase):
    """Service que permite obtener la instancia de la clase para la semana."""
    cursor = conectarse_db()

    # Controlar que exista la clase

    respuesta = consultar_clase_por_id(id_clase, cursor)
    control = _controlar_errores_query(respuesta, 400, "No se encontró la clase.", 401, cursor)
    if control is not None:
        return control
    
    # Obtener la instancia

    respuesta = obtener_instancia_clase_por_clase_id_semana(id_clase, cursor)
    control = _controlar_errores_query(respuesta, 402, "No se encontró una instancia para la clase en esta semana.", 403, cursor)
    if control is not None:
        return control
    
    print(respuesta)
    
    return _msj_exito_helper("Instancia obtenida exitosamente.", cursor, respuesta["data"])
