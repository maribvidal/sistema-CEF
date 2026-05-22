from db.operaciones.conectar_db import conectarse_db
from db.operaciones.empleados.consultar_db import listar_empleados
from db.operaciones.empleados.modificar_db import modificar_empleado

def listar_empleados_service():
    print("listar_empleados_service: Iniciando servicio para listar empleados")
    """Service que lista los empleados"""
    cursor = conectarse_db()
    respuesta = listar_empleados(cursor)
    print("empleados: ", respuesta)
    cursor.connection.close()

    if respuesta['status'] == 'error':
        return {
            "error": "Error al obtener empleados",
            "message": respuesta['message']
        }, 500
    elif respuesta['status'] == 'success' and not respuesta['data']:
        return {
            "error": "No se encontraron empleados"
        }, 404

    return respuesta['data'], 200


# falta implementar
def modificar_empleado_service(
    empleado_dni: int, 
    nombre: str, 
    apellido: str, 
    correo: str, 
    contraseña: str, 
    fecha_nac: str, 
    telefono: str, 
    genero: str, 
    rol_id: int
    ):
    """Service que modifica un empleado"""
    print("Ejecutando Modificación de empleado con DNI:", empleado_dni)
    cursor = conectarse_db()
    respuesta = modificar_empleado(empleado_dni, nombre, apellido, correo, contraseña, fecha_nac, telefono, genero, rol_id, cursor)

    # Con esto guardo los cambios en la base de datos
    cursor.connection.commit()
    cursor.connection.close()

    print("KEYS DE LA RESPUESTA")
    print(respuesta.keys())
    return respuesta, 200