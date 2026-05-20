from db.operaciones.commitear_db import commitear

def insertar_rol_tener_permiso(cursor, rol_id: int, permiso_id: int):
    """Permite insertar una fila para la tabla Rol_Tener_Permiso"""
    query = f"""INSERT INTO Rol_Tener_Permiso (rol_id, permiso_id)
                VALUES ({rol_id}, {permiso_id});"""
    cursor.execute(query)
    commitear(cursor)
    return cursor.lastrowid
