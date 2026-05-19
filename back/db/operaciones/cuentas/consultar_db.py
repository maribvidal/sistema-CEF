from db.operaciones.conectar_db import conectarse_db

def consultar_cuenta_por_id(id: int) -> tuple:
    """Función que consulta una cuenta por su id, y devuelve la tupla."""
    conexion = conectarse_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM cuentas WHERE id_cuenta = %s", (id,))
    res = cursor.fetchone()
    conexion.close()
    return res
