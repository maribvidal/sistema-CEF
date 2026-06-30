from db.operaciones.exception_handler import ejecutar_query 
import datetime

def modificar_perfil_usuario(
    cursor,
    usuario_id: int,
    dni=None,
    nombre=None,
    apellido=None,
    fecha_nac=None,
    correo=None,
    telefono=None,
):
    """Recibe el id de un usuario, y recibe cualquiera
        de los atributos de usuario que se quieran cambiar."""


    query = "UPDATE Usuario SET"
    if dni is not None:
        query += f" dni = '{dni}',"
    if nombre is not None:
        query += f" nombre = '{nombre}',"
    if apellido is not None:
        query += f" apellido = '{apellido}',"
    if fecha_nac is not None:
        query += f" fecha_nac = '{fecha_nac}',"
    if correo is not None:
        query += f" correo = '{correo}',"
    if telefono is not None:
        query += f" telefono = '{telefono}'"
    query = query.strip(",")  # Elimina la coma final si existe
    query += f" WHERE id = {usuario_id};"

    return ejecutar_query(query,cursor)

def modificar_contraseña(
    usuario_id: int,
    nueva_contraseña: str,
    cursor
):
    """Recibe el id de un usuario, y lo actualiza cambiando
        su contraseña por una nueva."""

    query = f"""
        UPDATE Usuario
        SET contraseña = '{nueva_contraseña}'
        WHERE id = {usuario_id};
    """

    return ejecutar_query(query,cursor)

def modificar_avatar(usuario_id: int, imagen_id: int, cursor):
    """Recibe el id de un usuario y el id de una imagen, y lo actualiza cambiando
        su avatar por la nueva imagen."""

    query = f"""
        UPDATE Usuario
        SET imagen_id = {imagen_id}
        WHERE id = {usuario_id};
    """

    return ejecutar_query(query,cursor)

def modificar_estado_usuario(usuario_id: int, cursor):
    """Recibe el id de un usuario y lo actualiza cambiando
        su estado a inactivo (0) o activo (1)."""

    query = f"""
        UPDATE Usuario
        SET estado = 1
        WHERE id = {usuario_id};
    """

    return ejecutar_query(query,cursor)

def desactivar_usuario(usuario_id: int, cursor):
    """Recibe el id de un usuario y actualiza su rol al 13."""

    query = f"""
        UPDATE Usuario
        SET rol_id = 13
        WHERE id = {usuario_id}
    """

    return ejecutar_query(query,cursor)

def borrar_usuario(usuario_id: int, cursor):
    """Recibe el id de un usuario y actualiza su rol al 23."""

    query = f"""
        UPDATE Usuario
        SET rol_id = 23
        WHERE id = {usuario_id}
    """

    return ejecutar_query(query,cursor)
