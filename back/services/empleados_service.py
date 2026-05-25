from db.operaciones.conectar_db import conectarse_db
from db.operaciones.empleados.consultar_db import listar_empleados
from db.operaciones.empleados.modificar_db import modificar_empleado
from db.operaciones.empleados.modificar_db import borrar_empleado
from db.operaciones.empleados.modificar_db import desactivar_empleado
from db.operaciones.empleados.consultar_db import listar_empleados_desactivados

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
    if respuesta['status'] == 'error':
        return {
            "error": "Error al intentar modificar empleado",
            "message": respuesta['message']
        }, 500
    return respuesta, 200

def borrar_empleado_service(empleado_dni: int):
    """Service que borra un empleado"""
    print("borrar_empleado_service: Iniciando servicio para borrar empleado")
    cursor = conectarse_db()
    respuesta = borrar_empleado(empleado_dni, cursor)
    print("RESPUESTA: ", respuesta)
    cursor.connection.close()

    if respuesta['status'] == 'error':
        return {
            "error": "Error al intentar borrar empleado",
            "message": respuesta['message']
        }, 500
    elif respuesta['status'] == 'success' and not respuesta['data']:
        return {
            "error": "No se encontraron empleados"
        }, 404

    return respuesta['data'], 200

def desactivar_empleado_service(empleado_dni: int):
   """Service que desactiva un empleado""" 

   cursor = conectarse_db()
   respuesta = desactivar_empleado(empleado_dni, cursor)
   print("RESPUESTA: ", respuesta)
   cursor.connection.close()

   if respuesta['status'] == 'error':
       return {
           "error": "Error al intentar borrar empleado",
           "message": respuesta['message']
       }, 500
# ESTO NO ES NECESARIO: CUANDO HAGO EJECUTAR QUERY ME DEVUELVE "SUCCESS" PRO CON DATA = NONE, y eso no significa que no se encontró el empleado, sino que se ejecutó la consulta pero no devuelve datos, lo cual es normal porque es un UPDATE, no un SELECT
#    elif respuesta['status'] == 'success' and not respuesta['data']: 
#        return {
#            "error": "No se encontraron empleados"
#        }, 404
   return respuesta['data'], 200

def listar_empleados_desactivados_service():
    """Service que lista los empleados desactivados"""
    cursor = conectarse_db()
    respuesta = listar_empleados_desactivados(cursor)
    print("empleados desactivados: ", respuesta)
    cursor.connection.close()

    if respuesta['status'] == 'error':
        return {
            "error": "Error al obtener empleados desactivados",
            "message": respuesta['message']
        }, 500
    elif respuesta['status'] == 'success' and not respuesta['data']:
        return {
            "error": "No se encontraron empleados desactivados"
        }, 404

    return respuesta['data'], 200
