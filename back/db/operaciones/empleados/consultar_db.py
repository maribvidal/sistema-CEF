from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone


def listar_empleados(cursor) -> dict:
    """Lista todos los usuarios que son empleados."""
    query = """
        SELECT id, nombre, apellido, rol_id, dni, correo
        FROM Usuario
        WHERE rol_id IN (1, 2)
    """
    return ejecutar_fetchall(query, cursor)

def listar_empleados_desactivados(cursor) -> dict:
    """Lista todos los usuarios que son empleados desactivados."""
    query = """
        SELECT id, nombre, apellido, rol_id, dni, correo
        FROM Usuario
        WHERE rol_id = 0
    """
    return ejecutar_fetchall(query, cursor)