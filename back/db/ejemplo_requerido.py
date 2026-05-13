import sqlite3 as sqlite

from db import conectar_y_commitear

@conectar_y_commitear
def obtener_empleados(
    cursor: sqlite.Cursor
):

    empleados = cursor.execute(
        """
        SELECT *
        FROM Empleado
        """
    ).fetchall()

    return empleados

## manejo de roles de empleados

@conectar_y_commitear
def obtener_empleado_por_dni(
    cursor: sqlite.Cursor,
    dni: int
):

    empleado = cursor.execute(
        """
        SELECT *
        FROM Empleado
        WHERE dni = ?
        """,
        (dni,)
    ).fetchone()

    return empleado

@conectar_y_commitear
def obtener_rol_por_id(
    cursor: sqlite.Cursor,
    rol_id: int
):

    rol = cursor.execute(
        """
        SELECT *
        FROM Rol
        WHERE id = ?
        """,
        (rol_id,)
    ).fetchone()

    return rol

@conectar_y_commitear
def actualizar_rol_empleado(
    cursor: sqlite.Cursor,
    dni: int,
    nuevo_rol_id: int
):

    cursor.execute(
        """
        UPDATE Empleado
        SET rol_id = ?
        WHERE dni = ?
        """,
        (nuevo_rol_id, dni)
    )