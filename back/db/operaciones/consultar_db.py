from db.operaciones.conectar_db import conectarse_db

# ----------- ME GUSTARIA SEPARAR TODO POR ENTIDAD ASI EN LOS SERVICES IMPORTO TODO DEL ARCHIVO Y YA -----------
# ej:                                   from consultar_usuario import *

## FUNCIONES DE CONSULTA

# - ¿Cómo voy a hacer cuando tenga que devolver varias tuplas?
# - ¿No me conviene hacer una función que devuelva un permiso
#    en base a un parámetro cualquiera recibido?



def consultar_permiso_por_id(id: int) -> tuple:
    """Hace una consulta por un Permiso con un id pasado por parámetro,
        y devuelve una tupla"""
    cursor = conectarse_db()
    res = cursor.execute(f"SELECT id FROM Permiso WHERE id = {id}")
    res = res.fetchone()
    cursor.connection.close()
    try:
        return res[0]
    except TypeError:
        print("No se encontró el permiso con el id proporcionado.")
        return ()

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

def consultar_usuario_por_id(id: int) -> tuple:
    """Hace una consulta por un Usuario con un id pasado por parámetro,
        y devuelve una tupla"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Usuario WHERE id = ?", (id,))
    res = res.fetchone()
    cursor.connection.close()
    return res

# def consultar_pagos_de_usuario(usuario_id: int) -> list:
#     """Hace una consulta por los pagos de un Usuario con un id pasado por parámetro,
#         y devuelve una lista de tuplas"""
#     cursor = conectarse_db()
#     res = cursor.execute("""
#         SELECT 
#             p.id, 
#             p.monto, 
#             p.fecha, 
#             c.id AS clase_id
#         FROM Pago p
#         INNER JOIN Clase c ON p.clase_id = c.id
#         WHERE p.usuario_id = ?
#     """, (usuario_id,))
#     res = res.fetchall()
#     cursor.connection.close()
#     return res
def consultar_pagos_de_usuario(usuario_id: int) -> list:
    """Hace una consulta por los pagos de un Usuario con un id pasado por parámetro,
       y devuelve una lista de tuplas. Mantiene el formato original de Mariano."""
    cursor = conectarse_db()
    res = cursor.execute("""
        SELECT 
            Pago.id, 
            Pago.monto, 
            Clase.id AS clase_id
        FROM Pago
        INNER JOIN Pago_Pagar_Clase ON Pago.id = Pago_Pagar_Clase.pago_id
        INNER JOIN Clase ON Pago_Pagar_Clase.clase_id = Clase.id
        WHERE Pago.usuario_id = ?
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
