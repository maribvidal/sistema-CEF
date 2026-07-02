from db.operaciones.usuario_pertenece_lista_espera_abonados.insertar_db import insertar_usuario_pertenece_lista_espera_abonados
from db.operaciones.listas_espera.insertar_db import insertar_lista_espera_abonados
from db.operaciones.reservas.consultar_db import consultar_reserva_por_usuario_clase
from db.operaciones.instancias_clases.consultar_db import revisar_validez_cupos
from db.operaciones.mensualidades.consultar_db import obtener_clase_mensualidad, obtener_mensualidad_por_id
from services import _controlar_errores_query
from db.operaciones.exception_handler import ejecutar_insertar, ejecutar_query
from utils.modulo_manejo_listas import revisar_cupos_disponible_abonado, revisar_si_hay_cupos

import datetime
from datetime import date
from dateutil.parser import parse

def formattear_fecha(fecha):
    """Función interna que formattea la fecha al
        formato pedido, suponiendo que se recibe
        un objeto tipo date, datetime, o un str
        pero que tiene una fecha dentro suyo."""
    if isinstance(fecha, date) and not isinstance(fecha, datetime.datetime):
        return fecha.strftime("%Y-%m-%d")
    if isinstance(fecha, datetime.datetime):
        return fecha.date().strftime("%Y-%m-%d")
    if isinstance(fecha, str):
        fecha = parse(fecha, dayfirst=False)
        return fecha.date().strftime("%Y-%m-%d")

# HABRIA QUE MODIFICAR ESTO, ES 1 MES. NO SE TENDRIAN QUE PODER PASAR CUALQUIER FECHA DE INICIO Y FIN
def insertar_mensualidad(usuario_id: int, cursor, fecha_ini = None):
    """Permite insertar una fila para la tabla Mensualidad"""
    query = f"""INSERT INTO Mensualidad (fecha_ini, fecha_fin, usuario_id, estado)"""
    
    if fecha_ini is None:
        valores = f""" 
            VALUES (DATE('now'), DATE('now', '+1 month'), {usuario_id}, 1)
        """
    else:
        fecha = formattear_fecha(fecha_ini)
        valores = f"""VALUES ('{fecha}', DATE('{fecha}', '+1 month'), {usuario_id}, 1);"""
    
    query += valores
    return ejecutar_insertar(query, cursor)

def insertar_mensualidad_con_fin(usuario_id: int, cursor, fecha_ini, fecha_fin):
    """Permite insertar una fila para la tabla Mensualidad"""
    query = f"""INSERT INTO Mensualidad (fecha_ini, fecha_fin, usuario_id)
                                VALUES  ('{fecha_ini}', '{fecha_fin}', {usuario_id});
    """
    return ejecutar_insertar(query, cursor)

def insertar_reservas_mensualidad(usuario_id: int, instancias_clase: dict, cursor):
    """Permite insertar las reservas de una mensualidad"""
    ids = []
    for key in instancias_clase.keys():
        query = f"""
            INSERT INTO Reserva (usuario_id, inst_clase_id, fecha) VALUES ({usuario_id}, {key}, DATE('now'));
        """
        respuesta = ejecutar_insertar(query, cursor)
        control = _controlar_errores_query(respuesta, 500, "No se pudo insertar la reserva de la mensualidad.", 400, cursor)
        if control is not None:
            # revertir las reservas insertadas hasta el momento
            for inst_id in ids:
                query = f"""
                    DELETE FROM Reserva
                    WHERE usuario_id = {usuario_id}
                    AND inst_clase_id = {inst_id};
                """
                ejecutar_query(query, cursor)

            return control
        ids.append(respuesta['data'])
    return {
        "status": "success",
        "data": ids
    }
    
def agregar_nuevas_reservas_mensualidad(id_mensualidad: int, usuario_id: int, cursor):
    """Permite agregar nuevas reservas de una mensualidad"""
    # obtener la clase de la mensualidad
    clase = obtener_clase_mensualidad(id_mensualidad, cursor)
    control = _controlar_errores_query(clase, 500, "No se pudo obtener la clase de la mensualidad.", 400, cursor)
    if control is not None:
        return control
    
    clase_id = clase['data']['clase_id']
    
    mensualidad = obtener_mensualidad_por_id(id_mensualidad, cursor)
    control = _controlar_errores_query(mensualidad, 500, "No se encontró la mensualidad.", 400, cursor)
    if control is not None:
        return control
    
    fecha_fin = mensualidad['data']['fecha_fin']
    
    # verificar todas las reservas que necesita la mensualidad
    # primero obtenemos todas las instancias de clase
    
    
    dict_cupos = revisar_si_hay_cupos(clase_id, cursor) 
    dict_cupos = revisar_validez_cupos(dict_cupos, cursor, fecha_fin)
    
    # aca tambien verifico los cupos disponibles en las instancias???
    hay_cupos = revisar_cupos_disponible_abonado(dict_cupos)
    
    if hay_cupos:
        # de esas reservas filtrar por las que ya tiene el usuario
        for key in list(dict_cupos.keys()):
            existe_reserva = consultar_reserva_por_usuario_clase(usuario_id, key, cursor)
            
            if existe_reserva['data'] is not None:
                del dict_cupos[key]
        
        # utilizar insertar_reservas_mensualidad 
        return insertar_reservas_mensualidad(usuario_id, dict_cupos, cursor)
    else:
        # si queres agregar a la lista de espera de abonados directamente:
        # respuesta = insertar_lista_espera_abonados(clase_id, cursor)
        # control = _controlar_errores_query(respuesta, 500, "No se pudo agregar a la lista de espera de abonados.", 400, cursor)
        # if control is not None:
        #     return control
        
        # respuesta = insertar_usuario_pertenece_lista_espera_abonados(usuario_id, respuesta['data'], cursor)
        # control = _controlar_errores_query(respuesta, 500, "No se pudo agregar al usuario a la lista de espera de abonados.", 400, cursor)
        # if control is not None:
        #     return control
        
        # # se checkearia por este status afuera tmb
        # return {
        #     "status": "add_lea"
        # }
        
        # si queres preguntar antes si quiere agregarse a la lista de espera:
        # primero tendrias que devolver aca algun mensaje para hacer rollback y en el front deberia de mostrar un mensaje
        # si acepta en el front, agregarlo a la lista de espera de abonados
        
        return{
            "status": "no_cupos"
        }