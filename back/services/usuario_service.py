from db.operaciones.usuarios.insertar_db import insertar_usuario
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_correo, consultar_usuario_por_dni, consultar_usuario_por_id
from db.operaciones.pagos.consultar_db import consultar_pagos_de_usuario
from db.operaciones.usuarios.modificar_db import modificar_perfil_usuario
from db.checkeos.checkear_inputs import checkear_inputs

import datetime

def registrar_usuario_service(
    dni: int,
    nombre: str,
    apellido: str,
    contraseña: str,
    fecha_nac,
    correo: str,
    telefono: str,
    genero: str
):
    """"Service que registra un usuario habiendo 
        realizado una comprobación de las entradas
        previamente."""

    def _es_fecha_valida(fecha: str) -> bool:
        """Se devuelve si la fecha es válida o no"""
        try:
            datetime.datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _obtener_años_hasta_2026(fecha: str) -> int:
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

    if consultar_usuario_por_dni(dni):
        return {
            "error": "El DNI ya se encuentra registrado"
        }, 400
    
    if consultar_usuario_por_correo(correo):
        return {
            "error": "El correo electrónico ya se encuentra registrado"
        }, 400
    
    if (_es_fecha_valida(fecha_nac) is False):
        return {
            "error": "La fecha de nacimiento no es válida."
        }, 400

    if _obtener_años_hasta_2026(fecha_nac) < 14:
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
        genero
    )

    return {
        "mensaje": "Usuario registrado exitosamente"
    }, 201
    
def obtener_perfil_usuario_service(usuario_id: int):
    usuario = consultar_usuario_por_id(usuario_id)

    if not usuario:
        return {
            "error": "Usuario no encontrado"
        }, 404

    perfil = {
        "id": usuario[0],
        "dni": usuario[1],
        "nombre": usuario[2],
        "apellido": usuario[3],
        "fecha_nac": usuario[5],
        "correo": usuario[6],
        "telefono": usuario[7],
        "genero": usuario[8]
    }

    return {
        "perfil": perfil
    }, 200
    
def listar_pagos_usuario_service(usuario_id: int):
    usuario = consultar_usuario_por_id(usuario_id)

    if not usuario:
        return {
            "error": "Usuario no encontrado"
        }, 404
    
    ## aca hay un tema y es que me tira que no hay pagos para usuarios que si los tienen
    pagos = consultar_pagos_de_usuario(usuario_id)

    if not pagos:
        return {
            "error": "No se encontraron pagos para este usuario"
        }, 404

    return {
        "pagos": pagos
    }, 200
    
def editar_perfil_usuario_service(
    usuario_id: int,
    correo: str,
    telefono: str
):
    usuario = consultar_usuario_por_id(usuario_id)

    if not usuario:
        return {
            "error": "Usuario no encontrado"
        }, 404

    errores = checkear_inputs(
        [
            {"name": "correo", "value": correo},
            {"name": "telefono", "value": telefono}
        ]
    )
    
    if len(errores) > 0:
        return errores, 400

    # Verificar si el nuevo correo ya está registrado por otro usuario
    usuario_con_correo = consultar_usuario_por_correo(correo)
    if usuario_con_correo and usuario_con_correo[0] != usuario_id:
        return {
            "error": "El correo electrónico ya se encuentra registrado por otro usuario"
        }, 400
    
    modificar_perfil_usuario(
        usuario_id,
        correo,
        telefono
    )

    return {
        "mensaje": "Perfil actualizado exitosamente"
    }, 200