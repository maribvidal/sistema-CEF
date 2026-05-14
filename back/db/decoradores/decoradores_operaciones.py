import sqlite3 as sqlite
from db import NOM_DB

## FUNCIONES DE CONEXIÓN CON LA BD

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

def conectar_y_commitear(fun=None):
    """Decorador que, dada una función, hace que se ejecute
        la función que establece a la conexión a la BD antes
        de que se ejecute el código de la función recibida, y
        que luego ejecuta la función que hace commit y termina
        esa conexión."""
    def wrap(fun):
        def decorated_function():
            cursor = conectarse_db()
            fun(cursor)
            commitear(cursor)
        return decorated_function
    if fun is None:
        return wrap
    return wrap(fun)
