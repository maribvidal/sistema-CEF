from db.operaciones import (
    obtener_empleado_por_dni,
    obtener_rol_por_id,
    actualizar_rol_empleado,
    obtener_empleados
)

def obtener_empleados_service():
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

def cambiar_rol_empleado(dni: int, nuevo_rol_id: int):

    empleado = obtener_empleado_por_dni(dni) 

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