import sqlite3 as sqlite

# CONSTANTES

NOM_DB = "database.db"

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
