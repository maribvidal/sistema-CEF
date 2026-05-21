import sqlite3 as sqlite

def commitear(cursor: sqlite.Cursor):
    """Recibe un Cursor y con él hace commit y cierra la conexión con la BD"""
    cursor.connection.commit()
