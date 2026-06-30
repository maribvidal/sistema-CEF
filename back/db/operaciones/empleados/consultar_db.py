from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def obtener_empleado_por_dni(dni, cursor) -> dict:
    """Devuelve una tupla que representa un empleado."""
    query = f"SELECT * FROM Usuario WHERE rol_id IN (0, 1, 2, 4, 5) AND dni = {dni}"
    return ejecutar_fetchone(query, cursor) 

def listar_empleados(cursor) -> dict:
    """Lista todos los usuarios que son empleados."""
    # UN PROFESOR TAMBIÉN ES UN EMPLEADOOOOOOO
    query = """
        SELECT id, nombre, apellido, rol_id, dni, genero, telefono
        FROM Usuario
        WHERE rol_id IN (0, 1, 2, 4, 5, 10, 11, 12, 14, 15, 20, 21, 22, 24, 25)
    """
    return ejecutar_fetchall(query, cursor)

def listar_correos_empleados(cursor) -> dict:
    """Lista todos los correos de los empleados."""
    query = """
        SELECT correo
        FROM Usuario
        WHERE rol_id IN (0, 1, 2, 4, 5, 10, 11, 12, 14, 15, 20, 21, 22, 24, 25)
    """
    return ejecutar_fetchall(query, cursor)

def listar_dnis_empleados(cursor) -> dict:
    """Lista todos los dnis de los empleados."""
    query = """
        SELECT dni
        FROM Usuario
        WHERE rol_id IN (0, 1, 2, 4, 5, 10, 11, 12, 14, 15, 20, 21, 22, 24, 25)
    """
    return ejecutar_fetchall(query, cursor)
