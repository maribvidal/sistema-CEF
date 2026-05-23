from db.operaciones.conectar_db import conectarse_db
from db.operaciones.usuarios.insertar_db import insertar_usuario
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_correo, consultar_usuario_por_dni, consultar_usuario_por_id
from db.operaciones.pagos.consultar_db import consultar_pagos_de_usuario
from db.operaciones.usuarios.modificar_db import modificar_perfil_usuario, modificar_contraseña
from db.checkeos.checkear_inputs import checkear_inputs
from db.operaciones.conectar_db import conectarse_db

import datetime

def registrar_usuario_service(
    dni: int,
    nombre: str,
    apellido: str,
    contraseña: str,
    fecha_nac: str,
    correo: str,
    telefono: str,
    genero: str,
    rol_id: int
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
            {"name": "genero", "value": genero},
            {"name": "rol_id", "value": rol_id}
        ]
    )
    
    if len(errores) > 0:
        return errores, 400

    cursor = conectarse_db()
    respuesta = consultar_usuario_por_dni(dni, cursor)
    if respuesta['status'] == 'error':
        cursor.connection.close()
        return respuesta, 400
    
    if respuesta['status'] == 'success' and respuesta['data'] is not None:
        cursor.connection.close()
        return {
            "error": "El DNI ya se encuentra registrado"
        }, 400
    
    respuesta = consultar_usuario_por_correo(correo, cursor)
    if respuesta['status'] == 'error':
        cursor.connection.close()
        return respuesta

    if respuesta['status'] == 'success' and respuesta['data'] is not None:
        cursor.connection.close()
        return {
            "error": "El correo electrónico ya se encuentra registrado"
        }, 400
    
    if (_es_fecha_valida(fecha_nac) is False):
        cursor.connection.close()
        return {
            "error": "La fecha de nacimiento no es válida."
        }, 400
    
    print("cantidad años: ", _obtener_años_hasta_2026(fecha_nac))
    if _obtener_años_hasta_2026(fecha_nac) < 14:
        cursor.connection.close()
        return {
            "error": "El usuario debe ser mayor de 14 años"
        }, 400

    ## TODO: Si hay que agregar otra comprobación de la fecha, hacerlo
      
    res = insertar_usuario(
        dni,
        nombre,
        apellido,
        contraseña,
        fecha_nac,
        correo,
        telefono,
        genero,
        rol_id,
        cursor
    )
    
    if res['status'] == 'error':
        cursor.connection.close()
        return {
            "error": res['message']
        }, 500

    cursor.connection.commit()
    cursor.connection.close()
    return {
        "mensaje": "Usuario registrado exitosamente"
    }, 201
    
def obtener_perfil_usuario_service(usuario_id: int):
    cursor = conectarse_db()
    usuario = consultar_usuario_por_id(usuario_id, cursor)

    if usuario['status'] == 'error':
        cursor.connection.close()
        return usuario, 400
    
    if usuario['status'] == 'success' and not usuario['data']:
        cursor.connection.close()
        return {
            "error": "Usuario no encontrado"
        }, 404
        
    print(" perfil de usuario: ", dict(usuario['data']))

    perfil = {
        "id": usuario['data'][0],
        "dni": usuario['data'][1],
        "nombre": usuario['data'][2],
        "apellido": usuario['data'][3],
        "contraseña": usuario['data'][5],
        "fecha_nac": usuario['data'][6],
        "correo": usuario['data'][4],
        "telefono": usuario['data'][7],
        "genero": usuario['data'][8],
        "rol_id": usuario['data'][9]
    }

    cursor.connection.commit()
    cursor.connection.close()
    return {
        "perfil": perfil
    }, 200
    
def listar_pagos_usuario_service(usuario_id: int):
    cursor = conectarse_db()
    usuario = consultar_usuario_por_id(usuario_id, cursor)
    
    if usuario['status'] == 'error':
        cursor.connection.close()
        return usuario, 400

    if usuario['status'] == 'success' and not usuario['data']:
        cursor.connection.close()
        return {
            "error": "Usuario no encontrado"
        }, 404
    
    ## aca hay un tema y es que me tira que no hay pagos para usuarios que si los tienen
    pagos = consultar_pagos_de_usuario(usuario_id, cursor)

    if pagos['status'] == 'error':
        cursor.connection.close()
        return {
            "error": pagos['message']
        }, 500

    if not pagos['data']:
        cursor.connection.close()
        return {
            "error": "No se encontraron pagos para este usuario"
        }, 404

    cursor.connection.commit()
    cursor.connection.close()
    return pagos['data'], 200
    
def editar_perfil_usuario_service(
    usuario_id: int,
    dni=None,
    nombre=None,
    apellido=None,
    fecha_nac=None,
    correo=None,
    telefono=None
):
    
    cursor = conectarse_db()

    usuario = consultar_usuario_por_id(usuario_id, cursor)

    if usuario['status'] == 'error':
        cursor.connection.close()
        return {
            "error": usuario['message']
        }, 400

    if usuario['status'] == 'success' and not usuario['data']:
        cursor.connection.close()
        return {
            "error": "Usuario no encontrado"
        }, 401

    datos_a_actualizar = []
    
    if dni is not None:
        datos_a_actualizar.append({"name": "dni", "value": dni})
    if nombre is not None:
        datos_a_actualizar.append({"name": "nombre", "value": nombre})
    if apellido is not None:
        datos_a_actualizar.append({"name": "apellido", "value": apellido})
    if fecha_nac is not None:
        datos_a_actualizar.append({"name": "fecha_nac", "value": fecha_nac})
    if correo is not None:
        datos_a_actualizar.append({"name": "correo", "value": correo})
    if telefono is not None:
        datos_a_actualizar.append({"name": "telefono", "value": telefono})
    
    errores = checkear_inputs(
        datos_a_actualizar
    )
    
    if len(errores) > 0:
        cursor.connection.close()
        return errores, 402

    usuario_con_correo = consultar_usuario_por_correo(correo, cursor)

    if usuario_con_correo['status'] == 'error':
        cursor.connection.close()
        return usuario_con_correo, 403
        
    if usuario_con_correo['data'] and usuario_con_correo['data'][6] == correo and usuario_con_correo['data'][3] == telefono:
        cursor.connection.close()
        return {
            "error": "No se proporcionó ningún dato nuevo para actualizar"
        }, 404
    
    res = modificar_perfil_usuario(
        usuario_id,
        dni,
        nombre,
        apellido,
        fecha_nac,
        correo,
        telefono,
        cursor
    )
    
    if res['status'] == 'error':
        cursor.connection.close()
        return {
            "error": "Se produjo un error desde el lado del servidor al modificar el perfil del usuario."
        }, 500

    cursor.connection.commit()
    cursor.connection.close()
    return {
        "mensaje": "Perfil actualizado exitosamente"
    }, 200

# Servicios para las HUs de contraseñas

def modificar_contraseña_service(
    usuario_id: int,
    contraseña_actual: str,
    nueva_contraseña: str
):
    """Service que permite modificar la contraseña de un usuario,
        habiendo realizado previamente una comprobación de las entradas."""

    def _validar_input_contraseña(contraseña: str) -> bool:
        """Se devuelve si la nueva contraseña cumple con las validaciones."""
        if len(contraseña) < 8:
            return False
        if contraseña[0].isdigit():
            return False
        return True

    # Validaciones de contraseña

    if not _validar_input_contraseña(nueva_contraseña):
        return {
            "error": "La nueva contraseña no cumple con las validaciones."
        }, 401

    # Comprobar que el usuario existe

    cursor = conectarse_db()
    
    usuario = consultar_usuario_por_id(usuario_id, cursor)

    if usuario['status'] == 'error':
        cursor.connection.close()
        return {
            "error": usuario['message']
        }, 402

    if usuario['status'] == 'success' and not usuario['data']:
        cursor.connection.close()
        return {
            "error": "Usuario no encontrado."
        }, 403

    # Comprobar que la contraseña actual coincide

    if usuario['data'][5] != contraseña_actual:
        cursor.connection.close()
        return {
            "error": "La contraseña actual es incorrecta"
        }, 404

    # Comprobar que la contraseña actual no sea igual a la nueva contraseña
    
    if contraseña_actual == nueva_contraseña:
        cursor.connection.close()
        return {
            "error": "La nueva contraseña no puede ser igual a la contraseña actual"
        }, 405

    # Modificar la contraseña del usuario

    res = modificar_contraseña(
        usuario_id,
        nueva_contraseña,
        cursor
    )

    if res['status'] == 'error':
        cursor.connection.close()
        return {
            "error": "Se produjo un error desde el lado del servidor al modificar la contraseña."
        }, 500

    cursor.connection.commit()
    cursor.connection.close()
    return {
        "mensaje": "Contraseña modificada exitosamente"
    }, 200
