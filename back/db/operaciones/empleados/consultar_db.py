from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def obtener_empleados(cursor) -> dict:
    """Hace una consulta para listar todos los empleados, y devuelve una lista de tuplas"""
    return ejecutar_fetchall("SELECT * FROM Empleado", cursor)

# TODO: Cambiar
def buscar_empleado_por_correo(correo: str, cursor) -> dict:
    """Hace una consulta por un Empleado con un correo pasado por parámetro,
        y devuelve una tupla. Corregidos los errores de sintaxis y alias."""
    query = f"""
        SELECT 
            e.id, 
            c.nombre, 
            r.nombre AS rol,
            CASE 
                WHEN a.id IS NOT NULL THEN 'ADMINISTRADOR'
                WHEN re.id IS NOT NULL THEN 'RECEPCIONISTA'
            END AS tipo
        FROM Empleado e
        INNER JOIN Cuenta c ON e.dni = c.dni
        INNER JOIN Rol r ON e.rol_id = r.id
        LEFT JOIN administrador a ON e.id = a.id
        LEFT JOIN recepcionista re ON e.id = re.id 
        WHERE c.correo = '{correo}'      
    """;
    return ejecutar_fetchone(query, cursor)
