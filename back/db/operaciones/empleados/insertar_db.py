from db.operaciones.exception_handler import ejecutar_insertar

def insertar_recepcionista(dni, nombre, apellido, correo, contraseña, genero, cursor) -> dict:
    """Inserta un empleado con los siguientes datos: dni, nombre, apellido, correo, 
        contraseña, y genero."""
    
    query = f"""
        INSERT INTO Usuario (dni, nombre, apellido, correo, contraseña, genero, rol_id)
                VALUES ({dni}, '{nombre}', '{apellido}', '{correo}', '{contraseña}', '{genero}', 2);
    """

    return ejecutar_insertar(query, cursor)
