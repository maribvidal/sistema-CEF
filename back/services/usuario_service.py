from db.operaciones.clases.consultar_db import consultar_clase_por_id
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.pagos.consultar_db import consultar_pagos_de_usuario
from db.checkeos.checkear_inputs import checkear_inputs
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.imagenes.insertar_db import insertar_imagen
from db.operaciones.imagenes.consultar_db import consultar_imagen_actual_usuario
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_dni, consultar_usuario_por_correo, consultar_usuario_por_id, listar_usuarios, obtener_clases_usuario, listar_dnis_usuarios, obtener_estado_usuario
from db.operaciones.usuarios.insertar_db import insertar_usuario
from db.operaciones.usuarios.modificar_db import modificar_perfil_usuario, modificar_contraseña, modificar_avatar, modificar_estado_usuario
from db.operaciones.mensualidades.consultar_db import consultar_mensualidad_cubre_clase
from db.operaciones.empleados.consultar_db import listar_dnis_empleados
from db.operaciones.usuarios.consultar_db import obtener_clases_usuario

from utils.envio_mails import enviar_mail, enviar_mail_confirmacion_nuevo_correo, enviar_mail_verificacion_registro
from services import _controlar_errores_query, _msj_exito_helper

from dotenv import load_dotenv
load_dotenv()

import datetime

# FALTA PENSAR DONDE ES NECESARIO CHECKEAR QUE EL ROL SEA = 3

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

    def _es_un_rol_valido(rol: int) -> bool:
        """Se devuelve si el rol es válido o no"""
        if (rol >= 0 and rol <= 4):
            return True
        return False

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
    
    def _es_correo_unico(correo: str) -> bool:
        """Se devuelve si el correo es único o no"""
        respuesta = consultar_usuario_por_correo(correo, cursor)
        return respuesta['status'] == 'success' and respuesta.get('data') is None


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
    
    # Comprobaciones de las entradas
    if len(errores) > 0:
        return errores, 400

    if (not _es_un_rol_valido(rol_id)):
        return {
            "message": "El rol_id pasado no es válido."
        }, 401

    if (_es_fecha_valida(fecha_nac) is False):
        cursor.connection.close()
        return {
            "message": "La fecha de nacimiento no es válida."
        }, 402
    
    if _obtener_años_hasta_2026(fecha_nac) < 14:
        cursor.connection.close()
        return {
            "message": "El usuario debe ser mayor de 14 años"
        }, 403

    cursor = conectarse_db()

    # Comprobaciónes del DNI
    res_dnis = listar_dnis_usuarios(cursor)

    if res_dnis['status'] == 'error':
        cursor.connection.close()
        return {
            "message": "Error al obtener los DNIs de los usuarios."
        }, 404

    for res_dni in res_dnis['data']:
        if dni == res_dni['dni']:
            cursor.connection.close()
            return {
                "message": "El DNI ya se encuentra registrado para un usuario."
            }, 405

    # Comprobar que el correo no se haya utilizado

    if not _es_correo_unico(correo):
        cursor.connection.close()
        return {
            "message": "El correo electrónico ya se encuentra registrado."
        }, 406

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
            "message": res['message']
        }, 500

    cursor.connection.commit()

    # --- INICIO LÓGICA DE CORREO DE VERIFICACIÓN ---
    try:
        from flask import request
        from utils.envio_mails import enviar_mail_verificacion_registro

        nuevo_usuario_id: int = int(res["data"])

        enlace_verificacion = (
            f"{request.host_url}usuarios/{nuevo_usuario_id}/verificar_correo"
        )

        enviar_mail_verificacion_registro(
            nuevo_usuario_id,
            correo,
            enlace_verificacion
        )
    except Exception as e:
        print(f"Error al enviar el correo de registro al usuario {correo}: {e}")
    # --- FIN LÓGICA DE CORREO ---

    cursor.connection.close()
    return {
        "message": "Usuario registrado exitosamente."
    }, 200
    
def obtener_perfil_usuario_service(usuario_id: int):
    cursor = conectarse_db()
    usuario = consultar_usuario_por_id(usuario_id, cursor)

    if usuario['status'] == 'error':
        cursor.connection.close()
        return usuario, 400

    cursor.connection.close()
    return {
        "perfil": usuario['data']
    }, 200
    
def listar_pagos_usuario_service(usuario_id: int):
    cursor = conectarse_db()
    usuario = consultar_usuario_por_id(usuario_id, cursor)
    
    if usuario['status'] == 'error':
        cursor.connection.close()
        return usuario, 400
    
    pagos = consultar_pagos_de_usuario(usuario_id, cursor)

    if pagos['status'] == 'error':
        cursor.connection.close()
        return {
            "error": pagos['message']
        }, 500

    cursor.connection.close()
    return pagos['data'], 200
    
def editar_perfil_usuario_service(
    usuario_id: int,
    dni=None,
    nombre=None,
    apellido=None,
    fecha_nac=None,
    correo: str="",
    telefono=None
): 
    def _obtener_años_hasta_2026(fecha) -> int:
        """Se devuelve la cantidad de años que faltan hasta
            el año actual, si la fecha es válida"""
        fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d")
        return 2026 - fecha.year

    def _es_correo_unico(correo: str) -> bool:
        """Se devuelve si el correo es único o no"""
        respuesta = consultar_usuario_por_correo(correo, cursor)
        return respuesta['status'] == 'success' and respuesta.get('data') is None

    cursor = conectarse_db()
    
    usuario = consultar_usuario_por_id(usuario_id, cursor)

    if usuario['status'] == 'error':
        cursor.connection.close()
        return {"message": usuario['message']}, 400

    if not _es_correo_unico(correo):
        cursor.connection.close()
        return {
            "message": "El correo electrónico ya se encuentra registrado."
        }, 406

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
        
        respuesta = consultar_usuario_por_correo(correo, cursor)
        if respuesta['status'] == 'error':
            cursor.connection.close()
            return respuesta, 402
    
    if telefono is not None:
        datos_a_actualizar.append({"name": "telefono", "value": telefono})
    
    errores = checkear_inputs(
        datos_a_actualizar
    )
    
    if len(errores) > 0:
        cursor.connection.close()
        return {"message": "Errores de validación en los datos"}, 400

    
    if fecha_nac is not None and _obtener_años_hasta_2026(fecha_nac) < 14:
        cursor.connection.close()
        return {"message": "El usuario debe ser mayor de 14 años"}, 403

    res = modificar_perfil_usuario(
        cursor,
        usuario_id,
        dni or None,
        nombre or None,
        apellido or None,
        fecha_nac or None,
        correo or None,
        telefono or None
    )
    
    if res['status'] == 'error':
        cursor.connection.close()
        return {
            "message": "Se produjo un error desde el lado del servidor al modificar el perfil del usuario."
        }, 500

    cursor.connection.commit()
    if correo is None:
        cursor.connection.close()
        return {
            "message": "Perfil actualizado exitosamente."
        }, 200
    else:
        enviar_mail_confirmacion_nuevo_correo(usuario_id, f"https://www.google.com", cursor) #El link está como placeholder mientras vemos que hacer
        cursor.connection.close()
        return {
            "message": "Perfil actualizado exitosamente. Se ha enviado un correo de aviso al nuevo correo electrónico."
        }, 200

def confirmar_nuevo_correo_service(usuario_id: int, correo: str):
    cursor = conectarse_db()
    modificar_perfil_usuario(
        cursor=cursor,
        usuario_id=usuario_id,
        correo=correo
    )
    print("Correo cambiado con éxito.")

# Servicios para las HUs de contraseñas

def modificar_contraseña_service(
    usuario_id: int,
    contraseña_actual: str,
    contraseña_nueva: str
):
    """Service que permite modificar la contraseña de un usuario,
        habiendo realizado previamente una comprobación de las entradas."""

    """
    def _validar_input_contraseña(contraseña: str) -> bool:
        ""Se devuelve si la nueva contraseña cumple con las validaciones.""
        if len(contraseña) < 8:
            return False
        if contraseña[0].isalnum(): # se permiten caracteres alfanumericos
            return False
        return True

    # Validaciones de contraseña    
    if not _validar_input_contraseña(contraseña_nueva):
        return {
            "error": "La nueva contraseña no cumple con las validaciones."
        }, 400
    """   
     
    errores = checkear_inputs(
        [
            {"name": "contraseña", "value": contraseña_nueva}
        ]
    )
    
    if len(errores) > 0:
        return errores, 400

    # Comprobar que el usuario existe
    cursor = conectarse_db()
    
    usuario = consultar_usuario_por_id(usuario_id, cursor)

    if usuario['status'] == 'error':
        cursor.connection.close()
        return {
            "error": usuario['message']
        }, 401

    # Comprobar que la contraseña actual coincide

    if usuario['data']["contraseña"] != contraseña_actual:
        cursor.connection.close()
        return {
            "error": "La contraseña actual es incorrecta."
        }, 402

    # Comprobar que la contraseña actual no sea igual a la nueva contraseña
    
    if contraseña_actual == contraseña_nueva:
        cursor.connection.close()
        return {
            "error": "La nueva contraseña no puede ser igual a la contraseña actual."
        }, 403

    # Modificar la contraseña del usuario

    res = modificar_contraseña(
        usuario_id,
        contraseña_nueva,
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
        "message": "Contraseña modificada exitosamente."
    }, 200

def restablecer_contraseña_service(correo: str):
    """Service que permite restablecer la contraseña de un usuario,
        habiendo realizado previamente una comprobación de las entradas."""

    if not correo:
        return {
            "error": "El correo electrónico es requerido para restablecer la contraseña."
        }, 400

    cursor = conectarse_db()
    
    usuario = consultar_usuario_por_correo(correo, cursor)

    if usuario['status'] == 'error':
        cursor.connection.close()
        return {
            "error": usuario['message']
        }, 401

    link = f"http://localhost:5173/ConfirmarNuevaContrasena?correo={correo}"
    mensaje = f"Hacé click en el siguiente enlace para restablecer tu contraseña: {link}"
    enviar_mail(correo, "Reestablecer contraseña", mensaje)
    
    cursor.connection.close()
    return {
        "message": "Se ha enviado un correo electrónico con instrucciones para restablecer la contraseña."
    }, 200
    
# checkeo de escenario 4 de olvidar contraseña se haria en el front no?
# checkeo de que las nuevas contraseñas sean iguales 
def confirmar_nueva_contrasena_service(nueva_contraseña: str, correo: str):
    """Service que permite confirmar la nueva contraseña de un usuario después de haber solicitado el restablecimiento,
        habiendo realizado previamente una comprobación de las entradas."""

    if not nueva_contraseña:
        return {
            "error": "La nueva contraseña es requerida para confirmar el restablecimiento de la contraseña."
        }, 400
        
    errores = checkear_inputs(
        [
            {"name": "contraseña", "value": nueva_contraseña}
        ]
    )
    
    if len(errores) > 0:
        return errores, 400

    cursor = conectarse_db()
    
    usuario = consultar_usuario_por_correo(correo, cursor)
    
    if usuario['status'] == 'error':
        cursor.connection.close()
        return {
            "error": usuario['message']
        }, 401
        
    if usuario['data']['contraseña'] == nueva_contraseña:
        cursor.connection.close()
        return {
            "error": "La nueva contraseña no puede ser igual a la contraseña actual."
        }, 402

    res = modificar_contraseña(
        usuario['data']['id'],
        nueva_contraseña,
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
        "message": "Nueva contraseña confirmada exitosamente."
    }, 200
    
def listar_usuarios_service():
    cursor = conectarse_db()
    
    respuesta = listar_usuarios(cursor)
    
    cursor.connection.close()
    
    if respuesta['status'] == 'error':
        return {
            "error": respuesta['message']
        }, 500
        
    return respuesta['data'], 200

def obtener_clases_usuario_service(id_usuario: int):
    cursor = conectarse_db()

    print("id usuario: ", id_usuario)
    respuesta = consultar_usuario_por_id(id_usuario, cursor)

    if respuesta['status'] == 'error':
        cursor.connection.close()
        return {
            "error": respuesta['message']
        }, 400
    
    respuesta = obtener_clases_usuario(id_usuario, cursor)

    if respuesta['status'] == 'error':
        cursor.connection.close()
        return {
            "error": respuesta['message']
        }, 500

    cursor.connection.close()
    return respuesta['data'], 200

def subir_avatar_usuario_service(usuario_id, avatar):
    """Service que permite subir el avatar de un usuario."""

    # Validar si el parámetro recibido no está vacío

    if not avatar:
        return {
            "error": "El parámetro 'avatar' está vacío."
        }, 400

    cursor = conectarse_db()

    # Validar si el usuario existe

    usuario = consultar_usuario_por_id(usuario_id, cursor)

    if usuario['status'] == 'error':
        cursor.connection.close()
        return {
            "error": usuario['message']
        }, 401

    # Insertar la imagen en la base de datos

    res = insertar_imagen(avatar, cursor)

    if res['status'] == 'error':
        cursor.connection.close()
        return {
            "error": res['message']
        }, 402

    imagen_id = res['data']

    if not isinstance(imagen_id, int):
        cursor.connection.close()
        return {
            "error": "No se pudo obtener un id de imagen válido."
        }, 500

    # Asociar la imagen al usuario

    res2 = modificar_avatar(usuario_id, imagen_id, cursor)

    if res2['status'] == 'error':
        cursor.connection.close()
        return {
            "error": res2['message']
        }, 500
    
    if res2['status'] == 'success' and res2['data'] is not None:
        cursor.connection.close()
        return {
            "error": "Ocurrió un error al intentar asociar la imagen al usuario."
        }, 403
    
    cursor.connection.commit()
    cursor.connection.close()

    return {
        "message": "Avatar subido y asociado al usuario exitosamente."
    }, 200

def obtener_avatar_usuario_service(usuario_id):
    """Service que permite obtener el avatar de un usuario dado."""

    cursor = conectarse_db()

    # Validar si el usuario existe

    usuario = consultar_usuario_por_id(usuario_id, cursor)

    if usuario['status'] == 'error':
        cursor.connection.close()
        return {
            "error": usuario['message']
        }, 400

    # Obtener el avatar asociado al usuario
    res = consultar_imagen_actual_usuario(usuario_id, cursor)

    if res['status'] == 'error':
        cursor.connection.close()
        return {
            "error": res['message']
        }, 401

    cursor.connection.close()
    return {
        "avatar": res['data']
    }, 200

def verificar_correo_usuario_service(usuario_id):
    """Service que permite verificar el correo de un usuario dado. Cambiando su estado de 0 a 1 en la bade de datos"""

    cursor = conectarse_db()

    # Validar si el usuario existe
    usuario = consultar_usuario_por_id(usuario_id, cursor)

    if usuario['status'] == 'error':
        cursor.connection.close()
        return {
            "error": usuario['message']
        }, 400
    print("el usuario existe")

    usuario = obtener_estado_usuario(usuario_id, cursor)
    if usuario['status'] == 'error':
        cursor.connection.close()
        return {
            "error": usuario['message']
        }, 400
    print("se encontró el estado del usuario usuario")
    print("Imprimiendo estado del usuario: ", usuario['data'])

    estado = usuario['data']['estado']
    if estado == 1:
        cursor.connection.close()
        return {
            "message": "El correo del usuario ya está verificado."
        }, 401
    print("el correo del usuario no está verificado, se procede a verificarlo")

    # Ahora seteamos su campo "estado" a 1, indicando que su correo está verificado
    resultado = modificar_estado_usuario(usuario_id, cursor)

    if resultado['status'] == 'error':
        cursor.connection.close()
        return {
            "error": "No se pudo verificar el correo del usuario."
        }, 401
    print("Se pudo modificar el estado del usuario en 1, indicando que su correo está verificado")

    cursor.connection.close()
    return {
        "message": "Correo verificado exitosamente."
    }, 200

def obtener_clases_usuario_service(usuario_id):
    """Service que permite obtener las clases."""

    cursor = conectarse_db()

    # Controlar que exista el usuario
    respuesta = usuario = consultar_usuario_por_id(usuario_id, cursor)
    control = _controlar_errores_query(respuesta, 400, "El usuario no existe.", 401, cursor)
    if control is not None:
        return control

    respuesta = obtener_clases_usuario(usuario_id, cursor)
    control = _controlar_errores_query(respuesta, 402, "No se pudieron obtener las clases de usuario.", 403, cursor)
    if control is not None:
        return control
    
    cursor.connection.close()
    return _msj_exito_helper("Se devolvieron las clases a las cuales el usuario está inscript con éxito.", cursor, respuesta["data"])
