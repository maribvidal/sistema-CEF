from db.operaciones.exception_handler import ejecutar_query 

def modificar_perfil_usuario(
    usuario_id: int,
    dni,
    nombre,
    apellido,
    fecha_nac,
    correo,
    telefono,
    cursor
):
    """Recibe el id de un usuario, y recibe el
        nuevo correo y teléfono que se les quiere
        poner, y modifica al usuario."""

    query = f"""
        UPDATE Usuario
        SET dni = '{dni}', 
            nombre = '{nombre}', 
            apellido = '{apellido}', 
            fecha_nac = '{fecha_nac}', 
            correo = '{correo}', 
            telefono = '{telefono}'
        WHERE id = {usuario_id};
    """

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
