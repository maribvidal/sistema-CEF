import sqlite3 as sqlite

from db import conectar_y_commitear

@conectar_y_commitear
def checkeo_dni_registrado(cursor: sqlite.Cursor, dni: int):
    cursor.execute("SELECT 1 FROM usuarios WHERE dni = ?", (dni,))
    return cursor.fetchone() 

@conectar_y_commitear
def checkeo_correo_registrado(cursor: sqlite.Cursor, correo: str):
    cursor.execute("SELECT 1 FROM usuarios WHERE correo = ?", (correo,))
    return cursor.fetchone() 