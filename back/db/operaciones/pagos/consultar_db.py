def consultar_pagos_de_usuario(cursor, usuario_id: int) -> list:
    """Hace una consulta por los pagos de un Usuario con un id pasado por parámetro,
       y devuelve una lista de tuplas."""
    query = """
        SELECT
            Pago.id,
            Pago.monto,
            Clase.id AS clase_id
        FROM Pago
        INNER JOIN Pago_Pagar_Clase ON Pago.id = Pago_Pagar_Clase.pago_id
        INNER JOIN Clase ON Pago_Pagar_Clase.clase_id = Clase.id
        WHERE Pago.usuario_id = ?;
    """
    res = cursor.execute(query, (usuario_id,))
    return res.fetchall()


def listar_pagos(cursor) -> list:
    """Hace una consulta por todos los pagos registrados en la base de datos,
        y devuelve una lista de tuplas"""
    query = """
        SELECT
            p.id,
            p.monto,
            p.fecha,
            c.id AS clase_id,
            p.usuario_id
        FROM Pago p
        INNER JOIN Pago_Pagar_Clase c ON p.id = c.pago_id
    """
    res = cursor.execute(query)
    return res.fetchall()
