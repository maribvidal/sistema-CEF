from db.operaciones.commitear_db import commitear

def actualizar_rol_empleado(cursor, 
    empleado_id: int,
    nuevo_rol_id: int,
    cursor
):
    """Recibe el id de un empleado, y el id de un
        rol, y le asigna al empleado un nuevo rol."""
    query = f"""UPDATE Empleado
                SET rol_id = {nuevo_rol_id}
                WHERE id = {empleado_id};"""
    ejecutar_query(query, cursor)
