from db.operaciones.usuarios.consultar_db import consultar_usuario_por_dni
from db.operaciones.clases.consultar_db import consultar_clase_por_id
from db.operaciones.listas_espera.consultar_db import consultar_lista_espera_abonado_usuario_por_idClase, obtener_lista_espera_abonados_por_id_clase
from db.operaciones.listas_espera.insertar_db import insertar_lista_espera_abonados
from services import _controlar_errores_query, _controlar_errores_query_sin_none, _msj_exito_helper
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.usuario_pertenece_lista_espera_abonados.insertar_db import insertar_usuario_pertenece_lista_espera_abonados

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
        }
    
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
    