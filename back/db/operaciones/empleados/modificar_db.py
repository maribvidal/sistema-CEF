from db.operaciones.exception_handler import ejecutar_fetchone, ejecutar_query

# falta implementar & testear
def modificar_empleado(
        empleado_dni: int, 
        nombre: str, 
        apellido, 
        correo, 
        contraseña, 
        fecha_nac, 
        telefono, 
        genero, 
        rol_id, 
        cursor
    ) -> dict:
    """Modifica un empleado específico en la base de datos, utilizando su ID como referencia.
        Recibe el ID del empleado a modificar y los nuevos datos (nombre, apellido, cargo, salario).
        Devuelve un diccionario con el resultado de la operación."""

    query_verificacion = f"""
        SELECT rol_id
        FROM Usuario
        WHERE dni = {empleado_dni}
    """
    usuario = ejecutar_fetchone(query_verificacion, cursor)
    print("FUNCIONA ESTO?")
    print(usuario["data"].keys())
    print(usuario["data"]["rol_id"])


    if not usuario:
        return {
            "status": "error",
            "message": "Empleado no encontrado"
        }
    elif usuario["data"]["rol_id"] not in (1, 2): # o sea si el usuario no es ni gerente ni administrador
        return {
            "status": "error",
            "message": "El usuario no es un empleado"
        }
    
    print("Se encontró el usuario creo")
    
    query_update = f"""
        UPDATE Usuario
        SET nombre = '{nombre}',
            apellido = '{apellido}',
            correo = '{correo}',
            contraseña = '{contraseña}',
            fecha_nac = '{fecha_nac}',
            telefono = '{telefono}',
            genero = '{genero}',
            rol_id = {rol_id}
        WHERE dni = {empleado_dni}
    """

    print(query_update)

    return ejecutar_query(query_update, cursor)

