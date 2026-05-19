from db.operaciones.conectar_db import conectarse_db

def obtener_empleados() -> list:
    """Hace una consulta para listar todos los empleados, y devuelve una lista de tuplas"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Empleado")
    res = res.fetchall()
    cursor.connection.close()
    return res

# TODO: Cambiar
def buscar_empleado_por_correo(correo: str) -> tuple:
    """Hace una consulta por un Empleado con un correo pasado por parámetro,
        y devuelve una tupla. Corregidos los errores de sintaxis y alias."""
    cursor = conectarse_db()
    res = cursor.execute("""
        SELECT 
            e.id, 
            e.nombre, 
            r.nombre AS rol,
            CASE 
                WHEN a.id IS NOT NULL THEN 'ADMINISTRADOR'
                WHEN re.id IS NOT NULL THEN 'RECEPCIONISTA'
            END AS tipo
        FROM Empleado e
        INNER JOIN Rol r ON e.rol_id = r.id
        LEFT JOIN administrador a ON e.id = a.id
        LEFT JOIN recepcionista re ON e.id = re.id 
        WHERE e.correo = ?      
    """, (correo,))
    res = res.fetchone()
    cursor.connection.close()
    return res
