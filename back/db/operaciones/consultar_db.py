import sqlite3 as sqlite




# ----------- ME GUSTARIA SEPARAR TODO POR ENTIDAD ASI EN LOS SERVICES IMPORTO TODO DEL ARCHIVO Y YA -----------
# ej:                                   from consultar_usuario import *




# CONSTANTES
from db import NOM_DB

## FUNCIONES DE CONEXIÓN A LA BD

def conectarse_db() -> sqlite.Cursor:
    """Crear una conexión con la BD y devolver un objeto Cursor"""
    conexion = sqlite.connect(NOM_DB)
    cursor = conexion.cursor()
    # Habilitar el control de Foreign Keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    return cursor

def desconectarse_db(cursor: sqlite.Cursor):
    """Cerrar la conexión con la BD a través del objeto Cursor"""
    cursor.connection.close()

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
    res = res.fetchone()
    cursor.connection.close()
    if res is not None:
        return res

def consultar_usuario_por_dni(dni: int) -> tuple:
    """Hace una consulta por un Usuario con un dni pasado por parámetro,
        y devuelve una tupla"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Usuario WHERE dni = ?", (dni,))
    res = res.fetchone()
    cursor.connection.close()
    return res

def consultar_usuario_por_correo(correo: str) -> tuple:
    """Hace una consulta por un Usuario con un correo pasado por parámetro,
        y devuelve una tupla"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Usuario WHERE correo = ?", (correo,))
    res = res.fetchone()
    cursor.connection.close()
    return res

def buscar_empleado_por_correo(correo: str) -> tuple:
    cursor = conectarse_db()
    res = cursor.execute("""
        SELECT 
            e.id, 
            e.nombre, 
            r.nombre AS rol
            CASE 
                WHEN a.empleado_id IS NOT NULL THEN 'ADMINISTRADOR'
                WHEN re.empleado_id IS NOT NULL THEN 'RECEPCIONISTA'
            END AS tipo
        FROM Empleado e
        INNNER JOIN Rol r ON e.rol_id = r.id
        LEFT JOIN administrador ON e.id = a.empleado_id
        LEFT JOIN recepcionista ON e.id = re.empleado_id 
        WHERE e.correo = ?      
    """, (correo,))
    res = res.fetchone()
    cursor.connection.close()
    return res

def listar_clases() -> list:
    """Hace una consulta para listar todas las clases, y devuelve una lista de tuplas"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Clase")
    res = res.fetchall()
    cursor.connection.close()
    return res

def listar_usuarios() -> list:
    """Hace una consulta para listar todos los usuarios, y devuelve una lista de tuplas"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Usuario")
    res = res.fetchall()
    cursor.connection.close()
    return res

def obtener_empleados() -> list:
    """Hace una consulta para listar todos los empleados, y devuelve una lista de tuplas"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Empleado")
    res = res.fetchall()
    cursor.connection.close()
    return res

def listar_pagos() -> list:
    """Hace una consulta para listar todos los pagos, y devuelve una lista de tuplas"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Pago")
    res = res.fetchall()
    cursor.connection.close()
    return res

def consultar_usuario_por_id(id: int) -> tuple:
    """Hace una consulta por un Usuario con un id pasado por parámetro,
        y devuelve una tupla"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Usuario WHERE id = ?", (id,))
    res = res.fetchone()
    cursor.connection.close()
    return res

def consultar_pagos_de_usuario(usuario_id: int) -> list:
    """Hace una consulta por los pagos de un Usuario con un id pasado por parámetro,
        y devuelve una lista de tuplas"""
    cursor = conectarse_db()
    res = cursor.execute("""
        SELECT 
            p.id, 
            p.monto, 
            p.fecha, 
            c.clase_id
        FROM Pago p
        INNER JOIN Pago_Pagar_Clase c ON p.id = c.pago_id
        WHERE p.usuario_id = ?
    """, (usuario_id,))
    res = res.fetchall()
    cursor.connection.close()
    return res

def obtener_rol_por_id(id: int) -> tuple:
    """Hace una consulta por un Rol con un id pasado por parámetro,
        y devuelve una tupla"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Rol WHERE id = ?", (id,))
    res = res.fetchone()
    cursor.connection.close()
    return res