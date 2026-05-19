from db.operaciones.consultar_db import consultar_usuario_por_dni, obtener_rol_por_id, obtener_empleados
from db.operaciones.modificar_db import actualizar_rol_empleado

def obtener_empleados_service():
    """Service que comprueba que hayan empleados registrados,
        y si los hay, devuelve una lista de empleados"""
    empleados = obtener_empleados()

    if not empleados:
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

    return empleados_lista, 200

def cambiar_rol_empleado_service(dni: int, nuevo_rol_id: int):
    """Service que, dado el dni de un empleado, y el
        id de un rol, le asigna a dicho empleado el
        nuevo rol."""
    empleado = consultar_usuario_por_dni(dni) 

    if empleado is None:
        return {
            "error": "Empleado no encontrado"
        }, 404

    rol = obtener_rol_por_id(nuevo_rol_id)

    if rol is None:
        return {
            "error": "Rol inexistente"
        }, 404

    if empleado["rol_id"] == nuevo_rol_id:
        return {
            "error": "El empleado ya posee ese rol"
        }, 400

    actualizar_rol_empleado(dni, nuevo_rol_id)

    return {
        "mensaje": "Rol actualizado correctamente"
    }, 200
