from decoradores.decoradores_operaciones import conectar_y_commitear
import sqlite3 as sqlite

@conectar_y_commitear
def checkeo_dni_registrado(cursor: sqlite.Cursor, dni: int):
    cursor.execute("SELECT 1 FROM usuarios WHERE dni = ?", (dni,))
    return cursor.fetchone() 

@conectar_y_commitear
def checkeo_correo_registrado(cursor: sqlite.Cursor, correo: str):
    cursor.execute("SELECT 1 FROM usuarios WHERE correo = ?", (correo,))
    return cursor.fetchone() 

@conectar_y_commitear
def buscar_usuario_por_correo(cursor: sqlite.Cursor, correo: str):
    cursor.execute("""
        SELECT id, correo, contraseña 
        FROM clientes
        WHERE correo = ?      
    """, (correo,))
    return cursor.fetchone()

@conectar_y_commitear
def buscar_empleado_por_correo(cursor: sqlite.Cursor, correo: str):
    cursor.execute("""
        SELECT 
            e.id, 
            e.nombre, 
            r.nombre AS rol
            CASE 
                WHEN a.empleado_id IS NOT NULL THEN 'ADMINISTRADOR'
                WHEN re.empleado_id IS NOT NULL THEN 'RECEPCIONISTA'
            END AS tipo
        FROM empleados e
        INNNER JOIN roles r ON e.rol_id = r.id
        LEFT JOIN administrador ON e.id = a.empleado_id
        LEFT JOIN recepcionista ON e.id = re.empleado_id 
        WHERE e.correo = ?      
    """, (correo,))
    return cursor.fetchone()