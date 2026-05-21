from db.operaciones.commitear_db import commitear

def insertar_rol_tener_permiso(rol_id: int, permiso_id: int, cursor):
    """Permite insertar una fila para la tabla Rol_Tener_Permiso"""
    query = f"""INSERT INTO Rol_Tener_Permiso (rol_id, permiso_id)
                VALUES ({rol_id}, {permiso_id});"""
    ejecutar_insertar(query, cursor)
