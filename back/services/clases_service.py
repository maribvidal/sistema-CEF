from db.operaciones.conectar_db import conectarse_db
from db.operaciones.clase_ocurrir_sala.insertar_db import insertar_clase_ocurrir_sala
from db.operaciones.clase_ocurrir_sala.modificar_db import modificar_clase_ocurrir_sala
from db.operaciones.clase_ocurrir_sala.consultar_db import consultar_clase_ocurrir_sala_por_fecha_hora_sala, consultar_clase_ocurrir_sala_por_claseid_fecha_hora
from db.operaciones.clases.consultar_db import listar_clases, consultar_clase_por_id
from db.operaciones.clases.insertar_db import insertar_clase
from db.operaciones.clases.modificar_db import modificar_clase
from db.operaciones.clases.modificar_db import modificar_clase_estado
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_id, obtener_clase_usuario_fecha_hora
from db.operaciones.usuario_inscribir_clase.insertar_db import insertar_usuario_inscribir_clase_por_id

def listar_clases_service():
    """Service que lista las clases"""

    cursor = conectarse_db()

    respuesta = listar_clases(cursor)

    if respuesta['status'] == 'error':
        cursor.connection.close()
        return respuesta, 400

    if respuesta['status'] == 'success' and not respuesta['data']:
        cursor.connection.close()
        return {
            "error": "No se encontraron clases."
        }, 401

    cursor.connection.close()
    return respuesta, 200

def publicar_clase_service(
    estado: str,
    id_actividad: int,
    id_profesor: int,
    fecha,
    hora: str,
    sala: int,
    cupo_maximo: int
):
    """Service que publica una clase"""
    """
    def _revisar_ocupacion_sala(sala, fecha, hora, cursor) -> dict:
        ""Función auxiliar que revisa si la sala está ocupada en la 
            fecha y hora dadas""
        tupla_consulta = consultar_clase_ocurrir_sala_por_fecha_hora_sala(sala, fecha, hora, cursor)

        if tupla_consulta['status'] == 'error':
            return {
                "status": "error",
                "message": tupla_consulta['message']
            }, 400

        # Si no tiró antes, todo debería estar bien
        if tupla_consulta['status'] == 'success' and tupla_consulta['data'] is not None:
             return {
                "status": "error",
                "message": "La sala ya está ocupada en la fecha y hora dadas."
            }, 401

        return tupla_consulta
    """

    cursor = conectarse_db()

    # Comprobar que la sala no se encuentre ocupada en la fecha y hora dadas

    respuesta = consultar_clase_ocurrir_sala_por_fecha_hora_sala(sala, fecha, hora, cursor)

    if respuesta['status'] == 'error':
        return {
            "status": "error",
            "message": respuesta['message']
        }, 400

    # Si no tiró antes, todo debería estar bien
    if respuesta['status'] == 'success' and respuesta['data'] is not None:
            return {
            "status": "error",
            "message": "La sala ya está ocupada en la fecha y hora dadas."
        }, 401

    # Intentar insertar la clase

    respuesta2 = insertar_clase(estado, id_actividad, id_profesor, cupo_maximo, cursor)

    if respuesta2['status'] == 'error':
        cursor.connection.close()
        return respuesta2['message'], 403

    # Intentar insertar la relación clase_ocurrir_sala

    respuesta3 = insertar_clase_ocurrir_sala(respuesta2['data'], sala, fecha, hora, cursor)

    if respuesta3['status'] == 'error':
        print(respuesta3['message'])
        cursor.connection.close()
        return respuesta3, 404

    cursor.connection.commit()
    cursor.connection.close()
    return {
        "mensaje": "Clase publicada exitosamente."
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
    print("Respuesta consulta clase por id: ", respuesta_consulta)

    if respuesta_consulta['status'] == 'error':
        cursor.connection.close()
        return respuesta_consulta, 400

    if respuesta_consulta['status'] == 'success' and not respuesta_consulta['data']:
        cursor.connection.close()
        return {
            "error": "Clase no encontrada."
        }, 401

    respuesta = modificar_clase(clase_id, estado, id_actividad, id_profesor, cupo_maximo, cursor)
    print("Respuesta modificar clase: ", respuesta)

    if respuesta['status'] == 'error':
        cursor.connection.close()
        return respuesta, 402

    print("Intentando modificar clase_ocurrir_sala...")
    print("Datos para modificar clase_ocurrir_sala: clase_id: ", clase_id, " sala: ", sala, " fecha: ", fecha, " hora: ", hora)
    respuesta2 = modificar_clase_ocurrir_sala(clase_id, sala, fecha, hora, cursor)
    print("Respuesta modificar clase_ocurrir_sala: ", respuesta2)

    if respuesta2['status'] == 'error':
        cursor.connection.close()
        return respuesta2, 403
    
    cursor.connection.commit()
    cursor.connection.close()

    return {
        "mensaje": "Clase modificada exitosamente."
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
        "mensaje": "Clase eliminada exitosamente."
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
        "mensaje": "Clase cancelada exitosamente."
    }, 200

def reservar_clase_service(clase_id: int, id_usuario: int, fecha, hora):
    """Service que, dado un usuario, lo intenta inscribir
        en una clase con una fecha y hora dada."""

    cursor = conectarse_db()

    # Comprobar que exista la clase

    res_clase = consultar_clase_por_id(clase_id, cursor)

    if res_clase['status'] == 'error':
        cursor.connection.close()
        return res_clase, 400

    if res_clase['status'] == 'success' and not res_clase['data']:
        cursor.connection.close()
        return {
            "error": "Clase no encontrada."
        }, 401

    # Comprobar que exista el clase_ocurrir_sala

    res_clase_ocu_sala = consultar_clase_ocurrir_sala_por_claseid_fecha_hora(clase_id, fecha, hora, cursor)

    if res_clase_ocu_sala['status'] == 'error':
        cursor.connection.close()
        return res_clase_ocu_sala, 402
    
    if res_clase_ocu_sala['data'] is None:
        cursor.connection.close()
        return {
            "error": "Clase_ocurrir_sala no encontrada."
        }, 403

    id_clase_ocu_sala = res_clase_ocu_sala['data']['id']

    # Comprobar que exista el usuario

    res_usuario = consultar_usuario_por_id(id_usuario, cursor)

    if res_usuario['status'] == 'error':
        cursor.connection.close()
        return res_usuario, 404

    if res_usuario['status'] == 'sucess' and not res_usuario['data']:
        cursor.connection.close()
        return {
            "error": "Usuario no encontrado."
        }, 405

    # Comprobar que el usuario no se haya inscrito ya a otra clase en esa hora

    res_usuario_clase = obtener_clase_usuario_fecha_hora(id_usuario, fecha, hora, cursor)

    if res_usuario_clase['status'] == 'error':
        cursor.connection.close()
        return res_usuario_clase['message'], 406

    ## Se compara si es mayor a 0 puesto que, si el dict no tiene tuplas, entonces
    ## va a devolver una cantidad de 0 el len().
    if len(res_usuario_clase['data']) > 0:
        cursor.connection.close()
        return {
            "error": "El usuario ya se encuentra inscripto en esa clase."
        }, 407

    # Comprobar el cupo de la clase

    # Insertar el usuario en la clase

    res_usu_ins_cla = insertar_usuario_inscribir_clase_por_id(id_usuario, clase_id, id_clase_ocu_sala, cursor)

    if res_usu_ins_cla['status'] == 'error':
        cursor.connection.close()
        return {
            "error": res_usu_ins_cla['message']
        }, 500

    cursor.connection.commit()
    cursor.connection.close()
    return {
        "mensaje": "Reserva realizada exitosamente."
    }, 200
