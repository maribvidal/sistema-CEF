from db.operaciones.conectar_db import conectarse_db
from db.operaciones.usuarios.insertar_db import insertar_usuario
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_correo, consultar_usuario_por_dni, consultar_usuario_por_id
from db.operaciones.pagos.consultar_db import consultar_pagos_de_usuario
from db.operaciones.usuarios.modificar_db import modificar_perfil_usuario
from db.checkeos.checkear_inputs import checkear_inputs
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

import datetime

def registrar_usuario_service(
    dni: int,
    nombre: str,
    apellido: str,
    contraseña: str,
    fecha_nac: str,
    correo: str,
    telefono: str,
    genero: str
):
    """"Service que registra un usuario habiendo 
        realizado una comprobación de las entradas
        previamente."""

    cursor = conectarse_db()

    def _es_fecha_valida(fecha: str) -> bool:
        """Se devuelve si la fecha es válida o no"""
        try:
            datetime.datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _obtener_años_hasta_2026(fecha) -> int:
        """Se devuelve la cantidad de años que faltan hasta
            el año actual, si la fecha es válida"""
        fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d")
        return 2026 - fecha.year

    errores = checkear_inputs(
        [
            {"name": "dni", "value": dni},
            {"name": "nombre", "value": nombre},
            {"name": "apellido", "value": apellido},
            {"name": "contraseña", "value": contraseña},
            {"name": "fecha_nac", "value": fecha_nac},
            {"name": "correo", "value": correo},
            {"name": "telefono", "value": telefono},
            {"name": "genero", "value": genero}
        ]
    )
    
    if len(errores) > 0:
        return errores, 400

    cursor = conectarse_db()
    respuesta = consultar_usuario_por_dni(dni, cursor)
    if respuesta['status'] == 'error':
        commitear(cursor)
        return respuesta
    
    if respuesta['status'] == 'success' and respuesta['data'] is not None:
        commitear(cursor)
        return {
            "error": "El DNI ya se encuentra registrado"
        }, 400
    
    respuesta = consultar_usuario_por_correo(correo, cursor)
    if respuesta['status'] == 'error':
        commitear(cursor)
        return respuesta

    if respuesta['status'] == 'success' and respuesta['data'] is not None:
        commitear(cursor)
        return {
            "error": "El correo electrónico ya se encuentra registrado"
        }, 400
    
    if (_es_fecha_valida(fecha_nac) is False):
        commitear(cursor)
        return {
            "error": "La fecha de nacimiento no es válida."
        }, 400

    if _obtener_años_hasta_2026(fecha_nac) < 14:
        commitear(cursor)
        return {
            "error": "El usuario debe ser mayor de 14 años"
        }, 400

    ## TODO: Si hay que agregar otra comprobación de la fecha, hacerlo
      
    insertar_usuario(
        dni,
        nombre,
        apellido,
        contraseña,
        fecha_nac,
        correo,
        telefono,
        genero,
        cursor
    )

    commitear(cursor)
    return {
        "mensaje": "Usuario registrado exitosamente"
    }, 201
    
def obtener_perfil_usuario_service(usuario_id: int):
    cursor = conectarse_db()
    usuario = consultar_usuario_por_id(usuario_id, cursor)

    if usuario['status'] == 'error':
        commitear(cursor)
        return usuario
    
    if usuario['status'] == 'success' and not usuario['data']:
        commitear(cursor)
        return {
            "error": "Usuario no encontrado"
        }, 404
        
    print(" perfil de usuario: ", dict(usuario['data']))

    perfil = {
        "id": usuario['data'][0],
        "dni": usuario['data'][1],
        "nombre": usuario['data'][2],
        "apellido": usuario['data'][3],
        "fecha_nac": usuario['data'][5],
        "correo": usuario['data'][6],
        "telefono": usuario['data'][7],
        "genero": usuario['data'][8]
    }

    commitear(cursor)
    return {
        "perfil": perfil
    }, 200
    
def listar_pagos_usuario_service(usuario_id: int):
    cursor = conectarse_db()
    usuario = consultar_usuario_por_id(usuario_id, cursor)

    if usuario['status'] == 'error':
        commitear(cursor)
        return usuario

    if usuario['status'] == 'success' and not usuario['data']:
        commitear(cursor)
        return {
            "error": "Usuario no encontrado"
        }, 404
    
    ## aca hay un tema y es que me tira que no hay pagos para usuarios que si los tienen
    pagos = consultar_pagos_de_usuario(usuario_id, cursor)

    if pagos['status'] == 'error':
        commitear(cursor)
        return pagos

    if not pagos['data']:
        commitear(cursor)
        return {
            "error": "No se encontraron pagos para este usuario"
        }, 404

    commitear(cursor)
    return {
        "pagos": pagos['data']
    }, 200
    
def editar_perfil_usuario_service(
    usuario_dni: int,
    correo: str,
    telefono: str
):
    cursor = conectarse_db()
    if correo is None and telefono is None:
        cursor.connection.close()
        return {
            "error": "No se proporcionó ningún dato para actualizar"
        }, 400
    
    cursor = conectarse_db()
    usuario = consultar_usuario_por_dni(usuario_dni, cursor)
    

    if usuario['status'] == 'error':
        commitear(cursor)
        return usuario

    if usuario['status'] == 'success' and not usuario['data']:
        commitear(cursor)
        return {
            "error": "Usuario no encontrado"
        }, 404

    datos_a_actualizar = []
    
    if correo is not None:
        datos_a_actualizar.append({"name": "correo", "value": correo})
    if telefono is not None:
        datos_a_actualizar.append({"name": "telefono", "value": telefono})
    
    
    errores = checkear_inputs(
        datos_a_actualizar
    )
    
    if len(errores) > 0:
        commitear(cursor)
        return errores, 400

    usuario_con_correo = consultar_usuario_por_correo(correo, cursor)

    if usuario_con_correo['status'] == 'error':
        commitear(cursor)
        return usuario_con_correo
    
    
    if usuario_con_correo['status'] == 'success' and usuario_con_correo['data'] and usuario_con_correo['data'][1] != usuario_dni:
         commitear(cursor)
         return {
            "error": "El correo electrónico ya se encuentra registrado por otro usuario"
        }, 400
        
    if usuario_con_correo['data'] and usuario_con_correo['data'][6] == correo and usuario_con_correo['data'][3] == telefono:
        commitear(cursor)
        return {
            "error": "No se proporcionó ningún dato nuevo para actualizar"
        }, 400
    
    cursor = conectarse_db()
    modificar_perfil_usuario(
        usuario_dni,
        correo,
        telefono,
        cursor
    )

    commitear(cursor)
    return {
        "mensaje": "Perfil actualizado exitosamente"
    }, 200
