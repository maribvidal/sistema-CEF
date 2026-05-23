from db.operaciones.exception_handler import ejecutar_query 

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
