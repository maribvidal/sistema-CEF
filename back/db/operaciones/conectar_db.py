import os
import sqlite3 as sqlite

def conectarse_db() -> sqlite.Cursor:
    """Crear una conexión con la BD y devolver un objeto Cursor"""
    conexion = sqlite.connect(os.getenv("NOM_DB"))
    conexion.row_factory = sqlite.Row
    cursor = conexion.cursor()
    # Habilitar el control de Foreign Keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    return cursor
