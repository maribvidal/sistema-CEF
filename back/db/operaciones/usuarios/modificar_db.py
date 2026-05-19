from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

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
