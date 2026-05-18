from db.operaciones import conectarse_db, commitear

def modificar_perfil_usuario(
    usuario_id: int,
    correo: str,
    telefono: str
):
    """Recibe el id de un usuario, y recibe el
        nuevo correo y teléfono que se les quiere
        poner, y modifica al usuario."""
    cursor = conectarse_db()
    cursor.execute("""
        UPDATE Usuario
        SET correo = ?, telefono = ?
        WHERE id = ?
    """, (correo, telefono, usuario_id))
    commitear(cursor)
    
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
