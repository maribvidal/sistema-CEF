from db.operaciones.clases.consultar_db import consultar_clase_por_id, consultar_disponibilidad_clase
from db.operaciones.usuario_inscribir_clase.consultar_db import consultar_usuario_inscribir_clase_por_usuario_id, consultar_superposicion_horaria_clase_usuario
from db.operaciones.usuario_inscribir_clase.insertar_db import insertar_usuario_inscribir_clase
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.pagos.consultar_db import consultar_pagos_de_usuario
from db.checkeos.checkear_inputs import checkear_inputs
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.imagenes.insertar_db import insertar_imagen
from db.operaciones.imagenes.consultar_db import consultar_imagen_actual_usuario
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_dni, consultar_usuario_por_correo, consultar_usuario_por_id, listar_usuarios, obtener_clases_usuario
from db.operaciones.usuarios.insertar_db import insertar_usuario
from db.operaciones.usuarios.modificar_db import modificar_perfil_usuario, modificar_contraseña, modificar_avatar
from db.operaciones.mensualidades.consultar_db import consultar_mensualidad_cubre_clase

from dotenv import load_dotenv
load_dotenv()

import os
import resend
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
        return respuesta, 401
    
    if respuesta['status'] == 'success' and respuesta['data'] is not None:
        cursor.connection.close()
        return {
            "error": "El DNI ya se encuentra registrado."
        }, 402
    
    respuesta = consultar_usuario_por_correo(correo, cursor)
    if respuesta['status'] == 'error':
        cursor.connection.close()
        return respuesta, 403

    if respuesta['status'] == 'success' and respuesta['data'] is not None:
        cursor.connection.close()
        return {
            "error": "El correo electrónico ya se encuentra registrado."
        }, 404
    
    if (_es_fecha_valida(fecha_nac) is False):
        cursor.connection.close()
        return {
            "error": "La fecha de nacimiento no es válida."
        }, 405
    
    if _obtener_años_hasta_2026(fecha_nac) < 14:
        cursor.connection.close()
        return {
            "error": "El usuario debe ser mayor de 14 años"
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
            "error": res['message']
        }, 500

    cursor.connection.commit()
    cursor.connection.close()
    return {
        "mensaje": "Usuario registrado exitosamente."
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
            "error": "Usuario no encontrado."
        }, 401

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

    if usuario['status'] == 'success' and not usuario['data']:
        cursor.connection.close()
        return {
            "error": "Usuario no encontrado."
        }, 401
    
    pagos = consultar_pagos_de_usuario(usuario_id, cursor)

    if pagos['status'] == 'error':
        cursor.connection.close()
        return {
            "error": pagos['message']
        }, 500

    if not pagos['data']:
        cursor.connection.close()
        return {
            "error": "No se encontraron pagos para este usuario."
        }, 402

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
        }, 402

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
            return respuesta, 403

        if respuesta['status'] == 'success' and respuesta['data'] is not None:
            cursor.connection.close()
            return {
                "error": "El correo electrónico ya se encuentra registrado."
            }, 404
    
    if telefono is not None:
        datos_a_actualizar.append({"name": "telefono", "value": telefono})
    
    errores = checkear_inputs(
        datos_a_actualizar
    )
    
    if len(errores) > 0:
        cursor.connection.close()
        return errores, 403
    
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
            "error": "Se produjo un error desde el lado del servidor al modificar el perfil del usuario."
        }, 500

    cursor.connection.commit()
    cursor.connection.close()
    return {
        "mensaje": "Perfil actualizado exitosamente."
    }, 200

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

    if usuario['status'] == 'success' and not usuario['data']:
        cursor.connection.close()
        return {
            "error": "Usuario no encontrado."
        }, 402

    # Comprobar que la contraseña actual coincide

    if usuario['data']["contraseña"] != contraseña_actual:
        cursor.connection.close()
        return {
            "error": "La contraseña actual es incorrecta."
        }, 403

    # Comprobar que la contraseña actual no sea igual a la nueva contraseña
    
    if contraseña_actual == contraseña_nueva:
        cursor.connection.close()
        return {
            "error": "La nueva contraseña no puede ser igual a la contraseña actual."
        }, 404

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
        "mensaje": "Contraseña modificada exitosamente."
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

    if usuario['status'] == 'success' and not usuario['data']:
        cursor.connection.close()
        return {
            "error": "Usuario no encontrado con el correo proporcionado."
        }, 402

    api_key = os.getenv("RESEND_API_KEY")
    resend.api_key = api_key
    
    front_url = os.getenv("FRONT_URL")
    link = f"{front_url}/ConfirmarNuevaContrasena?correo={correo}"
    
    respuesta = resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": correo,
        "subject": "Recuperación de contraseña",
        "html": f"""
            <h2>Recuperar contraseña</h2>

            <p>Hacé click acá:</p>

            <a href="{link}">
                Restablecer contraseña
            </a>
        """
    })

    cursor.connection.close()
    return {
        "mensaje": "Se ha enviado un correo electrónico con instrucciones para restablecer la contraseña."
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

    if usuario['status'] == 'success' and not usuario['data']:
        cursor.connection.close()
        return {
            "error": "Usuario no encontrado con el correo proporcionado."
        }, 402
        
    if usuario['data']['contraseña'] == nueva_contraseña:
        cursor.connection.close()
        return {
            "error": "La nueva contraseña no puede ser igual a la contraseña actual."
        }, 403

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
        "mensaje": "Nueva contraseña confirmada exitosamente."
    }, 200
    
def listar_usuarios_service():
    cursor = conectarse_db()
    
    respuesta = listar_usuarios(cursor)
    
    cursor.connection.close()
    
    if respuesta['status'] == 'error':
        return {
            "error": respuesta['message']
        }, 500
        
    if respuesta['status'] == 'success' and respuesta['data'] is None:
        return {
            "error": "No se encontraron usuarios."
        }, 404
        
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

    if respuesta['status'] == 'success' and not respuesta['data']:
        cursor.connection.close()
        return {
            "error": "Usuario no encontrado."
        }, 401

    respuesta = obtener_clases_usuario(id_usuario, cursor)

    if respuesta['status'] == 'error':
        cursor.connection.close()
        return {
            "error": respuesta['message']
        }, 500

    if respuesta['status'] == 'success' and not respuesta['data']:
        cursor.connection.close()
        return {
            "error": "No se encontraron clases para este usuario."
        }, 402

    cursor.connection.close()
    return respuesta['data'], 200

def inscribir_usuario_en_clase_service(usuario_id: int, clase_id: int):
    cursor = conectarse_db()

    usuario = consultar_usuario_por_id(usuario_id, cursor)

    if usuario['status'] == 'error':
        cursor.connection.close()
        return {
            "error": usuario['message']
        }, 500

    if usuario['status'] == 'success' and not usuario['data']:
        cursor.connection.close()
        return {
            "error": "Usuario no encontrado."
        }, 404
        
    clase = consultar_clase_por_id(clase_id, cursor)
    
    if clase['status'] == 'error':
        cursor.connection.close()
        return {
            "error": clase['message']
        }, 500
        
    if clase['status'] == 'success' and not clase['data']:
        cursor.connection.close()
        return {
            "error": "Clase no encontrada."
        }, 404
        
    res = consultar_usuario_inscribir_clase_por_usuario_id(usuario_id, clase_id, cursor)
    
    if res['status'] == 'error':
        cursor.connection.close()
        return {
            "error": res['message']
        }, 500
        
    if res['status'] == 'success' and res['data'] is not None:
        cursor.connection.close()
        return {
            "error": "El usuario ya se encuentra inscrito en esta clase."
        }, 400
        
    res = consultar_disponibilidad_clase(clase_id, cursor)
    
    if res['status'] == 'error':
        cursor.connection.close()
        return {
            "error": res['message']
        }, 500
        
    # en el front informa que no hay cupos y le da opcion de inscribirse a la lista de espera
    if res['status'] == 'success' and not res['data']:
        cursor.connection.close()
        return {
            "error": "No hay cupos disponibles para esta clase."
        }, 401
        
    # -------------  CHECKEAR  -------------
    res = consultar_mensualidad_cubre_clase(usuario_id, clase_id, cursor)
    print("respuesta mensualidad cubre clase: ", res)
    
    if res['status'] == 'error':
        cursor.connection.close()
        return {
            "error": res['message']
        }, 500
        
    if res['status'] == 'success' and not res['data']:
        cursor.connection.close()
        return {
            "error": "Debe regularizar su pago para poder reservar clases."
        }, 401

    # -------------  CHECKEAR  -------------
    res = consultar_superposicion_horaria_clase_usuario(usuario_id, clase_id, cursor)
    print("Respuesta superposicion horaria: ", res)
    
    if res['status'] == 'error':
        cursor.connection.close()
        return {
            "error": res['message']
        }, 500
    
    if res['status'] == 'success' and res['data']:
        cursor.connection.close()
        return {
            "error": "Ya posee una clase reservada en ese horario."
        }, 402

    res = insertar_usuario_inscribir_clase(usuario_id, clase_id, cursor)

    if res['status'] == 'error':
        cursor.connection.close()
        return {
            "error": res['message']
        }, 500

    cursor.connection.commit()
    cursor.connection.close()
    return {
        "mensaje": "Usuario inscrito en la clase exitosamente."
    }, 200

def subir_avatar_usuario_service(usuario_id, avatar):
    """Service que permite subir el avatar de un usuario."""

    # Validar si el parámetro recibido no está vacío

    if not avatar:
        return {
            "error": "El parámetro 'avatar' está vacío."
        }, 400

    # TODO: ¿Valido que el parámetro sea una imagen codificada?

    cursor = conectarse_db()

    # Validar si el usuario existe

    usuario = consultar_usuario_por_id(usuario_id, cursor)

    if usuario['status'] == 'error':
        cursor.connection.close()
        return {
            "error": usuario['message']
        }, 401

    if usuario['status'] == 'success' and not usuario['data']:
        cursor.connection.close()
        return {
            "error": "Usuario no encontrado."
        }, 402

    # Insertar la imagen en la base de datos

    res = insertar_imagen(avatar, cursor)

    if res['status'] == 'error':
        cursor.connection.close()
        return {
            "error": res['message']
        }, 403

    if res['status'] == 'success' and res['data'] is None:
        cursor.connection.close()
        return {
            "error": "No se pudo insertar la imagen."
        }, 404

    imagen_id = res['data']

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
        }, 405
    
    cursor.connection.commit()
    cursor.connection.close()

    return {
        "mensaje": "Avatar subido y asociado al usuario exitosamente."
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

    if usuario['status'] == 'success' and not usuario['data']:
        cursor.connection.close()
        return {
            "error": "Usuario no encontrado."
        }, 401

    # Obtener el avatar asociado al usuario

    res = consultar_imagen_actual_usuario(usuario_id, cursor)

    if res['status'] == 'error':
        cursor.connection.close()
        return {
            "error": res['message']
        }, 402
    
    if res['status'] == 'success' and res['data'] is None:
        cursor.connection.close()
        return {
            "error": "El usuario no tiene un avatar asociado."
        }, 403

    cursor.connection.close()
    return {
        "avatar": res['data']
    }, 200
