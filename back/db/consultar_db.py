from db import NOM_DB
import sqlite3 as sqlite

## FUNCIONES DE CONEXIÓN A LA BD

def conectarse_db() -> sqlite.Cursor:
    """Crear una conexión con la BD y devolver un objeto Cursor"""
    conexion = sqlite.connect(NOM_DB)
    cursor = conexion.cursor()
    return cursor

## FUNCIONES DE CONSULTA

# - ¿Cómo voy a hacer cuando tenga que devolver varias tuplas?
# - ¿No me conviene hacer una función que devuelva un permiso
#    en base a un parámetro cualquiera recibido?
# - ¿Puedo refactorizar ests funciones?

def consultar_permiso_por_id(id: int) -> tuple:
    """Hace una consulta por un Permiso con un id pasado por parámetro,
        y devuelve una tupla"""
    cursor = conectarse_db()
    res = cursor.execute(f"SELECT id FROM Permiso WHERE id = {id}")
    cursor.connection.close()
    res = res.fetchone()
    if res is not None:
        return res
