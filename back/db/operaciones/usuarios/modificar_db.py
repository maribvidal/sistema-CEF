from db.operaciones.commitear_db import commitear

def modificar_perfil_usuario(
    usuario_dni: int,
    correo: str,
    telefono: str,
    cursor
):
    """Recibe el id de un usuario, y recibe el
        nuevo correo y teléfono que se les quiere
        poner, y modifica al usuario."""
    query1 = f"""
        UPDATE Cuenta
        SET correo = '{correo}'
        WHERE dni = {usuario_dni}
    """

    query2 = f"""
        UPDATE Usuario
        SET telefono = '{telefono}'
        WHERE dni = {usuario_dni}
    """

    ejecutar_query(query1,cursor)
    ejecutar_query(query2,cursor)
