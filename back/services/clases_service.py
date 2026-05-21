from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear
from db.operaciones.clase_ocurrir_sala.insertar_db import insertar_clase_ocurrir_sala
from db.operaciones.clase_ocurrir_sala.modificar_db import modificar_clase_ocurrir_sala
from db.operaciones.clases.consultar_db import listar_clases, consultar_clase_por_id
from db.operaciones.clases.insertar_db import insertar_clase
from db.operaciones.clases.borrar_db import borrar_clase
from db.operaciones.clases.modificar_db import modificar_clase
from db.operaciones.actividades.consultar_db import listar_actividades
from db.operaciones.profesores.consultar_db import listar_profesores

def listar_clases_service():
    """Service que lista las clases"""

    cursor = conectarse_db()

    respuesta = listar_clases(cursor)

    if respuesta['status'] == 'error':
        commitear(cursor)
        cursor.connection.close()
        return respuesta

    if respuesta['status'] == 'success' and not respuesta['data']:
        commitear(cursor)
        cursor.connection.close()
        return {
            "error": "No se encontraron clases"
        }, 404

    commitear(cursor)
    cursor.connection.close()
    return respuesta['data'], 200

def listar_actividades_service():
    """Service que lista las actividades"""
    cursor = conectarse_db()
    respuesta = listar_actividades(cursor)
    commitear(cursor)
    cursor.connection.close()
    # No devolvemos 404 si está vacío para que el select del front no falle, solo devolvemos la lista vacía
    return respuesta, 200

def listar_profesores_service():
    """Service que lista los profesores"""
    cursor = conectarse_db()
    respuesta = listar_profesores(cursor)
    commitear(cursor)
    cursor.connection.close()
    return respuesta, 200

def publicar_clase_service(
    estado: str,
    id_actividad: int,
    id_profesor: int,
    fecha,
    hora: int,
    sala: int
):
    """Service que publica una clase"""

    cursor = conectarse_db()

    respuesta = insertar_clase(estado, id_actividad, id_profesor, cursor)

    if respuesta['status'] == 'error':
        cursor.connection.close()
        return respuesta['message'], 400

    respuesta2 = insertar_clase_ocurrir_sala(respuesta['data'], sala, fecha, hora, cursor)

    if respuesta2['status'] == 'error':
        print(respuesta2['message'])
        cursor.connection.close()
        return respuesta2

    commitear(cursor)
    cursor.connection.close()
    return {
        "mensaje": "Clase publicada exitosamente."
    }, 201

def modificar_clase_service(
    clase_id: int,
    estado: str,
    id_actividad: int,
    id_profesor: int,
    fecha,
    hora: int,
    sala: int
):
    """Service que modifica una clase"""

    cursor = conectarse_db()

    respuesta_consulta = consultar_clase_por_id(clase_id, cursor)

    if respuesta_consulta['status'] == 'error':
        cursor.connection.close()
        return respuesta_consulta

    if respuesta_consulta['status'] == 'success' and not respuesta_consulta['data']:
        cursor.connection.close()
        return {
            "error": "Clase no encontrada"
        }, 404

    respuesta = modificar_clase(clase_id, estado, id_actividad, id_profesor, cursor)

    if respuesta['status'] == 'error':
        cursor.connection.close()
        return respuesta

    respuesta2 = modificar_clase_ocurrir_sala(clase_id, sala, fecha, hora, cursor)

    if respuesta2['status'] == 'error':
        cursor.connection.close()
        return respuesta2
    
    commitear(cursor)

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
        return respuesta_consulta

    if respuesta_consulta['status'] == 'success' and not respuesta_consulta['data']:
        cursor.connection.close()
        return {
            "error": "Clase no encontrada"
        }, 404

    respuesta = borrar_clase(clase_id, cursor)

    if respuesta['status'] == 'error':
        # Hay que avisar si hay pagos pendientes
        cursor.connection.close()
        return respuesta

    commitear(cursor)
    cursor.connection.close()
    return {
        "mensaje": "Clase eliminada exitosamente."
    }, 200
