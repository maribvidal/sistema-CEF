from db.operaciones.conectar_db import conectarse_db

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

def listar_pagos():
    """Hace una consulta por todos los pagos registrados en la base de datos,
        y devuelve una lista de tuplas"""
    cursor = conectarse_db()
    res = cursor.execute("""
        SELECT 
            p.id, 
            p.monto, 
            p.fecha, 
            c.id AS clase_id,
            u.id AS usuario_id
        FROM Pago p
        INNER JOIN Clase c ON p.clase_id = c.id
        INNER JOIN Usuario u ON p.usuario_id = u.id
    """)
    res = res.fetchall()
    cursor.connection.close()
    return res