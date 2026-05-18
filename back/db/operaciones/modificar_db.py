import sqlite3 as sqlite
from db import NOM_DB

def conectarse_db() -> sqlite.Cursor:
    """Crea una conexión a la BD y devuelve un objeto Cursor"""
    conexion = sqlite.connect(NOM_DB)
    cursor = conexion.cursor()
    # Habilitar el control de Foreign Keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    return cursor

def commitear(cursor: sqlite.Cursor):
    """Recibe un Cursor y con él hace commit y cierra la conexión con la BD"""
    cursor.connection.commit()
    cursor.connection.close()

def modificar_perfil_usuario(
    usuario_id: int,
    correo: str,
    telefono: str
):
    cursor = conectarse_db()
    cursor.execute("""
        UPDATE Usuario
        SET correo = ?, telefono = ?
        WHERE id = ?
    """, (correo, telefono, usuario_id))
    commitear(cursor)
    
def actualizar_rol_empleado(
    empleado_id: int,
    nuevo_rol_id: int
):
    cursor = conectarse_db()
    cursor.execute("""
        UPDATE Empleado
        SET rol_id = ?
        WHERE id = ?
    """, (nuevo_rol_id, empleado_id))
    commitear(cursor)