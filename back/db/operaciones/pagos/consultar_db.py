from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

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
def consultar_pagos_de_usuario(usuario_id: int, cursor) -> dict:
    """Hace una consulta por los pagos de un Usuario con un id pasado por parámetro,
       y devuelve una lista de tuplas."""
    query = f"""
        SELECT
            p.id,
            p.monto,
            c.id
        FROM Pago p
        INNER JOIN Pago_Pagar_Clase ppc ON p.id = ppc.pago_id
        INNER JOIN Clase c ON ppc.clase_id = c.id
        WHERE p.usuario_id = {usuario_id};
    """
    return ejecutar_fetchall(query, cursor)

def listar_pagos(cursor):
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
    return ejecutar_fetchall(query, cursor)

def listar_pagos_fechas(cursor, fecha_inicio, fecha_fin):
    """Hace una consulta por todos los pagos registrados en la base de datos entre dos fechas,
        y devuelve una lista de tuplas"""
    query = f"""
        SELECT
            p.id,
            p.monto,
            p.fecha,
            c.id AS clase_id,
            p.usuario_id
        FROM Pago p
        INNER JOIN Pago_Pagar_Clase c ON p.id = c.pago_id
        WHERE p.fecha >= '{fecha_inicio}' AND p.fecha <= '{fecha_fin}';
    """
    return ejecutar_fetchall(query, cursor)

def verificar_existencia_pago_por_id(id_pago: int, cursor) -> dict:
    """Hace una consulta por un pago con un id pasado por parámetro."""
    query = f"""
        SELECT 1
        FROM Pago p
        WHERE p.id = {id_pago};
    """
    return ejecutar_fetchone(query, cursor)

def verificar_estado_pago_por_id(id_pago: int, cursor) -> dict:
    """Hace una consulta por el estado de un pago con un id pasado por parámetro."""
    query = f"""
        SELECT p.estado
        FROM Pago p
        WHERE p.id = {id_pago};
    """
    return ejecutar_fetchone(query, cursor)