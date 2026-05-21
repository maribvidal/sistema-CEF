from db.operaciones import consultar_usuario_por_dni, obtener_rol_por_id, obtener_empleados, actualizar_rol_empleado
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def obtener_empleados_service():
    """Service que comprueba que hayan empleados registrados,
        y si los hay, devuelve una lista de empleados"""
    cursor = conectarse_db()
    empleados = obtener_empleados(cursor)

    if not empleados:
        commitear(cursor)
        return {
            "error": "No hay empleados registrados"
        }, 404
        
    empleados_lista = []
    for empleado in empleados:
        empleados_lista.append({
            "dni": empleado["dni"],
            "nombre": empleado["nombre"],
            "apellido": empleado["apellido"],
            "rol_id": empleado["rol_id"]
        })

    commitear(cursor)
    return empleados_lista, 200

def cambiar_rol_empleado_service(dni: int, nuevo_rol_id: int):
    """Service que, dado el dni de un empleado, y el
        id de un rol, le asigna a dicho empleado el
        nuevo rol."""
    cursor = conectarse_db()
    empleado = consultar_usuario_por_dni(dni, cursor) 

    if empleado is None:
        commitear(cursor)
        return {
            "error": "Empleado no encontrado"
        }, 404

    rol = obtener_rol_por_id(nuevo_rol_id, cursor)

    if rol is None:
        commitear(cursor)
        return {
            "error": "Rol inexistente"
        }, 404

    if empleado["rol_id"] == nuevo_rol_id:
        commitear(cursor)
        return {
            "error": "El empleado ya posee ese rol"
        }, 400

    actualizar_rol_empleado(dni, nuevo_rol_id, cursor)
    commitear(cursor)

    return {
        "mensaje": "Rol actualizado correctamente"
    }, 200
