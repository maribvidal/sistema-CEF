from db.operaciones.reservas.insertar_db import insertar_reserva
from db.operaciones.instancias_clases.consultar_db import consultar_instancia_clase_por_id
from db.operaciones.listas_espera.consultar_db import consultar_lista_espera_abonado, consultar_lista_espera_individual
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_id, verificar_usuario_abonado
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.reservas.consultar_db import consultar_reserva_por_id
from db.operaciones.cancelaciones.insertar_db import insertar_cancelacion
from db.operaciones.reservas import borrar_reserva
from db.operaciones.clases.consultar_db import consultar_instancias_por_clase_id

from utils.modulo_manejo_listas import manejar_listas_de_espera_por_clase
from services import _controlar_errores_query,_controlar_errores_query_sin_none, _msj_error_helper, _msj_exito_helper

def cancelar_reserva_service(reserva_id):
    """Service que permite cancelar la reserva de un usuario."""

    cursor = conectarse_db()

    # Validar si la reserva existe

    respuesta = consultar_reserva_por_id(reserva_id, cursor)
    control = _controlar_errores_query(respuesta, 400, "La reserva con dicho id no existe.", 401, cursor)
    if control is not None:
        return control

    # Cancelar reserva (insertar una cancelación)
    res_elim_reserva = borrar_reserva(reserva_id, cursor)
    id_usuario = res_reserva["data"]["usuario_id"]
    id_ins_clase = res_reserva["data"]["inst_clase_id"]
    res_ins_cancelacion = insertar_cancelacion(id_usuario, id_ins_clase, cursor)
    if res_ins_cancelacion['status'] == 'error':
        return _msj_error_helper(res_ins_cancelacion['message'], cursor), 402
    
    cursor.connection.commit()

    # res_ins_clase = consultar_instancia_clase_por_id(id_ins_clase, cursor)
    # id_clase = res_ins_clase["data"]["clase_id"]
    # manejar_listas_de_espera_por_clase(id_clase, cursor)
    
    return _msj_exito_helper(f"Cancelación para la reserva con id {reserva_id} creada exitosamente.", cursor)

def crear_reserva_individual_service(usuario_id: int, inst_clase_id: int):
    """Service que permite crear una reserva individual."""

    cursor = conectarse_db()

    # CONSULTAR: ¿Valido si el usuario y la instancia de la clase existen?

    # Intentar crear la reserva

    respuesta = insertar_reserva(usuario_id, inst_clase_id, cursor)
    control = _controlar_errores_query(respuesta, 400, "La reserva ya había sido creada.", 401, cursor)
    if control is not None:
        return control

    cursor.connection.commit()

    return _msj_exito_helper(f"La reserva {respuesta["data"]} ha sido creada exitosamente.", cursor)

def crear_reserva_abonado_service(usuario_id: int, clase_id: int):
    """Service que permite crearle una reserva para todas las instancias
        existentes de una clase a un abonado."""

    cursor = conectarse_db()

    # CONSULTAR: ¿Valido si el usuario y la instancia de la clase existen?

    # Obtener las instancias de las clases

    respuesta = consultar_instancias_por_clase_id(clase_id, cursor)
    control = _controlar_errores_query(respuesta, 400, "La consulta por las instancias de la clase falló.", 401, cursor)
    if control is not None:
        return control
    
    instancias = respuesta["data"]
    print(instancias)

    # Intentar crear las reservas

    for instancia in instancias:
        respuesta = insertar_reserva(usuario_id, instancia["inst_clase_id"], cursor)
        control = _controlar_errores_query(respuesta, 402, "La reserva ya había sido creada.", 403, cursor)
        if control is not None:
            return control

    cursor.connection.commit()

    return _msj_exito_helper(f"La reservas para el usuario abonado {usuario_id} han sido creadas exitosamente.", cursor)
