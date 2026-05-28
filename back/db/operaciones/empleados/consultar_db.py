from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def listar_empleados(cursor) -> dict:
    """Lista todos los usuarios que son empleados."""
    query = """
        SELECT id, nombre, apellido, rol_id, dni, correo, genero
        FROM Usuario
        WHERE rol_id IN (0, 1, 2, 4)
    """
    return ejecutar_fetchall(query, cursor)

def listar_correos_empleados(cursor) -> dict:
    """Lista todos los correos de los empleados."""
    query = """
        SELECT correo
        FROM Usuario
        WHERE rol_id = 2
    """
    return ejecutar_fetchall(query, cursor)

def listar_dnis_empleados(cursor) -> dict:
    """Lista todos los dnis de los empleados."""
    query = """
        SELECT dni
        FROM Usuario
        WHERE rol_id = 0 OR rol_id = 1 OR rol_id = 2 OR rol_id = 4
    """
    return ejecutar_fetchall(query, cursor)
