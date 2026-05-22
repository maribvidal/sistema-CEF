from db.operaciones.exception_handler import ejecutar_query 

def modificar_perfil_usuario(
    usuario_id: int,
    correo: str,
    telefono: str,
    cursor
):
    """Recibe el id de un usuario, y recibe el
        nuevo correo y teléfono que se les quiere
        poner, y modifica al usuario."""

    query = f"""
        UPDATE Usuario
        SET telefono = '{telefono}', correo = '{correo}'
        WHERE id = {usuario_id};
    """

    return ejecutar_query(query,cursor)
