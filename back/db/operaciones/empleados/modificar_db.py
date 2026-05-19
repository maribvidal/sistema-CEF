from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def actualizar_rol_empleado(
    empleado_id: int,
    nuevo_rol_id: int
):
    """Recibe el id de un empleado, y el id de un
        rol, y le asigna al empleado un nuevo rol."""
    cursor = conectarse_db()
    cursor.execute("""
        UPDATE Empleado
        SET rol_id = ?
        WHERE id = ?
    """, (nuevo_rol_id, empleado_id))
    commitear(cursor)
