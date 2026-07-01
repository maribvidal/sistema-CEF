from services.pagos_service import crear_pago_service_particular
from db.operaciones.usuario_pertenece_lista_espera_individual.insertar_db import insertar_usuario_pertenece_lista_espera_individual
from db.operaciones.listas_espera.insertar_db import insertar_lista_espera_abonados, insertar_lista_espera_individual
from db.operaciones.usuario_pertenece_lista_espera_abonados.insertar_db import insertar_usuario_pertenece_lista_espera_abonados
from db.operaciones.mensualidades.consultar_db import verificar_disponibilidad_usuario
from db.operaciones.reservas.insertar_db import insertar_reserva
from db.operaciones.instancias_clases.consultar_db import consultar_instancia_clase_por_id
from db.operaciones.listas_espera.consultar_db import consultar_lista_espera_abonado, consultar_lista_espera_individual
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_id, verificar_usuario_abonado
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.reservas.consultar_db import consultar_reserva_por_id
from db.operaciones.cancelaciones.insertar_db import insertar_cancelacion
from db.operaciones.reservas import borrar_reserva
from db.operaciones.clases.consultar_db import consultar_cupo_disponible_por_clase, consultar_instancias_por_clase_id, consultar_instancias_por_id, obtener_cantidad_reservar_instancia_clase
from db.operaciones import consultar_usuario_por_dni, consultar_clase_por_id, consultar_lista_espera_abonado_usuario_por_idClase, consultar_lista_espera_individual_usuario_por_idInstanciaClase,  obtener_lista_espera_abonados_por_id_clase, obtener_lista_espera_individual_por_id_clase

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
    id_usuario = res_elim_reserva["data"]["usuario_id"]
    id_ins_clase = res_elim_reserva["data"]["inst_clase_id"]
    res_ins_cancelacion = insertar_cancelacion(id_usuario, id_ins_clase, cursor)
    if res_ins_cancelacion['status'] == 'error':
        return _msj_error_helper(res_ins_cancelacion['message'], cursor), 402
    
    cursor.connection.commit()

    # notificar siguiente en la lista de espera
    res_ins_clase = consultar_instancia_clase_por_id(id_ins_clase, cursor)
    id_clase = res_ins_clase["data"]["clase_id"]
    manejar_listas_de_espera_por_clase(id_clase, cursor)
    
    return _msj_exito_helper(f"Cancelación para la reserva con id {reserva_id} creada exitosamente.", cursor)

def crear_reserva_individual_service(usuario_id: int, inst_clase_id: int):
    """Service que permite crear una reserva individual."""

    cursor = conectarse_db()

    # Comprobar si el usuario existe
    usuario = consultar_usuario_por_id(usuario_id, cursor)
    control = _controlar_errores_query(usuario, 400, "Usuario no encontrado.", 401, cursor)
    if control is not None:
        return control
    
    # Comprobar si la instancia de clase existe
    inst_clase = consultar_instancias_por_id(inst_clase_id, cursor)
    control = _controlar_errores_query(inst_clase, 400, "Instancia de clase no encontrada.", 401, cursor)
    if control is not None:
        return control

    # Verificar si la instancia de clase tiene cupo disponible:
    # 1- obtener la cantidad de cupo disponible de la clase
    cupo_disponible = consultar_cupo_disponible_por_clase(inst_clase['data']['clase_id'], cursor)
    
    # 2- obtener la cantidad de reservas existentes para la instancia de clase
    reservas_existentes = obtener_cantidad_reservar_instancia_clase(inst_clase_id, cursor)
    
    # 3- comparar la cantidad de reservas existentes con la cantidad de cupo disponible
    if reservas_existentes['data']['cantidad_reservas'] >= cupo_disponible['data']['cupo_maximo']:
        # en front tienen que mostrar el pop up parecido al del pagar mensualidad y luego si apreta que si, mandar a la ruta de agregar lista de espera
        return _msj_error_helper("No hay cupo disponible para esta instancia de clase.", cursor), 409

    # Pagar
    respuesta, status = crear_pago_service_particular(usuario_id, "Reserva individual", inst_clase_id)
    if status != 200:
        return respuesta, status

    # Intentar crear la reserva
    respuesta = insertar_reserva(usuario_id, inst_clase_id, cursor)
    control = _controlar_errores_query(respuesta, 400, "La reserva ya había sido creada.", 401, cursor)
    if control is not None:
        return control

    respuesta = insertar_usuario_pertenece_lista_espera_individual(usuario_id, inst_clase_id, cursor)
    control = _controlar_errores_query(respuesta, 400, "Error al agregar usuario a la lista de espera individual.", 401, cursor)
    if control is not None:
        return control
    
    cursor.connection.commit()

    return _msj_exito_helper(f"La reserva {respuesta["data"]} ha sido creada exitosamente.", cursor)

def agregar_usuario_a_lista_espera_individual(usuario_id, inst_clase_id):
    """Agrega un usuario a la lista de espera individual para una instancia de clase específica."""
    cursor = conectarse_db()
    
    # Comprobar si el usuario existe
    usuario = consultar_usuario_por_id(usuario_id, cursor)
    control = _controlar_errores_query(usuario, 400, "Usuario no encontrado.", 401, cursor)
    if control is not None:
        return control
    
    # verificar que la clase existe
    respuesta  = consultar_instancia_clase_por_id(inst_clase_id, cursor)
    control = _controlar_errores_query(respuesta, 400, "Clase no encontrada.", 401, cursor)
    if control is not None:
        return control

    # verificar si el usuario ya está en la lista de espera
    respuesta = consultar_lista_espera_individual_usuario_por_idInstanciaClase(inst_clase_id, usuario['data']['dni'], cursor)
    control = _controlar_errores_query_sin_none(respuesta, 400, "Usuario ya está en la lista de espera.", 401, cursor)
    if control is not None:
        return control
    
    # verificar si existe una lista de espera para la instancia de clase
    respuesta = obtener_lista_espera_individual_por_id_clase(inst_clase_id, cursor)
    if respuesta['status'] == "error":
        return {
            "status": "error",
            "message": "Error al consultar la lista de espera."
        },500
    
    # Si no existe, crear una nueva lista de espera para la instancia de clase    
    if respuesta['data'] is None:
        respuesta = insertar_lista_espera_individual(inst_clase_id, cursor)
        control = _controlar_errores_query(respuesta, 500, "Error al crear la lista de espera.", 402, cursor)
        if control is not None:
            return control
    
    # si existe obtenerla
    lei_id = respuesta['data']['id']
    
    # agregar al usuario a la tabla usuario_pertenece_lista_espera_individual
    respuesta = insertar_usuario_pertenece_lista_espera_individual(usuario['data']['id'], lei_id, cursor)
    control = _controlar_errores_query(respuesta, 500, "Error al agregar usuario a la lista de espera.", 402, cursor)
    if control is not None:
        return control
    
    return _msj_exito_helper("Usuario agregado a la lista de espera de abonados exitosamente.", cursor)
    

def agregar_usuario_a_lista_espera_abonados(dni_cliente, clase_id):
    """Agrega un usuario a la lista de espera de abonados para una clase específica."""
    cursor = conectarse_db()
    
    # Comprobar si el usuario existe
    usuario = consultar_usuario_por_dni(dni_cliente, cursor)
    control = _controlar_errores_query(usuario, 400, "Usuario no encontrado.", 401, cursor)
    if control is not None:
        return control
    
    # verificar que la clase existe
    respuesta  = consultar_clase_por_id(clase_id, cursor)
    control = _controlar_errores_query(respuesta, 400, "Clase no encontrada.", 401, cursor)
    if control is not None:
        return control

    # verificar si el usuario ya está en la lista de espera
    respuesta = consultar_lista_espera_abonado_usuario_por_idClase(clase_id, dni_cliente, cursor)
    control = _controlar_errores_query_sin_none(respuesta, 400, "Usuario ya está en la lista de espera.", 401, cursor)
    if control is not None:
        return control
    
    # verificar si existe una lista de espera para la clase
    respuesta = obtener_lista_espera_abonados_por_id_clase(clase_id, cursor)
    if respuesta['status'] == "error":
        return {
            "status": "error",
            "message": "Error al consultar la lista de espera."
        },500
    
    # Si no existe, crear una nueva lista de espera para la clase    
    if respuesta['data'] is None:
        respuesta = insertar_lista_espera_abonados(clase_id, cursor)
        control = _controlar_errores_query(respuesta, 500, "Error al crear la lista de espera.", 402, cursor)
        if control is not None:
            return control
    
    # si existe obtenerla
    lea_id = respuesta['data']['id']
    
    # agregar al usuario a la tabla usuario_pertenece_lista_espera_abonados
    respuesta = insertar_usuario_pertenece_lista_espera_abonados(usuario['data']['id'], lea_id, cursor)
    control = _controlar_errores_query(respuesta, 500, "Error al agregar usuario a la lista de espera.", 402, cursor)
    if control is not None:
        return control
    
    return _msj_exito_helper("Usuario agregado a la lista de espera de abonados exitosamente.", cursor)
    
