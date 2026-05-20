from db.operaciones.exception_handler import ejecutar_query 

def modificar_perfil_usuario(
    usuario_dni: int,
    correo: str,
    telefono: str
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

    print(ejecutar_query(query1))
    print(ejecutar_query(query2))
