from db.operaciones.exception_handler import ejecutar_query


def cambiar_permiso(dni, permiso, cursor):
    """Función para cambiar el permiso (rol) de un usuario.
       Recibe el DNI del usuario y el nuevo `rol_id` y lo actualiza
       en la tabla `Usuario`.
    """

    query = f"""
        UPDATE Usuario
        SET rol_id = {permiso}
        WHERE dni = {dni};
    """

    return ejecutar_query(query, cursor)
