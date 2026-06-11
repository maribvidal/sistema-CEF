from datetime import datetime
from db.operaciones.usuarios.consultar_db import obtener_usuario_esta_en_instancia_clase
from db.operaciones.asistencias import verificar_asistencia_usuario_clase, registrar_asistencia
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.clases.consultar_db import listar_clases, consultar_clase_por_id, consultar_clase_por_sala_dia_hora
from db.operaciones.clases.insertar_db import insertar_clase
from db.operaciones.clases.modificar_db import modificar_clase_estado
from db.operaciones.actividades.consultar_db import consultar_actividad_por_id
from db.operaciones.profesores.consultar_db import consultar_profesor_por_id
from db.operaciones.salas.consultar_db import consultar_sala_por_id
from db.operaciones.reservas.insertar_db import insertar_reserva
from db.operaciones.reservas.consultar_db import obtener_reservas_usuario_dia_hora, obtener_reservas_usuario_inst_clase
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_id, verificar_usuario_abonado
from db.operaciones.instancias_clases.consultar_db import consultar_instancia_clase_por_id, obtener_reservas_instancia_clase
from db.operaciones.instancias_clases.insertar_db import insertar_instancia_clase
from db.operaciones.listas_espera import anotarse_lista_abonados, anotarse_lista_publico_general
from db.operaciones.reservas import consultar_reserva_por_usuario_clase
from db.operaciones.listas_espera import consultar_lista_espera_por_usuario_clase, borrar_lista_espera
from db.modulo_fechas import generar_fecha_actual, validar_fecha
from enums.dias import Dias

from services import _controlar_errores_query,_controlar_errores_query_sin_none, _msj_error_helper, _msj_exito_helper

def listar_clases_service():
    """Service que lista las clases"""

    cursor = conectarse_db()

    respuesta = listar_clases(cursor)
    control = _controlar_errores_query(respuesta, 400, "No se encontró ninguna clase en el sistema.", 401, cursor)
    if control is not None:
        return control

    return _msj_exito_helper("Se devolvió una lista de clases con éxito.", cursor, respuesta["data"])

def publicar_clase_service(
    estado: str,
    id_actividad: int,
    id_profesor: int,
    id_sala: int,
    dia: str,
    hora: str,
    cupo_maximo: int,
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

    # Intentar insertar la clase

    respuesta = insertar_clase(estado, id_actividad, id_profesor, id_sala, dia, hora, cupo_maximo, cursor)
    control = _controlar_errores_query(respuesta, 410, "Esa clase ya se encontraba insertada en el sistema.", 411, cursor)
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
                return _msj_error_helper("La fecha que se intentó utilizar no trascurre el día de la semana para la clase.", cursor), 412
        else:
            return _msj_error_helper("La fecha que se recibió no es válida o no cumple con el formato (YYY-mm-dd).", cursor), 413

    respuesta = insertar_instancia_clase(clase_id, fecha_actual, cursor)
    control = _controlar_errores_query(respuesta, 414, "No se pudo insertar la instancia de la clase.", 415, cursor)
    if control is not None:
        return control

    cursor.connection.commit()
    return _msj_exito_helper("Clase publicada exitosamente.", cursor, respuesta['data'])

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

    # Primero consultamos si la clase que queremos modificar, efectivamente existe en la base de datos

    respuesta = consultar_clase_por_id(clase_id, cursor)
    control = _controlar_errores_query(respuesta, 400, "Clase no encontrada.", 401, cursor)
    if control is not None:
        return control

    # Segundo verificamos que no haya ninguna instancia de la clase que queremos modificar, ya que como instancia_clase apunta directamente a Clase, pues todo cambio que hagamos en la clase repercute en la instancia de la misma

    respuesta = consultar_instancia_clase_por_id(clase_id, cursor)
    control = _controlar_errores_query_sin_none(respuesta, 402, "No se puede modificar la clase porque ya tiene una instancia asociada.", 403, cursor)
    if control is not None:
        return control

    # Tercero, intentamos modificar la clase

    respuesta = modificar_clase(clase_id, estado, id_actividad, id_profesor, sala, fecha, hora, cupo_maximo, cursor)

    if respuesta['status'] == 'error':
        return _msj_error_helper(respuesta["message"], cursor), 404
    
    cursor.connection.commit()
    return _msj_exito_helper("Clase modificada exitosamente.", cursor)

def eliminar_clase_service(clase_id: int):
    """Service que elimina una clase"""

    cursor = conectarse_db()

    # Primero vemos si existe ese id_clase en la TABLA Clases

    respuesta = consultar_clase_por_id(clase_id, cursor)
    control = _controlar_errores_query(respuesta, 400, "Clase no encontrada.", 401, cursor)
    if control is not None:
        return control

    # Despues nos aseguramos de que no exista ninguna instancia de la clase misma
    # y una instancia de la clase debería existir hasta que tenga reservas hechas

    respuesta = consultar_instancia_clase_por_id(clase_id, cursor)
    _controlar_errores_query_sin_none(respuesta, 402, "No se puede eliminar la clase porque ya tiene una instancia asociada.", 403, cursor)
    if control is not None:
        return control

    # Y si todo eso se cumple, entonces eliminamos la clase.

    respuesta = borrar_clase(clase_id, cursor)

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

    # Comprobar si la instancia de la clase existe

    respuesta = consultar_instancia_clase_por_id(id_ins_clase, cursor)
    control = _controlar_errores_query(respuesta, 400, "Instancia de clase no encontrada.", 401, cursor)
    if control is not None:
        return control

    # Comprobar si el usuario está inscripto en dicha instancia

    respuesta = obtener_usuario_esta_en_instancia_clase(id_ins_clase, id_usuario, cursor)
    control = _controlar_errores_query(respuesta, 402, "El usuario no se encuentra inscripto en la clase.", 403, cursor)
    if control is not None:
        return control

    return _msj_exito_helper("El usuario se encuentra inscripto.", cursor)

def anotarse_lista_espera_service(id_clase, id_usuario):
    """Service que permite anotarse a la lista de espera de una clase"""
    
    cursor = conectarse_db()
    
    # verificar existencia de usuario

    respuesta = consultar_usuario_por_id(id_usuario, cursor)
    _controlar_errores_query(respuesta, 400, "No se encontró el usuario.", 401, cursor)
    
    # verificar si el usuario abonó

    esAbonado = verificar_usuario_abonado(cursor, id_usuario)
    tipo = None
    
    if esAbonado:
        respuesta = anotarse_lista_abonados(id_usuario, id_clase, cursor)
        _controlar_errores_query(respuesta, 402, "No se pudo anotar a la lista de espera.", 403, cursor)
        tipo = "de abonados"
    else:
        respuesta = anotarse_lista_publico_general(id_usuario, id_clase, cursor)
        _controlar_errores_query(respuesta, 404, "No se pudo anotar a la lista de espera.", 405, cursor)
        tipo = "individual"
            
    cursor.connection.commit()
    return _msj_exito_helper(f"Se anotó a la lista de espera {tipo} con éxito.", cursor)
    
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

    # verificar que el usuario este en una lista de espera a la clase

    respuesta = consultar_lista_espera_por_usuario_clase(id_usuario, id_clase, cursor)
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

    # verificar que el usuario este en una lista de espera a la clase

    respuesta = consultar_lista_espera_por_usuario_clase(id_usuario, id_clase, cursor)
    control = _controlar_errores_query(respuesta, 404, "El usuario no tiene una inscripción en la lista de espera para esta clase.", 405, cursor)
    if control is not None:
        return control

    # Rechazar asistencia
    # esto pensarlo bien, por el momento lo que voy a hacer es borrarlo de la lista de espera y avisar al siguiente de la lista.
    
    respuesta = borrar_lista_espera(id_usuario, id_clase, cursor)
    if respuesta["status"] == 'error':
        cursor.connection.close()
        return {
            "error": respuesta['message']
        }, 500
        
    # avisar_siguiente_lista_espera(id_clase, cursor) <---- mirar como van a hacer en la cancelacion de reserva para avisar a los de las listas y en lo posible esa parte modularizarlo
        
    cursor.connection.commit()
    return _msj_exito_helper("Asistencia rechazada con éxito.", cursor)
